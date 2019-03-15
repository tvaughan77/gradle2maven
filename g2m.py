# g2m.py
import click
import logging
import os
import os.path

from pom_root import create_root_level_pom

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
@click.option('--artifact', '-a')
@click.option('--artifactversion', '-v')
def main(artifact, artifactversion):
    gradle_files = find_gradle_files(".")

    create_root_level_pom(artifact, artifactversion, gradle_files)
    for gf in gradle_files:
        click.echo(f"{gf}")

    # get list of build.gradle files and paths relative to here
    # create root-level pom as a one off
    # for each sub project build.gradle file:
    #   parse each dependency line into either a default or test dependency
    #   create a sub project pom.xml
    #   write out the maven dependencies






if __name__ == "__main__":
    main('Tom', 'Hello')