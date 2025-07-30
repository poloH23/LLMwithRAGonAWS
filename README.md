# 📌 Project Name

This project builds a Line chatbot that provides legal information based on Taiwan-Law-LLaMA, a large language model fine-tuned on Taiwanese legal texts. The system integrates a Retrieval-Augmented Generation (RAG) pipeline to enhance factual accuracy and contextual relevance.

It is designed for deployment on AWS EC2 and supports scalable backend services via FastAPI, document indexing with FAISS, and a custom Line bot interface.

---

## 📝 Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
  - [Clone the Repository](#-clone-the-repository)
  - [Conda Environment Setup](#-conda-environment-setup)
  - [Docker Setup](#-docker-setup-directly)
- [Usage](#-usage)
  - [Built-in Demo Runner](#-built-in-demo-runner)
  - [Tests](#-tests)
- [CI/CD Pipeline with GitHub Actions](#-cicd-pipeline-with-gitHub-actions)
- [Quick Start](#-quick-start)
- [Folder Structure](#-folder-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- 🔍 RAG Integration: Combines Taiwan-Law-LLaMA with a vector store for legal document retrieval.
- 💬 Line Chatbot: Interactive legal Q&A through the Line Messaging API.
- 🚀 AWS Deployment: Easily deployable on EC2 instances with Docker support.
- ⚖️ Legal Domain Focus: Optimized for civil and administrative law queries in Taiwan.

---

## 📋 Requirements

- Python 3.9+
- Conda (Anaconda or Miniconda)
- GNU Make (default on Linux/macOS, optional on Windows)
- Git (optional)
- Docker (optional)

*Python package dependencies are listed in [`requirements.txt`](./requirements.txt).*

---

## 💻 Installation

### 📥 Clone the Repository

```bash
git clone https://github.com/poloH23/[your-repo].git
cd [your-repo]
```

### 🐍 Conda Environment Setup

* Create a conda environment using the development packages (Recommended):
```bash
make conda-dev
```

* Create and activate a new conda environment:
```bash
# Create a new environment and install Git pre-commit hook
make conda-custom ENV=myenv
make init-hooks
```

---

### 🐳 Docker Setup Directly

1. Build the Docker image:
```bash
docker build -t your-project-name .
```

2. Run the container:
```bash
docker run -p 8000:8000 your-project-name
```

3. (Optional) Use Docker Compose:
```bash
docker-compose up --build
```

---

## 🚀 Usage

### 🧪 Built-in Demo Runner

* This project includes a demo script that can run in different modes:

```bash
make run-demo MODE=python
make run-demo MODE=fastapi
make run-demo MODE=fastapi NGROK=1
make run-demo MODE=flask
make run-demo MODE=flask NGROK=1
```

* Supported modes:
  * **python**: Run a plain Python CLI demo
  * **fastapi**: Run FastAPI app on port 8000
  * **flask**: Run Flask app on port 5000
  * Add **NGROK=1** to expose the app via ngrok

*Source: `scripts/main_demo.py`*

### 🧪 Tests

* This template includes a basic test file `tests/test_demo.py`:

```bash
make test
```

*You can extend this file to add unit tests for your own modules.*

### ✅ CI/CD Pipeline with GitHub Actions

* This project includes a minimal and efficient CI workflow using GitHub Actions:
  * Python 3.9 setup
  * Installs dependencies from `requirements.txt`
  * Runs `make lint` to check code style using pre-commit hooks
  * Runs `make test` to execute your test suite
  * Runs `make help` to show the instructions
  * To customize the workflow, edit `.github/workflows/python-ci.yml`

*You can monitor the build status in the Actions tab on your GitHub repo.*

---

## 🎥 Quick Start

* 📘 **New here?** Check out our [Quickstart Guide](docs/quickstart.md) to get set up and run your first demo!

---

## 📁 Folder Structure

```text
.
├── bak/                        # Backup files (e.g. environment.yml)
├── data/                       # Raw or processed data
├── docs/                       # Project documentation (incl. quickstart)
├── lib/                        # Utility functions and shared logic
│   ├── config.py
│   ├── path.py
│   └── utils.py
├── logs/, results/, reports/   # Output, logs, and generated reports
├── main                        # Main application code
├── models/                     # Saved models
├── notebooks/                  # Jupyter notebooks (experiments / EDA)
├── scripts/                    # Executable scripts or entry points
│   └── demo/
│       └── main_demo.py        # Demo for Python / FastAPI / Flask modes
├── shell/                      # Bash scripts for setup and utilities
│   ├── gitkeep.sh
│   └── setup_env.sh
├── tests/                      # Unit and integration tests
│   └── test_demo.py
├── Dockerfile
├── Makefile
├── .pre-commit-config.yaml
├── requirements.txt
├── .env, .env.example
├── .gitignore, .dockerignore
└── README.md
```

---

## 📄 License

This project is licensed under the GPL-3.0 License.
