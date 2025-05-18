import os
from typing import Optional
from lib.path import get_path


class TokenManager:
    def __init__(self):
        self.token_path = get_path(key="TOKEN")
        self.tokens = self._load_tokens()

    def _load_tokens(self) -> dict:
        token_dict = {}
        if os.path.exists(self.token_path):
            with open(self.token_path, "r") as file:
                for line in file:
                    key, _, value = line.partition("=")
                    if key and value:
                        token_dict[key.strip()] = value.strip()
        return token_dict

    def get(self, key: str) -> Optional[str]:
        return self.tokens.get(key)

    def get_hf_token(self) -> Optional[str]:
        token = self.get("HUGGINGFACE_TOKEN")
        if token:
            os.environ["HUGGINGFACE_TOKEN"] = token
            return ">>> HuggingFace token applied."
        return None

    def get_line_access(self) -> Optional[str]:
        return self.get("LINE_CHANNEL_ACCESS_TOKEN")

    def get_line_secret(self) -> Optional[str]:
        return self.get("LINE_CHANNEL_SECRET")

    def get_google_api_key(self) -> Optional[str]:
        return self.get("GEMINI_API_KEY")
