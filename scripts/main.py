import time
from pyngrok import ngrok
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    Configuration,
    ApiClient,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from lib.ngrok import start_ngrok
from lib.token_utils import TokenManager

# Add HuggingFace token
tm = TokenManager()
hf_token = tm.get_hf_token()
print(hf_token if hf_token is not None else ">>> HuggingFace token NOT found.")

# Line bot deployment
LINE_CHANNEL_ACCESS_TOKEN = tm.get_line_access()
LINE_CHANNEL_SECRET = tm.get_line_secret()
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
messaging_api = MessagingApi(ApiClient(configuration))
handler = WebhookHandler(channel_secret=LINE_CHANNEL_SECRET)

# Flask application
app = Flask(__name__)

# Model test; Warm up the model before the first request is received.
# time_s = time.time()
# print(">>> Model warm-up...")
# str_test = response_with_judgement("民法第184條的內容是什麼？")
# print(f">>> Model test: {str_test}")
# print(f">>> Model warm-up took {round((time.time()-time_s),2)} seconds.")


# Line webhook root; Define Flask's HTTP routing and map Line's POST request to the callback function
@app.route("/", methods=["POST"])
# Line Webhook router receives webhook requests from the Line platform
def callback():
    # Verify the Line signature to confirm that the request was sent by the Line server
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        # Send the request content to the handler for processing
        handler.handle(body, signature)
    except Exception as e:
        # If authentication fails, an HTTP 400 error is returned.
        print(f">>> [Webhook] Webhook handler error: {str(e)}")
        abort(400)
    return ">>> [Webhook] Webhook processed successfully."


@handler.add(MessageEvent)
# Even handling
def handle_message(event):
    try:
        if isinstance(event.message, TextMessageContent):
            # Timing start
            time_s = time.time()

            # Receive user messages
            user_message = event.message.text
            print(">>> Successfully received user message")

            # Llama generates answers
            # response = response_with_judgement(user_message)
            response = f"Test: receiving user message: {user_message}"

            # Return answers to Line users
            messaging_api.reply_message(
                ReplyMessageRequest(
                    replyToken=event.reply_token, messages=[TextMessage(text=response)]
                )
            )
            print(f">>> Processing time: {round((time.time() - time_s), 2)} seconds")
        else:
            print(
                f">>> Received user message is not a TextMessage: {type(event.message)}"
            )
    except Exception as e:
        print(f">>> An error occurred during processing: {str(e)}")


if __name__ == "__main__":
    ngrok_url = start_ngrok(port=5000)
    try:
        app.run(host="0.0.0.0", port=5000, debug=False)
    except KeyboardInterrupt:
        print(">>> Terminating Flask and Ngrok...")
        ngrok.disconnect(ngrok_url)
        ngrok.kill()
