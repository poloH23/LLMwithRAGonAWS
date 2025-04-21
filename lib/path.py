import os
import sys
from pathlib import Path
from dotenv import load_dotenv


def get_root() -> None:
    """
    Set the root directory of the project.
    Usage in Python script:
    get_root()
    root = os.environ['PROJECT_ROOT']
    :return:None
    """
    # Allow to use the ".env" file
    load_dotenv()

    abs_path = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.dirname(abs_path)
    os.environ["PROJECT_ROOT"] = project_root
    return None


def get_module() -> None:
    # Get the project root
    get_root()

    # get and set the environment variables
    python_path = os.environ.get("PYTHONPATH")
    if python_path:
        for path in python_path.split(":"):
            path = str(os.environ["PROJECT_ROOT"]) + path
            if path not in sys.path:
                sys.path.append(path)
    return None


def get_path(key: str) -> str:
    # Load modules and the project root
    get_root()
    PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT"))

    val = os.getenv(key)
    if val:
        path_result = os.path.join(PROJECT_ROOT, val.lstrip("/"))
        return path_result
    else:
        raise ValueError(f">>> Environment variable {key} doesn't exist!")


def check_all_path(*env_vars) -> None:
    for var in env_vars:
        path = get_path(var)
        if not os.path.exists(path):
            raise FileExistsError(f">>> File doesn't exist: {path}")
        else:
            print(f">>> File exists: {path}")
    return None
