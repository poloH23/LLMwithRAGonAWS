import os
import json
import torch
import faiss
import numpy as np
from threading import Lock
from typing import Any
from lib.path import get_path
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# === Global Settings ===
MODEL_LIST = [
    "lianghsun/Llama-3.2-Taiwan-Legal-1B-Instruct",
    "lianghsun/Llama-3.2-Taiwan-Legal-3B-Instruct",
]
MODEL_NAME = MODEL_LIST[1]
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
generation_lock = Lock()

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

# === Preload Language Model for Generation
gen_tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
gen_model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, torch_dtype=torch.float16
).to(DEVICE)
gen_model.eval()

# === Thread Pool Executor ===
executor = ThreadPoolExecutor(max_workers=2)


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


def llama_generate_response(context: str, query: str, max_token: int) -> str:
    # Prompt
    prompt = """
        你是一位台灣法律諮詢顧問。請閱讀使用者的問題與檢索資料，並提供清楚的法律回覆，內容包含：
        1. 相關法規的名稱、條號與條文內容
        2. 使用者敘述與法條構成要件的對應說明
        3. 初步法律建議（例如是否需尋求律師協助）
        4. 不確定時請回答「不知道」，避免提供不實資訊
        5. 回覆結尾請提醒使用者這不是正式法律意見
        """
    if context:
        prompt += f"\n下列為檢索法條後的參考資料，請摘要重點做為參考: {context}"
    prompt += f"\n使用者的問題: {query}"

    inputs = gen_tokenizer(prompt, return_tensors="pt", padding=True).to(DEVICE)
    print(">>> Calling generate...")
    with generation_lock:
        with torch.no_grad():
            output_ids = gen_model.generate(
                input_ids=inputs.input_ids,
                attention_mask=inputs.attention_mask,
                pad_token_id=gen_tokenizer.pad_token_id,
                max_new_tokens=max_token,
                temperature=0.1,
            )
    print(">>> Generate done")
    decoded = gen_tokenizer.decode(output_ids[0], skip_special_tokens=True)
    cleaned = decoded[len(prompt) :].strip()
    return cleaned


def llama_rag_process(query: str) -> str:
    # Retrieve relevant content
    top_results = search_faiss_idx(
        query=query,
        idx=index_cache,
        texts=texts_cache,
        top_k=8,
        max_length=512,
    )
    # Merge the retrieved content into the context
    context = "\n".join([result["text"] for result in top_results])
    result = llama_generate_response(context=context, query=query, max_token=256)
    return result


def llama_judgement(
    answer_x: str,
    answer_y: str,
) -> str:
    # Set the prompt
    prompt = """
    你是一位台灣法律諮詢顧問。請閱讀「回答1」與「回答2」，根據兩者的法律正確性與表達清晰度，判斷哪一個回答比較適當。
    請僅回覆「回答1」或「回答2」。
    """
    prompt += f"\n回答1: {answer_x}\n回答2: {answer_y}\n較佳的回答是："

    inputs = gen_tokenizer(prompt, return_tensors="pt", padding=True).to(DEVICE)
    with generation_lock:
        with torch.no_grad():
            output_ids = gen_model.generate(
                input_ids=inputs.input_ids,
                attention_mask=inputs.attention_mask,
                pad_token_id=gen_tokenizer.pad_token_id,
                max_new_tokens=8,
                temperature=0.1,
            )
    decoded = gen_tokenizer.decode(output_ids[0], skip_special_tokens=True)
    cleaned = decoded[len(prompt) :].strip()
    return cleaned


def response_with_judgement(query: str) -> str:
    try:
        future1 = executor.submit(llama_rag_process, query)
        future2 = executor.submit(llama_rag_process, query)

        answer_1 = future1.result()
        answer_2 = future2.result()

        if not answer_1.strip() or not answer_2.strip():
            return "⚠️ 未成功產生回覆，請稍後再試。"

        answer_1 = answer_1.replace("\n", "").replace("。", "。\n")
        answer_2 = answer_2.replace("\n", "").replace("。", "。\n")

        judgement = llama_judgement(answer_x=answer_1, answer_y=answer_2)
        if "回答1" in judgement:
            return answer_1
        elif "回答2" in judgement:
            return answer_2
        return "⚠️ 無法判斷最佳回覆，請稍後再試。"
    except TimeoutError:
        return "⚠️ 回覆超時，請稍後再試。"
