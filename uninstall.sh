#!/bin/bash

echo "---------------------------------"
echo "|  Removing Hornet Container    |"
echo "---------------------------------"

echo "[-] Removing Container"
docker stop hornet && docker rm hornet || true

echo "[*] Cleanup finished"
