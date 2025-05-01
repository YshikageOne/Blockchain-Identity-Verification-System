import json
import base64

#For RSA Encryption
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256 #hash function

#cryptographic identity manager
class IdentityManager:
    #create a public and private key
    #encodes them in base64
    @staticmethod
    def generate_key_pair():
        key = RSA.generate(2048) #2048 bit key size
        private_key = key.export_key()
        public_key = key.public_key().export_key()

        private_keyString = base64.b64encode(private_key).decode('utf-8')
        public_keyString = base64.b64encode(public_key).decode('utf-8')

        return private_keyString, public_keyString

    #signs a given data with a private key
    #data hashed with sha256
    @staticmethod
    def sign_data(data, private_keyString):
        if isinstance(data, dict):
            data = json.dumps(data, sort_keys = True)

        private_key = RSA.import_key(base64.b64decode(private_keyString))

        hash = SHA256.new(data.encode('utf-8'))
        signature = pkcs1_15.new(private_key).sign(hash)

        return base64.b64encode(signature).decode('utf-8')


    #verify the signature of the data with a public key
    @staticmethod
    def verify_signature(data, signatureString, public_keyString):
        try:
            if isinstance(data, dict):
                data = json.dumps(data, sort_keys = True)

            public_key = RSA.import_key(base64.b64decode(public_keyString))
            signature = base64.b64decode(signatureString)

            hash = SHA256.new(data.encode('utf-8'))
            pkcs1_15.new(public_key).verify(hash, signature)
            return True

        except(ValueError, TypeError):
            return False