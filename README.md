# fortanix-demo
A quick demo of the Fortanix sdkms/API. Tested on Raspbian but should work on any Linux distro.
## Requirements:
On the Linux host you're running this from you need to install:
- make
- docker

In Fortanix DMS you need to create:
- An application for REST API access.
- An RSA key for signing (with sign and verify operations enabled.)
- An RSA key for encryption (with encrypt and decrypt operations enabled.)
## Instructions:
1. Copy the example config to 'config.ini':
```bash
cp config.ini.example config.ini
```
Use the text editor of your choice to fill in the UUIDs for the keys you created and the API key.
2. Build the docker image:
```bash
make build
```
3. Run the program:
```bash
make run
```

## Results:
The output for a sucessful run will resemble this:
```
➜  fortanix-demo git:(main) ✗ make run          
docker run -v /home/dan/workDir/fortanix-demo:/home/dan/workDir/fortanix-demo -w /home/dan/workDir/fortanix-demo \
        --user 1000 \
        danielsteinke/fortanix-demo make python-run
python ./main.py
String to encrypt:
        Hello world!


Our encrypted and signed message is: 
kotZqD+7y9/w8WvGvnhmj65q4kLZutaHGfp/cxtmqBlDsPM+O1p1qhwe4/6fHmaqfq/YTStdXMzOoNQirUBV3VwL6IuHWqi0AMGa/oe/lAVWoNRZQfWqIEl30X/RFTwmRlOa9POywZERfhLVMJ1B5BSrbrmsmjt1vYxkQeNYqJbnLFxadQCtUf6rhY/d2WOuop9SUC+bymEXIcUg046Vlt9+KvnVSyxvPeR7rpwAytFKIzNg0iQh6hg3touZU+piReh2LQKcJMdLagxznS8ll8y+AJr8URMdXOzICA2LKnnNbVNnRxrEC+2eYgyojHlGgQSISubM2c/HNQr82MEZqQ==:HqJpbYCbvy2TOxYwDUAd+80rhH4ZsBZCwuFldyF6KKy00geI+GoQktT0rx67hIkRMDQKHtrXy1FcoySXVZvOiqYWQHpRg042P4G+XyO6TQXuEQ9qLbsKM5jNaGpggg3NmzLl4OQMkns46RjIqvL9XY1QZ2bDFXNbqIpWBMbwuB0BqlEveLjH/FnDtMKZXYGOTGNr9j/EegkupTaJEjDM+RKq+ZuAHFIU8J+JSznIv/0htcPWwPbYBT5B1qUwX+1zWGN3kZMz3+cTBbUBY4SNFA49XDi9xKmlAlnEzV2MqLwoeeMWbw2uNaq8JvXR/ICVlGryA7Hy0Q4GYQPql8rtog==


Decreypted string: 
        Hello world!


Successfully validated the signature
```
