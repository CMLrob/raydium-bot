import os
import json
from dotenv import load_dotenv
from solders.keypair import Keypair
from solana.rpc.api import Client

load_dotenv()

client = Client("https://api.mainnet-beta.solana.com")

def load_wallet():
    print("🔑 Loading wallet...")
    secret = json.loads(os.getenv("PRIVATE_KEY"))
    return Keypair.from_bytes(bytes(secret))

def get_balance(pubkey):
    print("🔎 Checking balance...")
    response = client.get_balance(pubkey)
    return response.value / 1e9  # Convert lamports to SOL



