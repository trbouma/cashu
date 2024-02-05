from importlib import reload
from cashu.wallet.wallet import Wallet as Wallet
from cashu.wallet.cli.cli_helpers import get_mint_wallet, print_mint_balances, verify_mint
import asyncio
from dotenv import load_dotenv
import os
from cashu.core.base import Proof, DLEQWallet
from cashu.core.migrations import migrate_databases
from cashu.wallet import migrations
import datetime
import requests
from cashu.core.base import TokenV1, TokenV2, TokenV3, TokenV3Token

from cashu.wallet.helpers import (
    deserialize_token_from_string,
    init_wallet,
    list_mints,
    receive,
    send,
)



load_dotenv()




mint = os.getenv('TESTCLIENT_MINT')
wallet_db = os.getenv('TESTCLIENT_WALLET_DB')
print(wallet_db, mint)
amount = 200
description = 'test'




mode = input("enter mode:")

wallet = Wallet(mint, wallet_db)
asyncio.run(migrate_databases(wallet.db, migrations))
asyncio.run(wallet._init_private_key())
asyncio.run(wallet.load_proofs())
asyncio.run(wallet.load_mint())

if mode =="invoice receive":
    amount = int(input("what is the amount to receive? "))
    invoice = asyncio.run(wallet.request_mint(amount))
    print("invoice:", invoice.bolt11 )
    print("----")
    print("id: ", invoice.id)
    paid = input("have you paid yet?")
    if paid =='y':
        asyncio.run(wallet.mint(amount, id=invoice.id))
        print("balance:", wallet.balance_per_keyset())
        print(wallet.available_balance)

if mode =="p2pk":
    pubkey = asyncio.run(wallet.create_p2pk_pubkey())
    lock_str = f"P2PK:{pubkey}"
    print("---- Pay to public key (P2PK) lock ----\n")
    print(f"Lock: {lock_str}")
    print("")

elif mode =="q":
    exit()

elif mode =="p":
    quote_id = input("Enter quote id:")
    asyncio.run(wallet.mint(amount, id=quote_id))
    print("balance:", wallet.balance_per_keyset())
    print(wallet.balance)
    # print(wallet.keyset_id)

elif mode =="invoice send":
    ln = input("what is the lightning invoice to send to? ")
  
    quote = asyncio.run(wallet.get_pay_amount_with_fees(ln))
    print("quote: ", quote.quote, quote.amount, quote.fee_reserve, quote.paid)
    total_amount = quote.amount + quote.fee_reserve
    print("total amount:", total_amount)
    print(wallet.proofs)
    _, send_proofs = asyncio.run(wallet.split_to_send(wallet.proofs, total_amount))
    # print("send_proofs:", send_proofs)
    try:
       melt_response = asyncio.run(wallet.pay_lightning(
           send_proofs, ln, quote.fee_reserve, quote.quote
       ))
    except Exception as e:
        print(f" Error paying invoice: {str(e)}")
       
    print(" Invoice paid!")

elif mode == "balance":
    balance_per_keyset = wallet.balance_per_keyset()
    print("balance per keyset:", balance_per_keyset)
    print(wallet.balance, wallet.available_balance )
    balance_per_mint = asyncio.run(wallet.balance_per_minturl())
    print(balance_per_mint)
    response = requests.get(mint + "/v1/keysets")
    print("home keyset", response.json()['keysets'][0]['id'])
    
    print(wallet.keysets)
    for each in balance_per_keyset:
        print(balance_per_keyset[each]['available'])

    # print(wallet.proofs)
elif mode == 'secrets':
    print(wallet.mnemonic)
    print(asyncio.run(wallet.generate_n_secrets(5))[0])    

elif mode == "cashu send":
    cashu_amount = int(input("what is the cashu token amount?"))
    _, send_proofs = asyncio.run(wallet.split_to_send(wallet.proofs, cashu_amount))
    token = asyncio.run(wallet.serialize_proofs(
        send_proofs,
        include_mints=True,
        include_dleq=True,
    ))
    print(token)
elif mode == "cashu receive":
    tokenObj : TokenV3
    cashu_token = input("what is the cashu token? ")
    tokenObj = deserialize_token_from_string(cashu_token)
    print(tokenObj)
    asyncio.run(receive(tokenObj=tokenObj, wallet=wallet))
    

    

    

    







