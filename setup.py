from setuptools import setup, find_packages

requires =[
    'click==7.0'
]

setup_options = dict(
    name='g2m',
    version='1.0.8',
    packages=find_packages(exclude=['tests*']),
    url='https://github.com/tvaughan77/gradle2maven',
    license='',
    author='tvaughan',
    author_email='',
    py_modules=['g2m', 'g2m_util', 'pom_root'],
    install_requires=requires,
    description='Converts gradle to maven',
    entry_points='''
       [console_scripts]
       g2m=g2m:main
    '''
)

setup(**setup_options)