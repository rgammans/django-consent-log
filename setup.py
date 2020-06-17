from setuptools import setup
import pathlib

projectdir = pathlib.Path(__file__).parent
readme = (projectdir / "README.rst").read_text()


setup(name='consent_log',
      version='0.1',
      description='Keeps a record of consents. Required by EU law',
      long_description=readme,
      long_description_content_type="text/x-rst",
      url='http://github.com/rgammans/django-consent-log',
      author='Gamma Science',
      author_email='info@gammascience.co.uk',
      license='GPLv3',
      packages=['consent_log',
                'consent_log.migrations',
                'consent_log.management.commands'
      ],
      requires = [ 'django' ],
      classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
      ],
      zip_safe=False,
      install_requires=[
        "Django>=2.0.0",
      ],
      tests_require=[
        "tox",
      ],
      test_suite="tox",
)
