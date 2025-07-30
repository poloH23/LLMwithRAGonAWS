import requests


def update_line_webhook(public_url: str, access_token: str):
    api_url = "https://api.line.me/v2/bot/channel/webhook/endpoint"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    full_url = public_url.rstrip("/") + "/callback"
    print(f">>> Try to update webhook to: {full_url}")
    payload = {"endpoint": full_url}
    response = requests.put(api_url, headers=headers, json=payload)
    print(f">>> LINE Webhook Update Status: {response.status_code} - {response.text}")
