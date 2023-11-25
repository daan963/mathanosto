import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

def get_last_serial_number():
    # Try to read the last serial number from a file
    try:
        with open("last_serial_number.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        # If the file doesn't exist, return 0
        return 0

def update_last_serial_number(serial_number):
    # Save the last serial number to a file
    with open("last_serial_number.txt", "w") as file:
        file.write(str(serial_number))

def create_rss_feed(serial_number):
    root = ET.Element("rss", xmlns="http://purl.org/dc/elements/1.1/", version="2.0")
    channel = ET.SubElement(root, "channel")

    title = ET.SubElement(channel, "title")
    title.text = "Qa Az Fd"

    link = ET.SubElement(channel, "link")
    link.text = f"https://qa-az-fd.jiosaavn.com/thap/"

    lanmange = ET.SubElement(channel, "lanmange")
    lanmange.text = "en"

    return root, channel

def create_rss_item(channel, url):
    item = ET.SubElement(channel, "item")

    title = ET.SubElement(item, "title")
    title.text = "watch sfasdfsdzvcxsfsdg gfdg sfsd livesfsdgfd stream"

    link = ET.SubElement(item, "link")
    link.text = url

    description = ET.SubElement(item, "description")
    description.text = "<div class=\"field field-name-field-date field-type-datetime field-laman-above;/div>"

    # Define the "dc" namespace
    dc_namespace = "http://purl.org/dc/elements/1.1/"
    dc_creator = ET.SubElement(item, f"{{{dc_namespace}}}creator")
    dc_creator.text = "royal"

    guid = ET.SubElement(item, "guid", isPermaLink="false")
    guid.text = f"13584 at {url}"

def save_rss_feed(root, serial_number):
    rss_name = f"{serial_number:06d}.xml"

    tree = ET.ElementTree(root)
    tree.write(rss_name, encoding="utf-8", xml_declaration=True)

    # Format the XML file for better readability
    with open(rss_name, "r") as file:
        xml_content = file.read()

    xml_dom = minidom.parseString(xml_content)
    formatted_xml = xml_dom.toprettyxml(indent="  ")

    with open(rss_name, "w") as file:
        file.write(formatted_xml)

    print(f"RSS feed saved as '{rss_name}'")

def main():
    input_file = "list.txt"

    if not os.path.isfile(input_file):
        print("Input file 'list.txt' not found.")
        return

    last_serial_number = get_last_serial_number()

    root, channel = create_rss_feed(last_serial_number)

    with open(input_file, "r") as file:
        urls = file.readlines()

    for i, url in enumerate(urls, start=last_serial_number + 1):
        url = url.strip()
        if url:
            create_rss_item(channel, url)

            # Check if the limit of 22 URLs is reached
            if i % 22 == 0:
                save_rss_feed(root, serial_number=i)
                root, channel = create_rss_feed(i + 1)

    # Save the last batch of URLs
    save_rss_feed(root, serial_number=i)
    update_last_serial_number(i)

if __name__ == "__main__":
    main()
