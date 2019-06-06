#!/bin/bash

Write-Output "---------------------------------"
Write-Output "|  Removing Hornet Container    |"
Write-Output "---------------------------------"

Write-Output "[-] Removing Container"
docker.exe stop hornet
docker.exe rm hornet

Write-Output "[*] Cleanup finished"
