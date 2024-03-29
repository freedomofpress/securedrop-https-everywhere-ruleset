### Status

Work in Progress / Ready for review

### Review Checklist

- [ ] Changes to `onboarded.txt` are accurate
- [ ] The file `default.rulesets.TIMESTAMP.gz` has been updated, extracting that file and inspecting the contents of the JSON file produces the expected rules
- [ ] The ruleset has been verified by modifying the HTTPS Everywhere configuration in a Tor Browser instance pointing to `Path Prefix`: `https://raw.githubusercontent.com/freedomofpress/securedrop-https-everywhere-ruleset/$BRANCH_NAME`
- [ ] `index.html` has been updated using `./update_index.sh`

### Post-Deployment Checklist

- [ ] Added/modified onion names have been updated in the SecureDrop Directory
