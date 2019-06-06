Write-Output "---------------------------------"
Write-Output "|      Installing Hornet        |"
Write-Output "---------------------------------"


Write-Output "[-] Cleaning up environment"
docker.exe stop hornet
docker.exe rm hornet

Write-Output "[+] Building Container"
docker.exe build -t hornetsrv:v1 .

Write-Output "[+] Running Container"
docker.exe run -d -it -p 1337:80 -p 8080:8080 --name=hornet hornetsrv:v1 

Write-Output "[*] Setup complete"
docker.exe ps

Write-Output "[*] Access webinterface under http://localhost:1337"