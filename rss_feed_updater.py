import os
import datetime
import xml.etree.ElementTree as ET

FEED_PATH = "kailey.xml"

# Today's example item (in reality, this would be generated dynamically)
new_item = {
    "title": "Example Company announces Q2 results",
    "link": "https://example.com/q2-results",
    "description": "Example Company posted strong revenue growth in Q2 2025.",
    "pubDate": datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'),
    "guid": "https://example.com/q2-results"
}


def load_or_create_feed(path):
    if os.path.exists(path):
        tree = ET.parse(path)
        root = tree.getroot()
        return tree, root
    else:
        rss = ET.Element("rss", version="2.0")
        channel = ET.SubElement(rss, "channel")
        ET.SubElement(channel, "title").text = "Daily Business Digest"
        ET.SubElement(channel, "link").text = "https://example.com"
        ET.SubElement(channel, "description").text = "A daily digest of news for selected companies."
        ET.SubElement(channel, "language").text = "en-us"
        ET.SubElement(channel, "pubDate").text = new_item["pubDate"]
        tree = ET.ElementTree(rss)
        return tree, rss


def append_item_to_feed(root, item):
    channel = root.find("channel")
    item_elem = ET.SubElement(channel, "item")
    ET.SubElement(item_elem, "title").text = item["title"]
    ET.SubElement(item_elem, "link").text = item["link"]
    ET.SubElement(item_elem, "description").text = item["description"]
    ET.SubElement(item_elem, "pubDate").text = item["pubDate"]
    ET.SubElement(item_elem, "guid").text = item["guid"]


def write_feed(tree, path):
    tree.write(path, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    tree, root = load_or_create_feed(FEED_PATH)
    append_item_to_feed(root, new_item)
    write_feed(tree, FEED_PATH)
    print(f"Feed updated: {FEED_PATH}")
