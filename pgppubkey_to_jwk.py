from authlib.common.encoding import int_to_base64
import json
import pgpy


# Input is PGP armored pubkey
key, _ = pgpy.PGPKey.from_file('key.asc')
n = int(key._key.keymaterial.n)
e = int(key._key.keymaterial.e)

# Expected JWK format according to https://tools.ietf.org/html/rfc7518#section-6.1
pubkey = {
    'kty': 'RSA',
    'e': int_to_base64(e),
    'n': int_to_base64(n)
}
print(json.dumps(pubkey))
