# g2m.py
import click
import logging
import os
import os.path

from g2m_util import get_root_level_gradle_file, write_pom
from lxml import etree as ET
from pom_root import create_root_level_pom, find_group_id
from pom_submodule import create_submodule_pom, derive_submodule_pom_filename
from xml.dom.minidom import parseString

log_handler = logging.StreamHandler()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)


def find_gradle_files(root_path):
    """
    :param root_path: Where to start looking for gradle-related files
    (for now, just hardcoded to search for "build.gradle")
    :return: An array of tuples; each tuple is (dirpath, filename)
    of a gradle-related file.
    """
    gradle_files = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in [f for f in filenames if f == 'build.gradle']:
            logger.debug(f"dirpath is {dirpath} and filename is {filename}")
            gradle_files.append((dirpath, filename))
    return gradle_files



@click.command()
@click.option('--artifact', '-a', prompt='The maven artifactId (e.g. echo-service)')
@click.option('--artifactversion', '-v', prompt='The artifact version (e.g. 1.0.0-SNAPSHOT)')
def main(artifact, artifactversion):
    # get list of build.gradle files and paths relative to here
    # extract the groupId from the root-level build.gradle
    # create root-level pom as a one off
    # for each sub project build.gradle file:
    #   parse each dependency line into either a default or test dependency
    #   create a sub project pom.xml
    #   write out the maven dependencies

    gradle_files = find_gradle_files(".")

    root_level_gradle_file = get_root_level_gradle_file(gradle_files)
    group_id = find_group_id(root_level_gradle_file)

    root_pom = create_root_level_pom(group_id, artifact, artifactversion, gradle_files)
    write_pom(root_pom, './pom.xml')

    for gradle_file in gradle_files:
        if not gradle_file == root_level_gradle_file:
            submodule_pom = create_submodule_pom(group_id, artifact, artifactversion, gradle_file)
            write_pom(submodule_pom, derive_submodule_pom_filename(gradle_file))








if __name__ == "__main__":
    main('Tom', 'Hello')