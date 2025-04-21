import json
import base64
import struct
from solders.pubkey import Pubkey as PublicKey
from solana.rpc.api import Client
from pathlib import Path

client = Client("https://solana-mainnet.g.alchemy.com/v2/KTVIX29yZflIqqXcvwffRCeOcHuklp54")  # Replace with your RPC if needed

def load_verified_pools():
    path = Path(__file__).parent / "raydium_pools.json"
    with open(path, "r") as f:
        return json.load(f)

def get_mock_raydium_pools():
    return [
        {"name": "SOL/USDC", "tvl": 32000000, "volume_24h": 8000000, "fee_apr": 18.2},
        {"name": "RAY/SOL", "tvl": 5500000, "volume_24h": 1200000, "fee_apr": 9.6},
        {"name": "BONK/USDC", "tvl": 230000, "volume_24h": 72000, "fee_apr": 34.4},
    ]

def fetch_token_balance_from_account_info(account_pubkey: str, decimals: int):
    try:
        pubkey = PublicKey.from_string(account_pubkey)
        response = client.get_account_info(pubkey)

        if response.value is None:
            return f"❌ Error: account {account_pubkey} not found"

        base64_data = response.value.data

        if not base64_data or not isinstance(base64_data[0], str):
            return f"❌ Error: account {account_pubkey} has no base64-encoded data"

        raw_bytes = base64.b64decode(base64_data[0])
        amount_bytes = raw_bytes[64:72]
        amount = struct.unpack("<Q", amount_bytes)[0]
        return amount / (10 ** decimals)

    except Exception as e:
        return f"❌ Error: {e}"

def get_sol_usdc_pool_balances():
    print("📡 Fetching SOL/USDC vault balances...")

    pools = load_verified_pools()
    pool = next((p for p in pools if p["name"] == "SOL/USDC"), None)

    if not pool:
        return "❌ Pool not found in JSON."

    sol = fetch_token_balance_from_account_info(pool["tokenVaultA"], pool["decimalsA"])
    usdc = fetch_token_balance_from_account_info(pool["tokenVaultB"], pool["decimalsB"])

    return {
        "SOL": sol,
        "USDC": usdc
    }

def get_lp_token_supply():
    print("🔍 Fetching LP token supply...")

    try:
        pools = load_verified_pools()
        pool = next((p for p in pools if p["name"] == "SOL/USDC"), None)

        if not pool:
            return "❌ LP mint not found."

        mint_pubkey = PublicKey.from_string(pool["lpMint"])
        resp = client.get_token_supply(mint_pubkey)
        supply_raw = int(resp.value.amount)
        decimals = resp.value.decimals
        supply = supply_raw / (10 ** decimals)

        return {
            "supply": supply,
            "decimals": decimals,
            "raw": supply_raw
        }

    except Exception as e:
        return f"❌ Error: {e}"

