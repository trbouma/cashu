from mnemonic import Mnemonic
from cashu.core.crypto.keys import derive_key_for_amount, derive_pubkey
from binascii import hexlify

mnemo = Mnemonic("english")
seed = bytes("the)")

mnemonic_str = "solution jelly sight much comic woman salad shift elbow diesel movie immense"
amount = int(13634523)           

test = derive_key_for_amount(mnemonic_str,"m/0'/0'/0'",amount)
privkey_hex = test[amount].serialize()

print(privkey_hex)

pubkey_hex= hexlify(derive_pubkey(privkey_hex).serialize()).decode()
print(pubkey_hex)
