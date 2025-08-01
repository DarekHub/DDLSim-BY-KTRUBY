
#!/bin/bash
# =================================================================
# # SCRIPT DE CONFIGURATION POUR LE PROJET IDRAK-FUSION         #
# # PHASE 2 : PILE LOGICIELLE                                   #
# =================================================================

# --- PARTIE 1 : MISE À JOUR DU SYSTÈME ET INSTALLATION DE DOCKER ---
echo " Mise à jour du système..."
sudo apt-get update && sudo apt-get upgrade -y

echo " Installation des dépendances pour Docker..."
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

echo " Ajout de la clé GPG officielle de Docker..."
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo " Ajout du référentiel Docker..."
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo " Installation de Docker Engine..."
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# --- PARTIE 2 : INSTALLATION DE NVIDIA CONTAINER TOOLKIT ---
echo " Installation de NVIDIA Container Toolkit..."
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list > /dev/null
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

echo " Configuration du runtime NVIDIA avec Docker..."
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# --- PARTIE 3 : INSTALLATION D'OLLAMA ---
echo " Installation d'Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

echo " Terminé ! Le serveur est prêt pour la phase suivante."

