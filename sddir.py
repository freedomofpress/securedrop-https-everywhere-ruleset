import re
import requests
import os
import urllib

from typing import Dict

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
    for directory_entry in directory_entries:
        directory_entry["base_url"] = urllib.parse.urlparse(
            directory_entry["landing_page_url"]
        ).netloc
        directory_entry["securedrop_redirect_url"] = (
            directory_entry["base_url"] + SECUREDROP_ONION_PSEUDO_TLD
        )
        directory_entry["onion_addr_with_protocol"] = (
            DEFAULT_ONION_PROTOCOL + directory_entry["onion_address"]
        )
        directory_entry["slug"] = remove_umlaut(directory_entry["slug"])
        directory_entry["title"] = remove_umlaut(directory_entry["title"])

    return directory_entries


def write_custom_ruleset(directory_entries: Dict) -> None:
    for directory_entry in directory_entries:
        ruleset = """<ruleset name="{org_name}">\n\t<target host="{org_url}{securedrop_tld}" />\n\t<rule from="^http[s]?://{securedrop_redirect_url}"
        to="{onion_addr_with_protocol}" />\n</ruleset>\n""".format(
            org_name=directory_entry["title"],
            org_url=directory_entry["base_url"],
            securedrop_redirect_url=directory_entry["securedrop_redirect_url"],
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
    directory_entries = get_securedrop_directory()
    write_custom_ruleset(directory_entries)

    print("✔️ Custom rulesets written to directory: ./{}".format(RULESET_DIR))
