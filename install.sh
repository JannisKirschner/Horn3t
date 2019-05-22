#!/bin/bash
echo "---------------------------------"
echo "|      Installing Hornet        |"
echo "---------------------------------"


echo "[-] Cleaning up environment"
docker stop hornet && docker rm hornet || true

echo "[+] Building Container"
docker build -t hornetsrv:v1 .

echo "[+] Running Container"
docker run -d -it -p 1337:80 -p 8080:8080 --name=hornet hornetsrv:v1 

echo "[*] Setup complete"
docker ps

echo "[*] Access webinterface under http://localhost:1337"