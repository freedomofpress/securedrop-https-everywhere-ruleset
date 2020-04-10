# HTTPS-Everywhere Rulesets for SecureDrop

## Development

Setup:

```
virtualenv --python=python3 .venv
source .venv/bin/activate
pip install -r requirements.txt
```

You can create a test key for signing using:

```
make test-key
```

which will create `test-key.jwk` in your current working directory.

## Updating Rulesets

Generate rulesets from securedrop directory:

```
python sddir.py
```

This populates the `rulesets` directory.

If you're signing the production rules, see HTTPS Everywhere docs [here](https://github.com/EFForg/https-everywhere/blob/master/docs/en_US/ruleset-update-channels.md) for the signing process. For the production rules this is done via the official signing cermony and the existing SD release key (JWK formatted version of the pubkey is in `release-pubkey.jwk`).

Then place the files to serve in the root of the git tree, then update the directory listing in `index.html`.

Commit the resulting `index.html` and all files to be served.
