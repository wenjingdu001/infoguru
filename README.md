# InfoGuru: RAG + Local LLaMA 3.1:70B Model for Secured Business-Specific Responses

## Overview

InfoGuru is an advanced AI-driven solution designed to provide business-specific responses using Retrieval-Augmented Generation (RAG) and the powerful LLaMA 3.1:70B model. This project leverages state-of-the-art language models and retrieval systems to generate context-aware and precise answers tailored to your business needs.

## Features

- High-Accuracy Responses: Combines retrieval of relevant documents with the generative power of the LLaMA 3.1:70B model to produce highly accurate and contextually appropriate responses.
- Customizable: Tailor the retrieval and generation process to suit your specific business domain.
- Scalable Architecture: Built to handle large-scale queries and retrievals efficiently.
- Dockerized Deployment: Easily deploy InfoGuru in any environment using Docker.

## Prerequisites
Before you begin, ensure you have the following installed:

- WSL (Windows Subsystem for Linux): To use Ubuntu on Windows.
- Docker: To run and manage containers.
- NVIDIA Drivers & CUDA: If you plan to leverage GPU acceleration.

## Setting Up LLM and AI Model Containers on WSL with Docker

This documentation provides step-by-step instructions for setting up a local AI environment on a Windows machine using Windows Subsystem for Linux (WSL) and Docker. The environment will include three Docker containers: one for Open WebUI, one for Ollama, and one for Stable Diffusion, all connected via a custom Docker bridge network.

## 1. Install WSL to Use Ubuntu (Linux) on Windows

### Step 1: Enable WSL
1. Open PowerShell as Administrator and run:

    ```powershell
    wsl --install
    ```
    This command installs WSL along with the default Linux distribution, which is typically Ubuntu. It sets up the necessary components for running Linux on Windows.

1. Restart your computer if prompted.

### Step 2: Install Ubuntu
1. After restarting, open the Microsoft Store and search for "Ubuntu". 
1. Install your preferred version of Ubuntu (e.g., Ubuntu 20.04 LTS).
1. Launch Ubuntu from the Start Menu, and complete the initial setup by creating a username and password.

## 2. Configure Network Settings with Hyper-V Manager

### Step 1: Create a configuration file for WSL
1. Navigate to `C:\Users\<your_username>`.
1. Create a file named `.wslconfig`.
1. Within the file, paste:

    ```
    [wsl2]
    networkingMode=bridged
    vmSwitch=wsl-nic
    ```
    Setting the network mode to bridged ensures that your WSL environment gets an IP address on the same network as your home network. This allows Docker containers to communicate with other devices on your local network.

### Step 2: Change Network Mode
1. In Hyper-V Manager, navigate to `Virtual Switch Manager`.
1. Create a new Virtual Switch with the type **External**, and name it `wsl-nic`.
1. Apply the changes. This ensures that your WSL environment uses an IP address that aligns with your home network.

## 3. Install Docker in Ubuntu
1. Install Docker in your WSL Ubuntu environment.
1. Follow the official guide to install Docker on Ubuntu: [Install Docker on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

## 4. Create a Docker Bridge Network for Containers
1. Open Ubuntu from the start menu
1. Create a Docker bridge network driver called `myllm` to allow communication between three Docker containers: Open WebUI, Ollama, and Stable Diffusion by running the following command:
    ```bash
    sudo docker network create --driver bridge myllm
    ```
    Creating a custom bridge network named myllm allows your containers to communicate with each other while isolating them from other networks. This setup ensures that the containers used for Open WebUI, Ollama, and Stable Diffusion can interact seamlessly.

1. You can view the details of this network by running the following command:
    ```bash
    sudo docker inspect myllm
    ```

## 5. Setup the Ollama Container

### Step 1: Create and Run the Container

Enter the following command in Ubuntu:
```bash
sudo docker run -d --network myllm -v ollama:/root/.ollama -e OLLAMA_KEEP_ALIVE=-1 -p 11434:11434 --restart unless-stopped --gpus all --name ollama ollama/ollama
```
- `-d`: Runs the container in detached mode.
- `--network myllm`: Connects the container to a specific network.
- `-v ollama:/root/.ollama`: Mounts a volume for persistent storage of Ollama data.
- `-e OLLAMA_KEEP_ALIVE=-1`: Sets an environment variable to keep Ollama alive.
- `-p 11434:11434`: Maps the container's port 11434 to the host’s port 11434 for access.
- `--restart unless-stopped`: Ensures the container restarts unless manually stopped.
- `--gpus all`: Grants access to all available GPUs.
- `--name ollama`: Assigns the container a name for easy management.
- `ollama/ollama`: Specifies the Docker image to use.

### Step 2: Pull the Llama3 Model
1. Access the container shell:
    ```bash
    sudo docker exec -it ollama sh
    ```
    This allows you to run commands inside the container environment.
1. Pull the Llama3.1 model:
    ```bash
    ollama pull llama3.1:70b
    ```
    Pulling the Llama3.1 model is necessary for the container to utilize this specific model for its operations. The `llama3.1:70b` model will take 40GB memory. If you prefer something lighter, use `llama3.1:8b` instead which only takes about 5GB.

1. Press `ctrl + d` to exit the container shell.

## 6. Setup the Stable Diffusion Container

### Step 1: Clone the Repository
We will use the AbdBarho's repo for setting up the container of Stable Diffusion.
```bash
git clone https://github.com/AbdBarho/stable-diffusion-webui-docker
```

### Step 2: Modify the Dockerfile
1. Navigate to the Dockerfile:
    ``` bash
    cd stable-diffusion-webui-docker/services/AUTOMATIC1111/
    ```

1. Edit the Dockerfile to add `--api` to `CLI_ARGS`. This step enables API functionality for the Stable Diffusion service, allowing it to interact programmatically.

###  Step 3: Follow Setup Instructions
Follow the setup instructions available at:
[Stable Diffusion WebUI Docker Setup](https://github.com/AbdBarho/stable-diffusion-webui-docker/wiki/Setup)

###  Step 4: Connect the Container to the "myllm" Network
```bash
sudo docker network connect myllm webui-docker
```
Connecting the container to the myllm network allows it to communicate with other containers on the same network, such as Ollama and Open WebUI. 

## 7. Setup the Open WebUI Container
### Step 1: Create and Run the Container
```bash
sudo docker run -d -p 8080:8080 --network myllm -e OLLAMA_BASE_URL=http://ollama:11434 --gpus all -v open-webui:/app/backend/data --name open-webui --restart unless-stopped ghcr.io/open-webui/open-webui:main
```
- `-d`: Runs the container in detached mode.
- `-p 8080:8080`: Maps the container's port 8080 to the host’s port 8080 for access.
- `--network myllm`: Connects the container to the myllm network.
- `-e OLLAMA_BASE_URL=http://ollama:11434`: Sets the environment variable to connect to the Ollama service.
- `--gpus all`: Grants access to all available GPUs.
- `-v open-webui:/app/backend/data`: Mounts a volume for persistent storage of Open WebUI data.
- `--name open-webui`: Assigns the container a name for easy management.
- `--restart unless-stopped`: Ensures the container restarts unless manually stopped.
- `ghcr.io/open-webui/open-webui:main`: Specifies the Docker image to use.

### Step 2: Access Open WebUI 
Open your web browser and go to: `http://<yourIPaddress>:8080`. 

Replace `<yourIPaddress>` with the IP address assigned to your WSL environment, or use `localhost`.