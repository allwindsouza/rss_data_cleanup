import xml.etree.ElementTree as ET
import requests


def compare_xml_files(data_1, data_2):
    """
    take in xml data not path
    """
    tree1 = ET.ElementTree(ET.fromstring(data_1))
    root1 = tree1.getroot()


    tree2 = ET.ElementTree(ET.fromstring(data_2))
    root2 = tree2.getroot()

    # Define a function to recursively compare elements
    def compare_elements(elem1, elem2):
        # Compare the tag names of the elements
        if elem1.tag != elem2.tag:
            return False

        # Compare the attributes of the elements
        if elem1.attrib != elem2.attrib:
            return False

        # Compare the text content of the elements
        if elem1.text != elem2.text:
            return False

        # Compare the child elements of the elements
        if len(elem1) != len(elem2):
            return False
        for child1, child2 in zip(elem1, elem2):
            if not compare_elements(child1, child2):
                return False

        return True

    # Compare the roots of the XML files
    differences = []
    if not compare_elements(root1, root2):
        # Output the differences
        for elem1, elem2 in zip(root1, root2):
            if not compare_elements(elem1, elem2):
                differences.append((elem1.tag, ET.tostring(elem1), ET.tostring(elem2)))

    return differences


