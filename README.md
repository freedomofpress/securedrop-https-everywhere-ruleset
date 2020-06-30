# HTTPS-Everywhere Rulesets for SecureDrop

## Development

Setup:

```
virtualenv --python=python3 .venv
source .venv/bin/activate
pip install --require-hashes --no-deps -r requirements.txt
```

You can create a test key for signing using:

```
make test-key
```

which will create `test-key.jwk` in your current working directory.

## Updating Rulesets

### Adding a new organization

1. Ensure they are in the official SecureDrop directory. If they are not, go through the IVF process with the organization.

2. Add their domain name and the requested URL to the `onboarded.txt` via PR into this repository. We match the domain based on the landing page of the organization, comparing the `netloc` in a URL with structure `scheme://netloc/path;parameters?query#fragment`.

3. Next, perform a ruleset release as described below.

### Updating the onion URL for an organization (e.g. if they transition to v3 or rotate URLs)

1. First update their onion URL in the official SecureDrop directory using the existing process.

2. Next, perform a ruleset release as described below.

### Release process

Generate rulesets via the securedrop.org directory using the `sddir.py` script:

```
source .venv/bin/activate
python sddir.py
```

This populates the `rulesets` directory. Inspect them and check all looks sane.

To sign the rules, see HTTPS Everywhere docs [here](https://github.com/EFForg/https-everywhere/blob/master/docs/en_US/ruleset-update-channels.md#2-signing-rulesets-with-this-key) for the signing process. In the step where you remove all HTTPS Everywhere rules from `rules` in the git checkout of the `https-everywhere` git repo, you should copy all rules from `rulesets` generated from the above Python script. You do not need to create a trivial rule as described in the HTTPS Everywhere docs.

For the production rules this signing must be done via the official signing ceremony and the existing SD release key (JWK formatted version of the pubkey is in `release-pubkey.jwk`). There is some internal documentation with more detailed instructions on this, ping `@redshiftzero` if you need to do this.

Once you have the signature, place the files to serve in the root of the git tree in this repository,and then update the directory listing in `index.html`.

Commit the resulting `index.html` and all files to be served.

Upon merge the ruleset release will be live.
