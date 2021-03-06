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

3. Next, generate and sign the update ruleset using the following command (requires signing key, please ping `@emkll` for assistance):

```
./scripts/generate-and-sign
```

4. Commit all files generated by the script above and open a Pull Request to this repository. Once the PR is merged, the rulesets will automatically be deployed to production.

## Verifying changes

Inspect the diff. If it looks good, commit the resulting `index.html` and all files to be served. To test locally, run

    make serve

And configure your browser to use `http://localhost:4080/https-everywhere/`.

## Deployment

Upon merge the container will be published to `quay.io/freedomofpress` and the new tag will be deployed automatically.
