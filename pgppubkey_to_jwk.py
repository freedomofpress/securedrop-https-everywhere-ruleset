import json
from josepy import JWK

with open('public_release.pem', 'rb') as f:
    key = f.read()

jwk = JWK.load(key).fields_to_partial_json()
jwk['kty'] = 'RSA'
print(json.dumps(jwk, indent=4, sort_keys=True))
