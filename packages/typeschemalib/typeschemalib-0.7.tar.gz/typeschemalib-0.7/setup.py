from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='typeschemalib',
      version='0.7',
      description='A yaml like schema that can be used to check dictionaries for correct schema',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/JakeRoggenbuck/typeschemalib',
      author='Jake Roggenbuck',
      author_email='jake@jr0.org',
      license='MIT',
      packages=['typeschemalib'],
      zip_safe=False)
