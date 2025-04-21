import argparse
import uvicorn
from fastapi import FastAPI
from flask import Flask

# --------------------
# FastAPI application definition
fastapi_app = FastAPI()


@fastapi_app.get("/")
def read_root():
    return {"message": ">>> Hello from FastAPI!"}


# --------------------
# Flask application definition
flask_app = Flask(__name__)


@flask_app.route("/")
def hello():
    return {"message": ">>> Hello from Flask!"}


# --------------------
# Ngrok startup tool
def start_ngrok(port: int):
    try:
        from pyngrok import ngrok
    except ImportError:
        raise RuntimeError(">>> Please install pyngrok first: pip install pyngrok")

    public_url = ngrok.connect((port))
    print(f">>> Ngrok tunnel opened: {public_url}")


# --------------------
# Main process: Execute according to parameter selection mode
def run(mode: str, use_ngrok: bool):
    if mode == "python":
        print(">>> Hello from plain Python script!")
        print(">>> You can add your own code here.")
    elif mode == "fastapi":
        port = 8000
        if use_ngrok:
            start_ngrok(port)
        print(f">>> Starting FastAPI app on port {port}...")
        uvicorn.run(f"{__name__}:fastapi_app", host="127.0.0.1", port=port)
    elif mode == "flask":
        port = 5000
        if use_ngrok:
            start_ngrok(port)
        print(f">>> Starting Flask app on port {port}...")
        flask_app.run(host="127.0.0.1", port=port)
    else:
        print(f">>> Unknown mode: {mode}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run demo script with different modes."
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["python", "fastapi", "flask"],
        default="python",
        help="Script mode: python, fastapi, flask",
    )
    parser.add_argument(
        "--ngrok", action="store_true", help="Use ngrok to expose the server"
    )
    args = parser.parse_args()

    run(args.mode, args.ngrok)
