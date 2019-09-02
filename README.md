# HTTPS-Everywhere Rulesets for SecureDrop

:warning: These rulesets are for testing and development only and are not to be used in production.

## Generate SecureDrop rulesets

```
pip install -r requirements.txt
python sddir.py
```

This populates the `rulesets` directory.

## Generating signing keys and signing the rulesets

Also see HTTPS Everywhere docs [here](https://github.com/EFForg/https-everywhere/blob/master/docs/en_US/ruleset-update-channels.md).

Generate a private key for signing ruleset releases:

```
openssl genrsa -out key.pem 4096
```

Now generate the corresponding public key:

```
openssl rsa -in key.pem -outform PEM -pubout -out public.pem
```

Now dump the key in the JWK format which assumes the public key is located in `public.pem` in the same directory:

```
python jwk.py > key.jwk
```

(in production this would be done via airgap signing)

## Updating the channel

If you've updated the rules, resign them and then place the files to serve in `channel/`, then run the following to update the directory listing:

```
python update_index.py
```

Commit the resulting `index.html` and all files in `channel/`
