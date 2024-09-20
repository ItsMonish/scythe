from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

class AESModule:
    def __init__(self, keySize: int = 128, key: str = "") -> None:
        if keySize not in [128, 192, 256]:
            raise Exception("Invalid Keysize")
        self.keySize = keySize
        self.toPutKey = False
        if key == "":
            self.key = get_random_bytes(self.keySize // 8)
            self.toPutKey = True
        else:
            self.key = bytes(bytearray.fromhex(key))

    def encrypt(self, con: str) -> str:
        object = AES.new(self.key, AES.MODE_CTR)
        if self.toPutKey:
            self.toPutKey = False
            return (
                self.key.hex() + object.nonce.hex() + object.encrypt(con.encode()).hex()
            )
        return object.encrypt(con.encode()).hex()

    def decrypt(self, con: str) -> str:
        if self.toPutKey:
            self.key = bytes(bytearray.fromhex((con[0 : self.keySize // 4])))
            nonce = bytes(
                bytearray.fromhex((con[self.keySize // 4 : ((self.keySize // 4) + 16)]))
            )
            buf = bytes(bytearray.fromhex(con[(self.keySize // 4) + 16 :]))
        else:
            nonce = bytes(bytearray.fromhex(con[0:16]))
            buf = bytes(bytearray.fromhex(con[16:]))
        object = AES.new(self.key, AES.MODE_CTR, nonce=nonce)
        return object.decrypt(buf).decode()
