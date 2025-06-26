import datetime
import xml.etree.ElementTree as ET
import os
import random

# Path to the output file
output_file = "kailey.xml"

# Set the maximum number of items to keep
MAX_ITEMS = 30

# Add a joke if no real articles are found
DAD_JOKES = [
    "Why don't skeletons fight each other? They don't have the guts.",
    "What do you call fake spaghetti? An impasta!",
    "I only know 25 letters of the alphabet. I don't know y.",
    "What do you call cheese that isn't yours? Nacho cheese.",
    "Why did the scarecrow win an award? Because he was outstanding in his field."
]

# TODO: Replace with actual news-fetching logic
items = []  # <-- no test articles anymore

# Load existing items if the file exists
existing_items = []
if os.path.exists(output_file):
    tree = ET.parse(output_file)
    root = tree.getroot()
    for item_elem in root.find("channel").findall("item"):
        item = {
            "title": item_elem.find("title").text,
            "link": item_elem.find("link").text,
            "description": item_elem.find("description").text,
            "pubDate": item_elem.find("pubDate").text,
            "guid": item_elem.find("guid").text,
        }
        existing_items.append(item)

# If no new items, add a dad joke
if not items:
    joke = random.choice(DAD_JOKES)
    now = datetime.datetime.utcnow()
    pub_date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
    items.append({
        "title": "Daily Dad Joke",
        "link": "https://example.com/dad-joke",
        "description": joke,
        "pubDate": pub_date,
        "guid": f"https://example.com/dad-joke-{now.strftime('%Y%m%d%H%M%S')}"
    })

# Combine and de-duplicate
all_items = items + existing_items
seen = set()
unique_items = []
for item in all_items:
    if item["guid"] not in seen:
        seen.add(item["guid"])
        unique_items.append(item)
    if len(unique_items) >= MAX_ITEMS:
        break

# Generate RSS XML
rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "Daily Business Digest"
ET.SubElement(channel, "link").text = "https://example.com"
ET.SubElement(channel, "description").text = "A daily digest of news for selected companies."
ET.SubElement(channel, "language").text = "en-us"
ET.SubElement(channel, "pubDate").text = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

for item in unique_items:
    item_elem = ET.SubElement(channel, "item")
    ET.SubElement(item_elem, "title").text = item["title"]
    ET.SubElement(item_elem, "link").text = item["link"]
    ET.SubElement(item_elem, "description").text = item["description"]
    ET.SubElement(item_elem, "pubDate").text = item["pubDate"]
    ET.SubElement(item_elem, "guid").text = item["guid"]

# Write to file
tree = ET.ElementTree(rss)
tree.write(output_file, encoding="utf-8", xml_declaration=True)
