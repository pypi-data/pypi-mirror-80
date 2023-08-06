from setuptools import setup, find_packages

# read requirements
with open('requirements.txt') as fh:
    requirements = fh.read().splitlines()

# read description
with open("README.md", 'r') as fh:
    long_description = fh.read()

setup(name='ddconst',
      version='0.0.2',
      author='Daniel Danis',
      author_email='daniel.gordon.danis@protonmail.com',
      description='Constants used across multiple codebases',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/ielis/ddconst',

      packages=find_packages(),
      python_requires='>=3.6',
      install_requires=requirements,
      data_files=[('', ['requirements.txt'])],
      package_data={'': ['test_data/*']},
      include_package_data=True,

      license='GPLv3',
      keywords='utility'
      )
