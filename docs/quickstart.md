# 🎥 Quick Project Setup Walkthrough (For New Developers)

Welcome to the **Your Project Name** onboarding tutorial!  
In this short video, you'll learn how to:

- [✅ Clone the project](#-step-1-clone-the-project)
- [⚙️ Create and activate your development environment](#-step-2-set-up-the-conda-environment-and-install-git-hooks)
- [🔧 Format and lint your code](#-step-3-check-and-format-code)
- [🧪 Run tests](#-step-4-run-unit-tests)
- [🚀 Try out demo apps](#-step-5-try-out-demo-apps)
- [☁️ Push and validate with GitHub Actions](#-step-6-push-your-code)

---

## 🛠️ Step 1: Clone the Project

```bash
git clone https://github.com/your-org/your-project.git
cd your-project
```

---

## 🧬 Step 2: Set Up the Conda Environment and Install Git Hooks

1. Build the environment for development

```bash
make conda-dev
conda activate <your-env-name>  # The name is defined in ./bak/environment.yml
```

2. Build the environment by customized environment name (lite version)

```bash
make conda-custom ENV=myenv
```

---

## 🧼 Step 3: Check and Format Code

```bash
make lint     # Run pre-commit checks (black, ruff, gitkeep)
make code-format   # Apply formatting fixes
```

---

## 🧪 Step 4: Run Unit Tests

```bash
make test
```

*Visit the printed URL or localhost port to view your app.*

---

## 🚀 Step 5: Try Out Demo Apps

```bash
make run-demo MODE=python
make run-demo MODE=fastapi NGROK=1
make run-demo MODE=flask
```

---

## ☁️ Step 6: Push Your Code

```bash
git add .
git commit -m "feat: my first commit"
git push origin main
```

*✅ Once pushed, GitHub Actions will automatically run make lint and make test.*

---

## 🎉 Done!
- You’ve now set up your local environment, verified your tools, and tested your project.
- Happy hacking 👨‍💻👩‍💻

---
