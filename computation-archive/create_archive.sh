#cd src
zip -r archive.zip src/*
#mv archive.zip ./archive.zip
#cd ..
curl -F "data=@./archive.zip" https://ipfs.infura.io:5001/api/v0/add
