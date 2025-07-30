import os
import json
import torch
import faiss
import numpy as np
from typing import Any
from google import genai
from google.genai import types
from concurrent.futures import ThreadPoolExecutor
from transformers import AutoTokenizer, AutoModel
from lib.path import get_path
from lib.token_utils import TokenManager

# === Global Settings ===
os.environ["TOKENIZERS_PARALLELISM"] = "false"
MODEL_LIST = [
    "lianghsun/Llama-3.2-Taiwan-Legal-1B-Instruct",
    "lianghsun/Llama-3.2-Taiwan-Legal-3B-Instruct",
]
MODEL_NAME = MODEL_LIST[1]
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# === Load Embeddings and FAISS Index Once ===
embedding_path = os.path.join(get_path(key="DATA"), "embeddings", "laws_embedding.json")
with open(embedding_path, "r") as f:
    data = json.load(f)
texts_cache = [item["text"] for item in data]
embeddings_cache = np.array([item["embedding"] for item in data], dtype="float32")
index_cache = faiss.IndexFlatL2(embeddings_cache.shape[1])
index_cache.add(embeddings_cache)

# === Preload Embeddings and Model and Tokenizer ===
embedding_tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
embedding_model = AutoModel.from_pretrained(MODEL_NAME, torch_dtype=torch.float16).to(
    DEVICE
)
embedding_model.eval()

# === Thread Pool Executor ===
executor = ThreadPoolExecutor(max_workers=2)

# === Gemini initialization ===
tm = TokenManager()
client = genai.Client(api_key=tm.get_google_api_key())


# === Embedding Related Works ===
def search_faiss_idx(
    query: str,
    idx: Any,
    texts: list,
    top_k: int,
    max_length: int,
) -> list:
    tokens = embedding_tokenizer(
        query, padding=True, truncation=True, max_length=max_length, return_tensors="pt"
    ).to(DEVICE)
    with torch.no_grad():
        query_embedding = (
            embedding_model(**tokens).last_hidden_state.mean(dim=1).cpu().numpy()
        )
    query_embedding = query_embedding.astype("float32")

    distances, indices = idx.search(query_embedding, top_k)
    results = [
        {"text": texts[i], "score": distances[0][j]} for j, i in enumerate(indices[0])
    ]
    return results


# === Gemini wrapper ===
def gemini_generate(prompt: str, max_token: int = 1024) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-04-17",
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_mime_type="text/plain",
                temperature=0.0,
                max_output_tokens=max_token,
            ),
        )
        return response.text.strip()
    except Exception as e:
        print(f"[Gemini Error] {e}")
        return "⚠️ 模型回應失敗。"


# === Prompt generator for answering ===
def gemini_generate_response(context: str, query: str, max_token: int = 1024) -> str:
    prompt = """
    你是一位台灣法律諮詢顧問。請閱讀使用者的問題與檢索資料，並提供清楚的法律回覆，內容包含：
    1. 相關法規的名稱、條號與條文內容
    2. 使用者敘述與法條構成要件的對應說明
    3. 初步法律建議（例如是否需尋求律師協助）
    4. 不確定時請回答「不知道」，避免提供不實資訊
    5. 回覆結尾請提醒使用者這不是正式法律意見
    """
    if context:
        prompt += f"\n下列為檢索後的參考資料，摘要重點做為參考: {context}"
    prompt += f"\n使用者的問題: {query}"
    return gemini_generate(prompt=prompt, max_token=max_token)


def gemini_rag_process(query: str, max_token: int = 1024) -> str:
    # Retrieve relevant content
    top_results = search_faiss_idx(
        query=query,
        idx=index_cache,
        texts=texts_cache,
        top_k=5,
        max_length=512,
    )
    # Merge the retrieved content into the context
    context = "\n".join([result["text"] for result in top_results])
    result = gemini_generate_response(context=context, query=query, max_token=max_token)
    return result


# === Prompt generator for comparison ===
def gemini_judgement(answer_x: str, answer_y: str, max_token: int = 64) -> str:
    prompt = f"""
    你是一位台灣法律諮詢顧問。請閱讀「回答1」與「回答2」，根據兩者的法律正確性與表達清晰度，判斷哪一個回答比較適當。
    請只回覆：「回答1」或「回答2」，不要加任何說明。
    
    回答1：{answer_x}
    
    回答2：{answer_y}
    
    較佳的回答是：
    """
    return gemini_generate(prompt=prompt, max_token=max_token)


def response_with_judgement(query: str) -> str:
    try:
        future1 = executor.submit(gemini_rag_process, query=query, max_token=1024)
        future2 = executor.submit(gemini_rag_process, query=query, max_token=1024)

        answer_1 = future1.result()
        answer_2 = future2.result()

        if not answer_1.strip() or not answer_2.strip():
            return "⚠️ 未成功產生回覆，請稍後再試。"

        answer_1 = answer_1.replace("\n", "").replace("。", "。\n")
        answer_2 = answer_2.replace("\n", "").replace("。", "。\n")

        judgement = gemini_judgement(answer_x=answer_1, answer_y=answer_2)
        if "回答1" in judgement:
            return answer_1
        elif "回答2" in judgement:
            return answer_2
        return "⚠️ 無法判斷最佳回覆，請稍後再試。"
    except TimeoutError:
        return "⚠️ 回覆超時，請稍後再試。"
