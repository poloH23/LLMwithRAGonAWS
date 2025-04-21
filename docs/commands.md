# 🛠 Common Linux/Docker Operation Instructions

---

## 📝 Table of Contents

- [Compress/Uncompress Project](#-compressUncompress-project)
- [Docker Deployment](#-docker-deployment)
- [Conda Environment Setup](#-conda-environment-setup)
- [Install Docker (Ubuntu)](#-install-docker-ubuntu)
  - [OS requirements](#-OS-requirements)
  - [Uninstall old versions](#-uninstall-old-versions)
  - [Install using the apt repository](#-install-using-the-apt-repository)
  - [Uninstall Docker Engine](#-uninstall-docker-engine)

---

## 📦 Compress/Uncompress Project
```bash
# compress the entire directory
zip -r project-template.zip .

# uncompress the zip file
unzip project-template.zip -d project-template
```

---

## 🐋 Docker Deployment
1. Deploy by Docker image
```bash
# Build a Docker image
# Or use: $ docker build -t py-base .
make docker-build

# Export the image into a tar file
docker save -o py-base py-base.tar

# Uploading to EC2 using SCP
scp -i ~/.ssh/your-key.pem py-base.tar ubuntu@your-ec2-ip:/home/ubuntu/

# Importing Docker images on EC2
ssh -i ~/.ssh/your-key.pem ubuntu@your-ec2-ip
docker load < py-base.tar

# Execute the container and start your service
# Or use: $ docker run -it py-base
make docker-run

# Create a new Conda environment (lite)
make conda-custom ENV=myenv
```

2. Deploy by compressed file
```bash
# Compress the project directory
tar -czvf py-base.tar.gz .

# Uploading to EC2 using SCP
scp -i ~/.ssh/your-key.pem py-base.tar.gz ubuntu@your-ec2-ip:/home/ubuntu/

# SSH login to EC2
ssh -i ~/.ssh/your-key.pem ubuntu@your-ec2-ip

# Uncompress tar file and build Docker image
mkdir myproject/
tar -xzvf py-base.tar.gz -C py-base/
cd py-base/

# Build a Docker image
# Or use: $ docker build -t py-base .
make docker-build

# Execute the container and start your service
# Or use: $ docker run -it py-base
make docker-run
```

---

## 🐍 Conda Environment Setup
* After activating the Docker container:
```bash
# Create a new conda environment
# Build lite version (Recommendation)
make conda-custom ENV=myenv

# Build development version
make conda-dev

# Activate conda environment
conda activate myenv
```

---

## 🐳 Install Docker (Ubuntu)

### 💻 OS requirements
* To install Docker Engine, you need the 64-bit version of one of these Ubuntu versions:
  * Ubuntu Oracular 24.10
  * Ubuntu Noble 24.04 (LTS)
  * Ubuntu Jammy 22.04 (LTS)
  * Ubuntu Focal 20.04 (LTS)

### 🧹 Uninstall old versions
* Before you can install Docker Engine, you need to uninstall any conflicting packages.
* The unofficial packages to uninstall are:
  * docker.io
  * docker-compose
  * docker-compose-v2
  * docker-doc
  * podman-docker
* Uninstall command:
```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

### 📦 Install using the apt repository
* Before you install Docker Engine for the first time on a new host machine, you need to set up the Docker apt repository. Afterward, you can install and update Docker from the repository.
1. Set up Docker's `apt` repository.
```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

2. Install the Docker packages.
* Latest
```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
* Specific version
```bash
# To install a specific version of Docker Engine, start by listing the available versions in the repository:
# List the available versions:
apt-cache madison docker-ce | awk '{ print $3 }'

# 5:28.1.1-1~ubuntu.24.04~noble
# 5:28.1.0-1~ubuntu.24.04~noble
# ...

# Select the desired version and install:
VERSION_STRING=5:28.1.1-1~ubuntu.24.04~noble
sudo apt-get install docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin
```

3. Add your user to the docker group.
```bash
sudo usermod -aG docker $USER
```

4. Verify that the installation is successful by running the hello-world image:
```bash
sudo docker run hello-world
```

### ❌ Uninstall Docker Engine
1. Uninstall the Docker Engine, CLI, containerd, and Docker Compose packages:
```bash
sudo apt-get purge docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
```

2. Images, containers, volumes, or custom configuration files on your host aren't automatically removed. To delete all images, containers, and volumes:
```bash
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
```

3. Remove the source list and keyrings
```bash
sudo rm /etc/apt/sources.list.d/docker.list
sudo rm /etc/apt/keyrings/docker.asc
```

* You have to delete any edited configuration files manually.
