print("🚀 Bot is starting...")

from solana_client import load_wallet, get_balance
from raydium import (
    get_mock_raydium_pools,
    get_sol_usdc_pool_balances,
    get_lp_token_supply
)

def main():
    try:
        print("🔑 Loading wallet...")
        wallet = load_wallet()
        address = wallet.pubkey()
        print(f"📬 Wallet Address: {address}")

        print("🔎 Checking balance...")
        balance = get_balance(address)
        print(f"💰 Balance: {balance:.4f} SOL")

        print("\n📊 Raydium Pools (Mock):")
        pools = get_mock_raydium_pools()
        for pool in pools:
            print(f" - {pool['name']}: TVL ${pool['tvl']:,}, Volume ${pool['volume_24h']:,}, APR {pool['fee_apr']}%")

        print("\n📡 Real Raydium Pool Balances (SOL/USDC):")
        balances = get_sol_usdc_pool_balances()

        if isinstance(balances, dict):
            sol = balances.get("SOL")
            usdc = balances.get("USDC")

            if isinstance(sol, float) and isinstance(usdc, float):
                print(f" - SOL Vault:  {sol:.6f} SOL")
                print(f" - USDC Vault: {usdc:.2f} USDC")
            else:
                print("❌ Error retrieving token values:")
                print(f"  - SOL: {sol}")
                print(f"  - USDC: {usdc}")
        else:
            print("❌ Error retrieving balances:", balances)

        print("\n💧 LP Token Supply (SOL/USDC):")
        lp = get_lp_token_supply()

        if isinstance(lp, dict):
            print(f" - Total Supply: {lp['supply']:.6f} LP tokens")
            print(f" - Raw Amount:   {lp['raw']}")
            print(f" - Decimals:     {lp['decimals']}")
        else:
            print(lp)

    except Exception as e:
        print("❌ Error occurred:", e)

if __name__ == "__main__":
    main()

from solana.rpc.api import Client
client = Client("https://api.mainnet-beta.solana.com")

from solders.pubkey import Pubkey
resp = client.get_token_account_balance(Pubkey.from_string("GJwrRkg3uwhsQvcHfQvSk4xeRpoEKwqxuGg6rGD2qTq6"))

print("\n🔍 Direct vault balance test:")
print(resp)





