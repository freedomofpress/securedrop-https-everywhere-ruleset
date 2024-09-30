import gzip
import json
import xml.etree.ElementTree
from pathlib import Path

LATEST_TIMESTAMP = Path("latest-rulesets-timestamp").read_text().strip()


def load_xml_files():
    xml_files = []
    for ruleset in sorted(Path("rulesets").glob("*.xml")):
        tree = xml.etree.ElementTree.parse(ruleset)
        root = tree.getroot()
        # Rebuild the JSON
        expected = {
            "name": root.attrib["name"],
            "target": [root[0].attrib["host"]],
            "rule": [{"from": root[1].attrib["from"], "to": root[1].attrib["to"]}],
        }
        xml_files.append(expected)
    return xml_files


def test_compressed_matches_xml():
    # Read the contents of the gzipped file
    with gzip.open(f"default.rulesets.{LATEST_TIMESTAMP}.gz", "rb") as f:
        rulesets = json.load(f)
    xml_files = load_xml_files()

    assert rulesets["rulesets"] == xml_files


def test_generated_matches_xml():
    # Read the contents of the default file
    rulesets = json.loads(Path("rulesets/default.rulesets").read_text())
    xml_files = load_xml_files()

    assert rulesets == xml_files


def test_unique_signature():
    """
    For every default.rulesets.*.gz file, there should be a corresponding
    rulesets-signature.*.sha256 file with no extras.
    """
    rulesets = []
    for path in sorted(Path(".").glob("default.rulesets.*.gz")):
        rulesets.append(path.name.split(".")[2])

    signatures = []
    for path in sorted(Path(".").glob("rulesets-signature.*.sha256")):
        signatures.append(path.name.split(".")[1])

    # Just verify it found *something*
    assert LATEST_TIMESTAMP in rulesets
    # Now check they're equal
    assert rulesets == signatures
