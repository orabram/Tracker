import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast
import pickle

ENCRYPTION_NUMBER = 32

class RSAEncryption():
    def __init__(self):
        self.keys = {}
        try:
            self.keys_file = open("keys.dat", 'rb+')
            self.keys = pickle.load(self.keys_file)
        except:
            self.keys_file = open("keys.dat", "wb+")

    def generate_keys(self):
        random_generator = Random.new().read
        key = RSA.generate(1024, random_generator) #generate pub and priv key
        return key

    def generate_pub_key(self):
        key = self.generate_keys()
        publickey = key.publickey() # pub key export for exchange
        return publickey

    def get_pub_key(self, key):
        publickey = key.publickey() # pub key export for exchange
        return publickey

    def encrypt_message(self, pubkey, message):
        encrypted = pubkey.encrypt(message, ENCRYPTION_NUMBER)
        print encrypted
        return encrypted

    def decrypt_message(self, key, message):
        decrypted = key.decrypt(ast.literal_eval(str(message)))
        return decrypted

    def create_key_pair(self, filename, key):
        self.keys[filename] = key

    def get_key(self, filename):
        return self.keys[filename]