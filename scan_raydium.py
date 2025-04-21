from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solana.rpc.types import DataSliceOpts

RAYDIUM_PROGRAM = Pubkey.from_string("RVKd61ztZW9k39u9wUTiBsuoF1oHkYV7S2ZPphW6yTq")
client = Client("https://solana-mainnet.g.alchemy.com/v2/KTVIX29yZflIqqXcvwffRCeOcHuklp54")  # or your own

print("🔍 Scanning Raydium AMM program for live accounts...")

accounts = client.get_program_accounts(
    RAYDIUM_PROGRAM,
    encoding="base64",
    data_slice=DataSliceOpts(offset=0, length=0),
    commitment="confirmed"
)

if accounts.value:
    print(f"\n✅ Found {len(accounts.value)} accounts owned by Raydium")
    print("🧪 Showing first 10 AMM pool account addresses:\n")
    for entry in accounts.value[:10]:
        print(" -", str(entry.pubkey))
else:
    print("❌ No accounts found.")

