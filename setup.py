from setuptools import setup

setup(name='consent_log',
      version='0.1',
      description='Keeps a record of consents. Required by EU law',
      url='http://github.com/storborg/funniest',
      author='Gamma Science',
      author_email='info@gammascience.co.uk',
      license='GPLv3',
      packages=['consent_log'],
      requires = [ 'django' ],
      zip_safe=False,
    install_requires=[
        "Django>=2.0.0",
    ],
    tests_require=[
        "nose",
        "coverage",
    ],
    test_suite="tests.runtests.start",
)
