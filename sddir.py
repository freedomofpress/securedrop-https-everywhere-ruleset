import re
import requests
import os
import csv
import urllib

from typing import Dict, List

SECUREDROP_ONION_PSEUDO_TLD = ".securedrop.tor.onion"
DEFAULT_ONION_PROTOCOL = "http://"  # We don't store protocol in the directory
RULESET_DIR = "rulesets"


def remove_umlaut(text: str) -> str:
    text = re.sub('ü', 'u', text)
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
            directory_entry["base_url"].rsplit('.',1)[0] + SECUREDROP_ONION_PSEUDO_TLD
        )
        directory_entry["onion_addr_with_protocol"] = (
            DEFAULT_ONION_PROTOCOL + directory_entry["onion_address"]
        )
        directory_entry["slug"] = remove_umlaut(directory_entry["slug"])
        directory_entry["title"] = remove_umlaut(directory_entry["title"])

        directory_entry_map.update({directory_entry["base_url"]: directory_entry})

    return directory_entry_map


def write_custom_ruleset(onboarded_org: str, sd_rewrite_rule: str, directory_entries: Dict) -> None:
    try:
        directory_entry = directory_entries[onboarded_org]
    except KeyError:
        print(f"Failed to find '{onboarded_org}', org names are:")
        print(directory_entries.keys())
        raise

    ruleset = """<ruleset name="{org_name}">\n\t<target host="{securedrop_redirect_url}" />\n\t<rule from="^http[s]?://{securedrop_redirect_url}"
    to="{onion_addr_with_protocol}" />\n</ruleset>\n""".format(
        org_name=directory_entry["title"],
        securedrop_redirect_url=sd_rewrite_rule,
        onion_addr_with_protocol=directory_entry["onion_addr_with_protocol"],
        securedrop_tld=SECUREDROP_ONION_PSEUDO_TLD,
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
    with open('onboarded.txt', 'r') as f:
        reader = csv.DictReader(f)
        directory_entries = get_securedrop_directory()
        for row in reader:
            #write_custom_ruleset(org.strip(), directory_entries)
            write_custom_ruleset(row["primary_domain"], row["sd_rewrite_rule"], directory_entries)


    print("✔️ Custom rulesets written to directory: ./{}".format(RULESET_DIR))
