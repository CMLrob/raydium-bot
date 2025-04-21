from time import sleep, time
from solana.rpc.api import Client
from solders.pubkey import Pubkey

# Use your Alchemy RPC
client = Client("https://solana-mainnet.g.alchemy.com/v2/KTVIX29yZflIqqXcvwffRCeOcHuklp54")

# Raydium vaults to check (replace if needed)
vault_sol = Pubkey.from_string("2Dg5bpn9GzFo5GL7LDU1AdcEYq9zbs6X4sBbd53W44rZ")
vault_usdc = Pubkey.from_string("GoeR8xVKTcSFnCL5FjzqTSDqQAi4KRZZyRxx73qXTgKZ")

def get_balance(pubkey: Pubkey, label: str):
    try:
        resp = client.get_token_account_balance(pubkey)
        ui_amount = resp.value.ui_amount
        print(f"✅ {label} Balance: {ui_amount}")
    except Exception as e:
        print(f"❌ {label} Error: {e}")

def rate_safe_loop(interval=5):
    print(f"\n⏱️ Starting rate-safe bot loop (~{interval}s between vault sets)\n")
    while True:
        t_start = time()

        get_balance(vault_sol, "SOL Vault")
        sleep(1)  # space out individual calls
        get_balance(vault_usdc, "USDC Vault")

        elapsed = time() - t_start
        print(f"🔁 Waiting for next round (elapsed: {elapsed:.2f}s)\n")
        sleep(max(0, interval - elapsed))

if __name__ == "__main__":
    rate_safe_loop()
