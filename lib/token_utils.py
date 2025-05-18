import os
from typing import Optional
from lib.path import get_path


def get_hf_token() -> Optional[str]:
    # Get ".token" file
    fil_token = get_path(key="TOKEN")

    # Get HuggingFace token
    if os.path.exists(fil_token):
        with open(fil_token, "r") as file:
            for line in file:
                # Parse format "key=value"
                key, _, value = line.partition("=")
                if key.strip() == "HUGGINGFACE_TOKEN":
                    hf_token = value.strip()
                    command = f"export HUGGINGFACE_TOKEN={hf_token}"
                    os.system(command)
                    break
            return ">>> HuggingFace token applied."
    return None


def get_line_access() -> Optional[str]:
    # Get ".token" file
    fil_token = get_path(key="TOKEN")

    # Get Line Access
    if os.path.exists(fil_token):
        line_access = None
        with open(fil_token, "r") as file:
            for line in file:
                # Parse format "key=value"
                key, _, value = line.partition("=")
                if key.strip() == "LINE_CHANNEL_ACCESS_TOKEN":
                    line_access = value.strip()
                    break
            return line_access
    return None


def get_line_secret() -> Optional[str]:
    # Get ".token" file
    fil_token = get_path(key="TOKEN")

    # Get Line Secret
    if os.path.exists(fil_token):
        line_secret = None
        with open(fil_token, "r") as file:
            for line in file:
                # Parse format "key=value"
                key, _, value = line.partition("=")
                if key.strip() == "LINE_CHANNEL_SECRET":
                    line_secret = value.strip()
                    break
            return line_secret
    return None
