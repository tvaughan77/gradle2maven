import unittest

from lxml import etree
from pom_submodule import derive_submodule_pom_filename, create_submodule_pom, \
    parse_dependencies, parse_dependency, make_dependency_element


class TestPomSubmodule(unittest.TestCase):

    def test_derive_submodule_pom_filename(self):
        gradle_tuple = ('./mysubproject-a', 'build.gradle')
        self.assertEqual('./mysubproject-a/pom.xml', derive_submodule_pom_filename(gradle_tuple))

    def test_create_submodule_pom(self):
        pom = create_submodule_pom('com.myGroup',
                                   'myArtifact',
                                   '1.0.0',
                                   ('./tests/my-fake-project/sub-project-a', 'build.gradle'))
        actual_string = etree.tostring(pom, pretty_print=True).decode('utf-8')

        print(f"the actual string is '{actual_string}'")

        expected = etree.fromstring(EXPECTED_POM)
        expected_string = etree.tostring(expected, pretty_print=True).decode('utf-8')

        self.assertEqual(expected_string, actual_string)

    def test_parse_dependency(self):
        # These all look the same, but there's minor spaces missing, etc conditions being tested here
        actual = parse_dependency("group: 'com.foo.bar', name: 'whatever'")
        self.assertTupleEqual(('com.foo.bar', 'whatever', None), actual)

        actual = parse_dependency("group:'com.foo.bar' , name: 'whatever'")
        self.assertTupleEqual(('com.foo.bar', 'whatever', None), actual)

        actual = parse_dependency("group: 'com.foo.bar',name: 'whatever'")
        self.assertTupleEqual(('com.foo.bar', 'whatever', None), actual)

        actual = parse_dependency("group: 'com.foo.bar', name:'whatever'")
        self.assertTupleEqual(('com.foo.bar', 'whatever', None), actual)

    def test_parse_dependency_with_version(self):
        actual = parse_dependency("group: 'com.foo.bar', name: 'whatever', version: '1.2.3'")
        self.assertTupleEqual(('com.foo.bar', 'whatever', '1.2.3'), actual)

        actual = parse_dependency("group: 'com.foo.bar', name: 'whatever',version: '1.2.3' ")
        self.assertTupleEqual(('com.foo.bar', 'whatever', '1.2.3'), actual)

    def test_parse_dependencies(self):
        (default_deps, test_deps) = parse_dependencies(('./tests/my-fake-project/sub-project-a', 'build.gradle'))

        self.assertTupleEqual(('${project.groupId}', 'foo-project', '${project.version}'), default_deps[0])
        self.assertTupleEqual(('com.upside.model', 'model-core', None), default_deps[1])
        self.assertTupleEqual(('com.fasterxml.jackson.core',  'jackson-databind', None), test_deps[0])
        self.assertTupleEqual(('com.something', 'my-artifact', '1.2.3'), test_deps[1])

    def test_make_dependency_element_no_version_no_scope(self):
        element = make_dependency_element(('a', 'b', None), None)
        self.assertEqual('<dependency><groupId>a</groupId><artifactId>b</artifactId></dependency>',
                         etree.tostring(element).decode('utf-8'))

    def test_make_dependency_element_no_version_test_scope(self):
        element = make_dependency_element(('a', 'b', None), 'test')
        self.assertEqual('<dependency><groupId>a</groupId><artifactId>b</artifactId><scope>test</scope></dependency>',
                         etree.tostring(element).decode('utf-8'))

    def test_make_dependency_element_version_no_scope(self):
        element = make_dependency_element(('a', 'b', '1'), None)
        self.assertEqual('<dependency><groupId>a</groupId><artifactId>b</artifactId><version>1</version></dependency>',
                         etree.tostring(element).decode('utf-8'))

    def test_make_dependency_element_version_test_scope(self):
        element = make_dependency_element(('a', 'b', '1'), 'test')
        self.assertEqual('<dependency><groupId>a</groupId><artifactId>b</artifactId>'
                         '<version>1</version><scope>test</scope></dependency>',
                         etree.tostring(element).decode('utf-8'))


EXPECTED_POM = """<project xmlns="http://maven.apache.org/POM/4.0.0"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>com.myGroup</groupId>
        <artifactId>myArtifact</artifactId>
        <version>1.0.0</version>
    </parent>

    <artifactId>sub-project-a</artifactId>
    <name>sub-project-a</name>
    <description>sub-project-a</description>

    <properties>
    </properties>

    <dependencies>
    <dependency><groupId>${project.groupId}</groupId><artifactId>foo-project</artifactId><version>${project.version}</version></dependency><dependency><groupId>com.upside.model</groupId><artifactId>model-core</artifactId></dependency><dependency><groupId>com.fasterxml.jackson.core</groupId><artifactId>jackson-databind</artifactId><scope>test</scope></dependency><dependency><groupId>com.something</groupId><artifactId>my-artifact</artifactId><version>1.2.3</version><scope>test</scope></dependency></dependencies>
</project>

"""

