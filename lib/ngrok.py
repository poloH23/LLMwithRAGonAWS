from pyngrok import ngrok


def start_ngrok(port=5000):
    try:
        # Open Http tunnel
        public_url = ngrok.connect(port, "http")
        print(f">>> Ngrok public URL: {public_url}")
        return public_url
    except Exception as e:
        print(f">>> Ngrok exception: {e}")
        return None
