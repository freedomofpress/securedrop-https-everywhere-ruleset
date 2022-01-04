from authlib.jose import JsonWebKey

with open("public.pem", "r") as f:
    key_file = f.read()

key = JsonWebKey.import_key(key_file, {"kty": "RSA"})

print(key.as_json())
