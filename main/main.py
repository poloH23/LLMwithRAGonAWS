import os
from pyngrok import ngrok
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from lib.path import get_path
from lib.token import get_hf_token
from lib.token import get_line_access
from lib.token import get_line_secret
from lib.ngrok import start_ngrok
from lib.rag import response_with_judgement


# Add HuggingFace token
token_info = get_hf_token()
(
    print(token_info)
    if token_info is not None
    else print(">>> HuggingFace token NOT found.")
)

# Get the embedding files
fil_embeddings = os.path.join(get_path(key="DATA"), "embeddings", "laws_embedding.json")

# Line bot deployment
LINE_CHANNEL_ACCESS_TOKEN = get_line_access()
LINE_CHANNEL_SECRET = get_line_secret()
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Flask application
app = Flask(__name__)


# Line webhook
# Define Flask's HTTP routing and map Line's POST request to the callback function
@app.route("/", methods=["POST"])
# Line Webhook router receives webhook requests from the Line platform
def callback():
    # Verify the Line signature to confirm that the request was sent by the Line server
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        # Send the request content to the handler for processing
        handler.handle(body, signature)
    except InvalidSignatureError:
        # If authentication fails, an HTTP 400 error is returned.
        abort(400)
    return "Webhook processed successfully."


@handler.add(MessageEvent, message=TextMessage)
# Even handling
def handle_message(event):
    try:
        # Receive user messages
        user_message = event.message.text
        print(">>> Successfully received user message")

        # Llama generates answers
        response = response_with_judgement(query=user_message)

        # Return answers to Line users
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response))
    except Exception as e:
        print(f">>> An error occurred during processing: {str(e)}")


if __name__ == "__main__":
    # # Set the Python path
    # python_path = os.environ.get("PROJECT_ROOT") + os.getenv("PYTHONPATH")
    # env = os.environ.copy()
    # env["PYTHONPATH"] = python_path
    #
    # # Start Flask service
    # flask_process = subprocess.Popen(
    #     ["python", "-m", "flask", "--app", "main.legal_linebot_local_ver", "run", "--host=0.0.0.0", "--port=5000"],
    #     cwd=os.environ.get("PROJECT_ROOT"),
    #     env=env
    # )

    # Start ngrok
    # ngrok_url, ngrok_process = start_ngrok(port=5000)
    ngrok_url = start_ngrok(port=5000)

    try:
        app.run(host="0.0.0.0", port=5000)
    except KeyboardInterrupt:
        print(">>> 終止 Flask 和 Ngrok.")
        # ngrok_process.terminate()
        # Turn off this tunnel and clear all tunnels
        ngrok.disconnect(ngrok_url)
        ngrok.kill()
