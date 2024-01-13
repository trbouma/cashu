from importlib import reload
from cashu.wallet.wallet import Wallet as Wallet
from cashu.wallet.cli.cli_helpers import get_mint_wallet, print_mint_balances, verify_mint
import asyncio

from cashu.core.migrations import migrate_databases
from cashu.wallet import migrations


from cashu.wallet.helpers import (
    deserialize_token_from_string,
    init_wallet,
    list_mints,
    receive,
    send,
)

# mint = "https://mint.asats.io"
mint = "http://127.0.0.1:3338"
# mint = "https://8333.space:8333"
# mint = "https://testnut.cashu.space"

# wallet_db = 'postgres://postgres:password@beelink:6432/testwallet'
wallet_db = 'sqlite:///data/wallet.sqlite3.db'
amount = 1
description = 'test'

wallet = Wallet(mint, wallet_db)
asyncio.run(migrate_databases(wallet.db, migrations))
# asyncio.run(wallet._init_private_key())
# asyncio.run(wallet.load_proofs())
# asyncio.run(wallet.load_mint())


mode = input("enter mode:")

if mode =="i":
    invoice = asyncio.run(wallet.request_mint(amount))
    print("invoice:", invoice.bolt11 )
    print("----")
    print("id: ", invoice.id)
    paid = input("have you paid yet?")
    if paid =='y':
        asyncio.run(wallet.mint(amount, id=invoice.id))
        print("balance:", wallet.balance_per_keyset())
        print(wallet.available_balance)

elif mode =="q":
    exit()

elif mode =="p":
    quote_id = input("Enter quote id:")
    asyncio.run(wallet.mint(amount, id=quote_id))
    print("balance:", wallet.balance_per_keyset())
    print(wallet.balance)
    # print(wallet.keyset_id)

elif mode == "b":
    print("balance:", wallet.balance_per_keyset())
    print(wallet.balance)


    







