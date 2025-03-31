import csv
import logging
import os
import re
import requests
import sys
import textwrap
import urllib
from urllib.parse import urlparse
from typing import Dict

# Configure logging output
logfmt = "%(asctime)s %(levelname)-8s %(message)s"
logging.basicConfig(format=logfmt, level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S")

SECUREDROP_ONION_PSEUDO_TLD = ".securedrop.tor.onion"
RULESET_DIR = "rulesets"

# tcfmailvault.info = unlisted SecureDrop; all others: extended outage
EXEMPTIONS = [
    "tcfmailvault.info",
    "espenandersen.no",
    "www.sfchronicle.com",
    "aftenbladet.no",
    "apps.publicintegrity.org",
    "www.ktipp.ch",
    "www.abc.net.au",
    "img.huffingtonpost.com",
    "disclose.ngo",
    "techcrunch.com",
    "webapps.aljazeera.net",
    "www.apache.be",
    "www.dr.dk",
    "noyb.eu",
]


def remove_umlaut(text: str) -> str:
    text = re.sub("ü", "u", text)
    return text


def get_securedrop_directory() -> Dict:
    r = requests.get("https://securedrop.org/api/v1/directory/")
    directory_entries = r.json()

    # Keys of interest: landing_page_url and onion_address
    directory_entry_map = {}
    for directory_entry in directory_entries:
        directory_entry["base_url"] = urllib.parse.urlparse(
            directory_entry["landing_page_url"]
        ).netloc
        # For redirect URL, drop TLD from base_url: newsorg.com -> newsorg.securedrop.tor.onion
        directory_entry["securedrop_redirect_url"] = (
            directory_entry["base_url"].rsplit(".", 1)[0] + SECUREDROP_ONION_PSEUDO_TLD
        )
        directory_entry["slug"] = remove_umlaut(directory_entry["slug"])
        directory_entry["title"] = remove_umlaut(directory_entry["title"])

        directory_entry_map.update({directory_entry["base_url"]: directory_entry})

    return directory_entry_map


def write_custom_ruleset(
    onboarded_org: str, sd_rewrite_rule: str, is_https: bool, directory_entries: Dict
) -> None:
    try:
        directory_entry = directory_entries[onboarded_org]
    except KeyError:
        logging.error(f"Failed to find '{onboarded_org}', org names are:")
        logging.error(directory_entries.keys())
        raise

    secure = "s" if is_https else ""
    onion_addr = f"http{secure}://{directory_entry['onion_address']}"

    ruleset = textwrap.dedent(
        """\
    <ruleset name="{org_name}">
    \t<target host="{securedrop_redirect_url}" />
    \t<rule from="^http[s]?://{securedrop_redirect_url}"
        to="{onion_addr}" />
    </ruleset>
    """.format(
            org_name=directory_entry["title"],
            securedrop_redirect_url=sd_rewrite_rule,
            onion_addr=onion_addr,
        )
    )

    RULESET_OUTPUT = "securedrop-ruleset.xml"
    with open(
        os.path.join(RULESET_DIR, directory_entry["slug"] + "-" + RULESET_OUTPUT),
        "w",
    ) as f:
        f.write(ruleset)


if __name__ == "__main__":
    # We don't want to generate rules for all organizations. Instead we want to
    # do so on an opt-in basis. The following text file contains the homepages
    # of the organizations that have opted in.
    with open("onboarded.txt", "r") as f:
        reader = csv.DictReader(f)
        directory_entries = get_securedrop_directory()
        for row in reader:
            # Validate that no subdomains are in the onion address
            # (per https://github.com/freedomofpress/securedrop-https-everywhere-ruleset/issues/219)
            if "." in row["sd_rewrite_rule"].removesuffix(".securedrop.tor.onion"):
                logging.error(f"Subdomain not allowed in onion address: {row['sd_rewrite_rule']}")
                sys.exit(1)
            if row["primary_domain"] in EXEMPTIONS:
                logging.warning(f"Skipping exempted domain: {row['primary_domain']}")
                continue
            is_https = row["is_https"] == "yes"
            write_custom_ruleset(
                row["primary_domain"], row["sd_rewrite_rule"], is_https, directory_entries
            )

    logging.info("✔️ Custom rulesets written to directory: ./{}".format(RULESET_DIR))
