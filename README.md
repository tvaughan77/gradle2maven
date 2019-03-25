# gradle2maven
Converts a multi-gradle project to a bunch o' poms

Usage:
```
g2m -a <top level artifact name> -v <top level artifact version>
```


## Assumptions

This script assumes a multi-module gradle project like:

```
my-service/
    build.gradle
    my-sub-project-a/
        build.gradle
    my-sub-project-z/
        build.gradle
```

It will produce new `pom.xml` files everywhere a build.gradle file exists with the following rules:

* the root-level build.gradle is a one-off and needs to manually curated, but will include the `<modules>...` stanza
* each sub project will point to the root level pom as its parent
* any special plugin or non-dependency-management related gradle section is ignored; you'll need to find the 
maven equivalent and wire it up manually

### Dumpster Fire Formatting

This (currently) produces godawful single-line `<depdency>` blocks in the resulting pom.xmls.  I've found it easier
to just do a "Command+Option+L" in IntelliJ to format all the poms correctly than battle the 3 different XML
libraries everyone recommends one use to prettyprint XML in Python.  I'm seriously shocked how hard it is to just
get a well-formatted XML document saved to a file in this oh-so-beloved language.  Must by PEBKAU.

### Adding dependencies
1. After adding the dependency to requirements-to-freeze.txt,
```
pip install -r requirements-to-freeze.txt
pip freeze > requirements.txt
```

2. Also, add the dependency to the `requires` array in setup.py

3. Finally, tox probably needs to be recreated with `tox --recreate`

### Installing
```
pyenv local 3.6.0
pip install -r requirements.txt
pip install . 
python setup.py sdist bdist_wheel upload -r local

```

### Running tests
Running tests _should_ be as straight-forward as running this in a non-virtualenv (tox creates its own):
```
tox
```

If you've recently added a dependency to the project, you may need to (one time) run:
```
tox --recreate
```
