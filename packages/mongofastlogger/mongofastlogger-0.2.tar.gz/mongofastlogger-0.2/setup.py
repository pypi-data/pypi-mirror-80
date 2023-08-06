from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='mongofastlogger',
      version='0.2',
      description='A simple and fask logging library that uses the power of mongodb to save and query logs (with built in cli)',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/JakeRoggenbuck/mongofastlogger',
      author='Jake Roggenbuck',
      author_email='jake@jr0.org',
      license='MIT',
      packages=['mongofastlogger'],
      zip_safe=False)
