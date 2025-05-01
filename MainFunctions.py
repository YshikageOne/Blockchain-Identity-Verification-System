from Blockchain import *
from IdentityManager import *
from datetime import datetime
import time
import uuid

#Main System
class IdentityVerificationSystem:
    def __init__(self):
        self.blockchain = Blockchain()
        self.identity_manager = IdentityManager()

    #register a new user by generating a key pair(private and public key)
    #and adding it to the blockchain
    def register_user(self, user_data):
        try:
            private_key, public_key = self.identity_manager.generate_key_pair()

            identity_data = user_data.copy()
            identity_data["public_key"] = public_key
            identity_data["registration_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            identity_id = self.blockchain.register_identity(identity_data)

            result = {
                "success": True,
                "identity_id": identity_id,
                "private_key": private_key,
                "public_key": public_key,
                "message": "Identity has registered successfully"
            }

            return True, result

        except Exception as e:
            return False, {"error": str(e)}

    #verifying the user identity by checking the blockchain
    def verify_user(self, identity_id, challenge_response = None):
        try:
            isFound, identity_data = self.blockchain.verify_identity(identity_id)

            #check if the identity is in the blockchain
            if not isFound:
                return False, {"error": "Identity not found"}

            if challenge_response:
                challenge = challenge_response.get("challenge") #used to prove that someone really is who they say they are
                signature = challenge_response.get("signature") #ensures that the data hasn't been changed and that it really came from an authorized user

                isValid = self.identity_manager.verify_signature(
                    challenge,
                    signature,
                    identity_data["public_key"]
                )

                if not isValid:
                    return False, {"error": "Identity verification failed - invalid signature"}

            result = identity_data.copy()
            result.pop("public_key", None)

            return True, {
                "success": True,
                "identity_verified": True,
                "identity_data": result
            }

        except Exception as e:
            return False, {"error": str(e)}

    #generate a random UUID to be used for verification
    def generate_challenge(self):
        return str(uuid.uuid4())

    #create identity proof that can be verified by others
    def create_identity_proof(self, identity_id, private_key, custom_data = None):

        timestamp = time.time()

        proof_data = {
            "identity_id": identity_id,
            "timestamp": timestamp,
            "expiration":timestamp + 3600,
        }

        if custom_data:
            proof_data["custom_data"] = custom_data

        signature = self.identity_manager.sign_data(proof_data, private_key)

        proof = {
            "data": proof_data,
            "signature": signature
        }

        return proof

    #verify an identity proof
    def verify_identity_proof(self, proof):
        try:
            proof_data = proof["data"]
            signature = proof["signature"]

            identity_id = proof_data["identity_id"]

            if proof_data["expiration"] < time.time(): #check if the proof is expired or not
                return False, {"error": "Proof has expired"}

            isFound, identity_data = self.blockchain.verify_identity(identity_id)

            if not isFound:
                return False, {"error": "Identity not found"}

            isValid = self.identity_manager.verify_signature(
                proof_data,
                signature,
                identity_data["public_key"]
            )

            if not isValid:
                return False, {"error": "Invalid signature"}

            return True,{
                "valid": True,
                "identity_data": identity_data
            }

        except Exception as e:
            return False, {"error": str(e)}