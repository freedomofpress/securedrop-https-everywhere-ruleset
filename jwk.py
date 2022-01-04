from authlib.jose import JWK
from authlib.jose import JWK_ALGORITHMS


jwk = JWK(algorithms=JWK_ALGORITHMS)
with open("public.pem", "r") as f:
    key = f.read()
obj = jwk.dumps(key, kty="RSA", indent=4, sort_keys=True)
key_str = str(obj).replace("'", '"')
print(key_str)
