import os
import ecdsa
import hashlib
import requests

keepalive = True

def generate_wallet():
    # Generate random private key
    private_key = os.urandom(32) 

    # Derive public key from private key 
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    public_key = vk.to_string().hex()

    # Derive wallet address from public key
    address = "0x"+hashlib.sha3_256(hashlib.sha3_256(bytes.fromhex(public_key[2:])).digest()).hexdigest()[24:]

    return address,private_key

def print_result(private_key,address,balance):
    print(f"Private Key: {private_key.hex()}")
    print(f"Wallet Address: {address}")
    print(f"Wallet Balance: {balance}")

def check_balance():
    address, private_key = generate_wallet()
    try:
        response = requests.get("https://api.blockcypher.com/v1/eth/main/addrs/"+address+"/balance")
        response.raise_for_status()
        data = response.json()
        final_balance=data["final_balance"]
        print_result(private_key,address,final_balance)
        print("---------------------")
        if final_balance != 0:
            with open('FoundAddress.txt', 'a') as f:
                f.write("\n",private_key)
                print("0")
    except Exception as e:
        print("Error:Please Check your Network Connection")
        print(e)

while keepalive:
    check_balance()



