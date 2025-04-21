from solana.rpc.api import Client
from solders.pubkey import Pubkey
import base64

# Use your Alchemy RPC
client = Client("https://solana-mainnet.g.alchemy.com/v2/KTVIX29yZflIqqXcvwffRCeOcHuklp54")

# Raydium AMM ID for SOL/USDC
amm_pubkey = Pubkey.from_string("7gfhm6Ftz5FkUVrZJJWELPffK2DYPxXZTb43HvRacGKF")

account_info = client.get_account_info(amm_pubkey)

if account_info.value and isinstance(account_info.value.data, tuple):
    raw_bytes = base64.b64decode(account_info.value.data[0])

    lp_mint = Pubkey.from_bytes(raw_bytes[72:104])
    vault_a = Pubkey.from_bytes(raw_bytes[104:136])
    vault_b = Pubkey.from_bytes(raw_bytes[136:168])

    print("\n✅ Decoded Raydium Pool Info:")
    print(f" - AMM ID:       {amm_pubkey}")
    print(f" - LP Mint:      {lp_mint}")
    print(f" - Vault A (SOL):  {vault_a}")
    print(f" - Vault B (USDC): {vault_b}")
else:
    print("❌ Failed to decode AMM account.")
