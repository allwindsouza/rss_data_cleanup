import xml.etree.ElementTree as ET
import requests
import re

def elements_equal(elem1, elem2):
    try:
        if elem1.tag != elem2.tag:
            return False
        if elem1.text != elem2.text:
            return False
        if len(elem1) != len(elem2):
            return False
        if not all(elements_equal(c1, c2) for c1, c2 in zip(elem1, elem2)):
            return False
        if "date" in elem1.attrib or "time" in elem1.attrib:
            return True  # Return True for date or time-related fields
        for key in elem1.attrib:
            if re.search(r"(date|time)", key):
                return True  # Return True for date or time-related fields
            if elem1.attrib[key] != elem2.attrib.get(key):
                return False
        return True
    except:
        return False


def compare_xml_files(data_1, data_2):
    """
    Compare two XML files, ignoring any differences in date or time-related fields.
    """
    try:
        # Load XML files into ElementTree objects
        tree1 = ET.ElementTree(ET.fromstring(data_1))
        tree2 = ET.ElementTree(ET.fromstring(data_2))

        # Get root elements of both trees
        root1 = tree1.getroot()
        root2 = tree2.getroot()

        # Check for differences in non-date and non-time-related fields
        for elem1, elem2 in zip(root1.iter(), root2.iter()):
            if not elements_equal(elem1, elem2):
                if not re.search(r"(date|time)", elem1.tag):
                    for key in elem1.attrib:
                        if not re.search(r"(date|time)", key):
                            if elem1.attrib[key] != elem2.attrib.get(key):
                                return False
    except:
        return False
    return True





