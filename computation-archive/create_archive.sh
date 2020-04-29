zip -r archive.zip src/*
curl -F "data=@./archive.zip" https://ipfs.infura.io:5001/api/v0/add
