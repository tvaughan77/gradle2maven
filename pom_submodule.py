import logging
import re
from g2m_util import namespace, get_module_name, load_file
from lxml import etree

logger = logging.getLogger()

# =====================================================================================================================
# Regex patterns
#

# Any line in a build.gradle file that starts with testCompile should result in a test-scope <dependency>
regex_scope_test = re.compile("testCompile (.+)$")

# Otherwise, any line that just has 'compile' in it should result in a default-scope <dependency>
regex_scope_default = re.compile("compile (.+)$")

# Gradle also allows a sub-module to depend on another submodule with "compile project", but that should
# also just result in a default-scope <dependency> in our pom
regex_project = re.compile("project\\(':(.*)'\\)")

# Some dependencies have versions, some don't (they're delegated to a parent).  Support either case.  I wrote
# this out as 1 big ass regex but it made my head hurt, so I'm splitting it up to improve readability/debugging
regex_version = re.compile("group:\\s*'(.+)'\\s*,\\s*name:\\s*'(.+)'\\s*,\\s*version:\\s*'(.+)'")
regex_no_version = re.compile("group:\\s*'(.+)'\\s*,\\s*name:\\s*'(.+)'\\s*")

# =====================================================================================================================

template = """<project xmlns="http://maven.apache.org/POM/4.0.0"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>xxx</groupId>
        <artifactId>xxx</artifactId>
        <version>xxx</version>
    </parent>

    <artifactId>xxx</artifactId>
    <name>xxx</name>
    <description>xxx</description>

    <properties>
    </properties>

    <dependencies>
    </dependencies>
</project>
"""


def create_submodule_pom(group_id, artifact, artifact_version, gradle_file_tuple):
    """
    :param group_id: The groupId of this artifact
    :param artifact: The parent artifact name
    :param artifact_version: The parent artifact version
    :param gradle_file_tuple: The (path, filename) of the build.gradle to replace with a pom.xml
    :return: An XML Element representing a POM for the sub project
    """
    utf8_parser = etree.XMLParser(encoding='utf-8')
    pom = etree.fromstring(template, parser=utf8_parser)

    module_name = get_module_name(gradle_file_tuple)

    pom.find(f"{namespace}parent/{namespace}groupId").text = f"{group_id}"
    pom.find(f"{namespace}parent/{namespace}artifactId").text = f"{artifact}"
    pom.find(f"{namespace}parent/{namespace}version").text = f"{artifact_version}"
    pom.find(f"{namespace}artifactId").text = module_name
    pom.find(f"{namespace}name").text = module_name
    pom.find(f"{namespace}description").text = module_name

    dependencies = pom.find(f"{namespace}dependencies")

    default_dependencies, test_dependencies = parse_dependencies(gradle_file_tuple)

    for dd in default_dependencies:
        dependencies.append(make_dependency_element(dd, None))

    for td in test_dependencies:
        dependencies.append(make_dependency_element(td, 'test'))

    return pom


def derive_submodule_pom_filename(gradle_file_tuple):
    """
    :param gradle_file_tuple: A (path, filename) of a gradle file
    :return: The corresponding pom.xml location that should replace the gradle_file
    """
    return f"{gradle_file_tuple[0]}/pom.xml"


def parse_dependencies(gradle_file_tuple):
    """
    :param gradle_file_tuple: A (path, filename) of a gradle file
    :return: A pair of lists of (groupId, artifactId, version) data.  The first returned list is of default
    scoped dependencies, the second list is of test-scoped dependencies.  The version data may be None
    """
    gradle = load_file(gradle_file_tuple)
    default_dependencies = []
    test_dependencies = []
    for line in gradle:
        match_scope_test = re.search(regex_scope_test, line)
        if match_scope_test:
            logger.debug(f"Found test scope dependency {match_scope_test.group(1)}")
            test_dependencies.append(parse_dependency(line))
        else:
            match_scope_default = re.search(regex_scope_default, line)
            if match_scope_default:
                logger.debug(f"Found default scope dependency {match_scope_default.group(1)}")
                default_dependencies.append(parse_dependency(line))

    return default_dependencies, test_dependencies


def parse_dependency(dependency_line):
    """
    :param dependency_line: A gradle-style dependency line like "group: 'com.upside.model', name: 'model-core'"
    with an optional "version" definition like "'com.something', name: 'my-artifact', 'version':'1.2.3'"
    :return: A tuple of (groupId, artifactId, version), where version may be None if undefined in the input
    """

    # If the dependency_line is like "compile project(':merchant-service-db')"
    match_project = re.search(regex_project, dependency_line)
    if match_project:
        return '${project.groupId}', match_project.group(1), '${project.version}'

    # If the dependency_line is like "compile group: 'org.jscience', name: 'jscience', version:'4.3.1'"
    match_version = re.search(regex_version, dependency_line)
    if match_version:
        return match_version.group(1), match_version.group(2), match_version.group(3)

    # If the dependency line is like "compile group: 'io.dropwizard', name: 'dropwizard-core'" (no version)
    match_dep = re.search(regex_no_version, dependency_line)
    if match_dep:
        return match_dep.group(1), match_dep.group(2), None

    else:
        raise ValueError(f"Expected to find dependency info in {dependency_line} but our regex didn't match")


def make_dependency_element(dep_tuple, scope):
    """
    :param dep_tuple: A tuple of (groupId, artifactId, version) where version is possibly null
    :param scope: Either 'test' or None; where None is the default scope.
    :return: An XML element wrapping the dependency input in a pom.xml-appropriate <dependency> section
    """
    dependency = etree.Element('dependency')
    group_id = etree.SubElement(dependency, 'groupId')
    group_id.text = dep_tuple[0]
    artifact_id = etree.SubElement(dependency, 'artifactId')
    artifact_id.text = dep_tuple[1]

    if dep_tuple[2]:
        version = etree.SubElement(dependency, 'version')
        version.text = dep_tuple[2]

    if scope:
        s = etree.SubElement(dependency, 'scope')
        s.text = scope

    return dependency
