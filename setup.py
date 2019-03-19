from setuptools import setup, find_packages

requires =[
    'click==7.0',
    'lxml==4.3.2'
]

setup_options = dict(
    name='g2m',
    version='1.1.0',
    packages=find_packages(exclude=['tests*']),
    url='https://github.com/tvaughan77/gradle2maven',
    license='',
    author='tvaughan',
    author_email='',
    py_modules=['g2m', 'g2m_util', 'pom_root', 'pom_submodule'],
    install_requires=requires,
    description='Converts gradle to maven',
    entry_points='''
       [console_scripts]
       g2m=g2m:main
    '''
)

setup(**setup_options)