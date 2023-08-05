import json
import os
import time

import pgpy
from redis import StrictRedis

from om.utils import config


class Encryption:
    keys = {}
    key_expiration = {}
    key_created = {}
    REDIS_HKEY = "kv"
    REDIS_KEY = "encryption_key"

    def __init__(self):
        self.redis = StrictRedis(host=config.string("REDIS_HOST", "localhost"),
                                 port=config.int("REDIS_PORT", 6379),
                                 db=config.int("REDIS_DB", 0))

    def get_key(self, key_name):
        now = time.time()
        data = self.redis.hget(self.REDIS_HKEY, self.REDIS_KEY)
        if not data:
            return self.keys.get(key_name)

        keys = json.loads(data).get(key_name, {})

        # find last created and not expired key
        # or key with greatest expiration time
        # or stay with current key
        last_created_valid_key_index = None
        latest_expiration_key_index = None
        key_list = list(keys.values())
        for key_index, key in enumerate(key_list):
            if key["created"] > self.key_created.get(key_name, 0) and key["expiration"] > now:
                self.key_created[key_name] = key["created"]
                last_created_valid_key_index = key_index
            elif key["expiration"] > self.key_expiration.get(key_name, 0):
                self.key_expiration[key_name] = key["expiration"]
                latest_expiration_key_index = key_index

        def load_key(new_key):
            self.keys[key_name], _ = pgpy.PGPKey.from_blob(new_key["pubkey"])
            self.key_expiration[key_name] = new_key["expiration"]
            self.key_created[key_name] = new_key["created"]

        if last_created_valid_key_index is not None:
            load_key(key_list[last_created_valid_key_index])
        elif latest_expiration_key_index:
            load_key(key_list[latest_expiration_key_index])
        return self.keys.get(key_name)

    def encrypt_file(self, file_name, out_file_name=None, key_name="default"):
        with open(file_name, "rb") as file:
            compress = True
            ending = file_name.rsplit(".", 1)
            if ending in ["gz", "jpg", "jpeg"]:
                compress = False
            encrypted = self.encrypt_data(file.read(), compress, key_name)
        if encrypted:
            new_name = out_file_name or f"{file_name}.pgp"
            if not new_name.endswith(".pgp"):
                new_name = new_name + ".pgp"
            with open(new_name, "wb") as out:
                out.write(encrypted)
            os.remove(file_name)
            return True
        return False

    def encrypt_data(self, data, compress=True, key_name="default"):
        compression = pgpy.constants.CompressionAlgorithm.ZLIB if compress else \
            pgpy.constants.CompressionAlgorithm.Uncompressed
        key = self.get_key(key_name)
        if not key:
            return None
        encrypted = key.encrypt(pgpy.PGPMessage.new(data), compression=compression)
        return bytes(encrypted)


if __name__ == "__main__":
    text = b"please decrypt me"
    encryption = Encryption()

    encrypted_text = encryption.encrypt_data(text, True)
    if encrypted_text:
        with open("/data/upload/files/test_encryption.txt.pgp", "wb") as outfile:
            outfile.write(encrypted_text)
    else:
        print("ENCRYPTION FAILED")

    with open("/data/test_encryption.txt", "wb") as new_file:
        new_file.write(text)
    encryption.encrypt_file("/data/test_encryption.txt", "/data/upload/files/test_encryption2.txt")
