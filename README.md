# gradle2maven
Converts a multi-gradle project to a bunch o' poms

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

It will product new `pom.xml` files everywhere a build.gradle file exists with the following rules:

* the root-level build.gradle is a one-off and needs to manually curated, but will include the `<modules>...` stanza
* each sub project will point to the root level pom as its parent
* any special plugin or non-dependency-management related gradle section is ignored; you'll need to find the 
maven equivalent and wire it up manually

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