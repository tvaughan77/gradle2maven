import os
from lxml import etree as ET

namespace = '{http://maven.apache.org/POM/4.0.0}'


def load_file(path_file_tuple):
    """
    :param path_file_tuple: A tuple of (path, filename) to load and read
    :return: an array of strings, one element per line in the file
    """
    file = f"{path_file_tuple[0]}/{path_file_tuple[1]}"
    with open(file, 'r') as myfile:
        content = myfile.readlines()
    return content


def write_pom(element, filename):
    """
    :param element: A root-level element to write out
    :param filename: Where to write the XML
    """
    element_tree = ET.ElementTree(element)
    element_tree.write(filename, pretty_print=True, xml_declaration=True, encoding="utf-8")


def get_root_level_gradle_file(gradle_files):
    """
    This is lame; but to work in both test and production situations
    (where the root level gradle file should always be "."), this
    just finds the shortest path in the list of gradle files and
    assumes that's the "root level" gradle file.
    :param gradle_files: A list of (path, filenames) of gradle-related
    files
    :return: The root level gradle file, or None if none can be found
    """
    shortest_path = 1024
    shortest_tuple = None
    for tuple in gradle_files:
        if len(tuple[0]) < shortest_path:
            shortest_path = len(tuple[0])
            shortest_tuple = tuple
    return shortest_tuple


def get_module_element(path_file_tuple):
    """
    Returns a submodule's name wrapped as a <module>...</module> XML Element
    :param path_file_tuple: A (path, file) tuple to a build.gradle file
    :return: The name of the module (assumed to be 'the last part' of the path), wrapped in a module XML Element
    """
    module = ET.Element('module')
    module.text = get_module_name(path_file_tuple)
    return module


def get_module_name(path_file_tuple):
    """
    Assumes the name of a module is the same as the subdirectory beneath which it's stored
    :param path_file_tuple: A (path, file) tuple
    :return: The "last part" of the path as a string
     For example, if path_file_tuple is ('./my-submodule', 'build.gradle') then this should return 'my-submodule'
    """
    submodule_name = os.path.split(path_file_tuple[0])
    return submodule_name[1]
