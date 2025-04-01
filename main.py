import sdkms.v1
import base64
import configparser

##Create our message to sign and encrypt
data = 'Hello world!'
print(f"String to encrypt:\r\n\t{data}")

##Use configparser to load our config file
config_parser=configparser.ConfigParser()
config_parser.read('./config.ini')
##Define the keys we will be using
signing_key_uuid=config_parser['KEYCONFIG']['signing_key_uuid']
encryption_key_uuid=config_parser['KEYCONFIG']['encryption_key_uuid']

##Set up our sdkms config, client and authorization
config = sdkms.v1.Configuration()
config.host = config_parser['APICONFIG']['api_host']
config.app_api_key = config_parser['APICONFIG']['app_api_key']
client = sdkms.v1.ApiClient(configuration=config)
auth_instance = sdkms.v1.AuthenticationApi(api_client=client)
auth = auth_instance.authorize()
config.api_key['Authorization'] = auth.access_token
config.api_key_prefix['Authorization'] = 'Bearer'

##Create our API instances
sign_api_instance = sdkms.v1.SignAndVerifyApi (api_client=client)
encrypt_api_instance = sdkms.v1.EncryptionAndDecryptionApi(api_client=client)

##Sign the message
sign_request = sdkms.v1.SignRequest(hash_alg= sdkms.v1.DigestAlgorithm.SHA256, data=bytearray(data.encode()))
sign_response = sign_api_instance.sign(signing_key_uuid, sign_request)

##Encrypt the message
encrypt_request = sdkms.v1.EncryptRequest(
           alg=sdkms.v1.ObjectType.RSA,
           plain=bytearray(data.encode()),
           mode="OAEP_MGF1_SHA1")
encrypt_response = encrypt_api_instance.encrypt(encryption_key_uuid, encrypt_request)

##Encode our encrypted message and signature in base64 so we can transmit it using
##a common protocol like HTTP or SMTP.
cipher_b64 = base64.b64encode(encrypt_response.cipher).decode()
signature_b64 = base64.b64encode(sign_response.signature).decode()

##Format the cipher and signature per requirements. 
b64_cipher_signature = f"{cipher_b64}:{signature_b64}"

print("\r\n")
print(f"Our base64 encrypted and signed message is: \r\n{b64_cipher_signature}")

##Now split the cipher and signature back out:
encrypted_message_array = b64_cipher_signature.split(':')
##Decode from base64 back to byte array
cipher_bytearray = bytearray(base64.b64decode(encrypted_message_array[0]))
signature_bytearray = bytearray(base64.b64decode(encrypted_message_array[1]))

##Now use our existing API instance to decrypt the message:
decrypt_request = sdkms.v1.DecryptRequest( alg=sdkms.v1.ObjectType.RSA,cipher=cipher_bytearray,mode='OAEP_MGF1_SHA1')
decrypt_response = encrypt_api_instance.decrypt(encryption_key_uuid, decrypt_request)
decrypted_string = decrypt_response.plain.decode()

##Now use our existing API instance to verify the signature:
verify_request = sdkms.v1.VerifyRequest(hash_alg=sdkms.v1.DigestAlgorithm.SHA256, data=decrypt_response.plain, signature=signature_bytearray)
verify_response = sign_api_instance.verify(signing_key_uuid, verify_request)

print("\r\n")
print(f"Decreypted string: \r\n\t{decrypted_string}")
print("\r\n")
if verify_response.result:
    print('Successfully validated the signature')
