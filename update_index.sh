#!/bin/bash
set -e
TIMESTAMP="$(<latest-rulesets-timestamp)"

# Replaces all occurrences of the form .0. with the new timestamp, where 0
# is any sequence of numbers with at least one digit
sed -Ei "s/\.[0-9]+\./\.$TIMESTAMP\./g" index.html

echo "Timestamp in index.html has been set to $TIMESTAMP. Please inspect the"
echo "diff below."
echo
git diff index.html
