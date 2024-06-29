from mnemonic import Mnemonic
from cashu.core.crypto.keys import derive_key_for_amount, derive_pubkey
from binascii import hexlify

mnemo = Mnemonic("english")
# mnemonic_str = mnemo.generate()
# print(mnemonic_str)
mnemonic_str = "solution jelly sight much comic woman salad shift elbow diesel movie immense"
amount = int(21e8)           

test = derive_key_for_amount(mnemonic_str,"m/0'/0'/0'",amount)
seed = test[amount].serialize()

print(seed)

pubkey= hexlify(derive_pubkey(seed).serialize()).decode()
print(pubkey)
