from setuptools import setup, find_packages
import os

directories = []

with open('README.md') as readme_file:
    README = readme_file.read()

for i in os.listdir("contacts"):
    i = "contacts\\"+i
    directories.append(i)

setup_args = dict(
    name='ContactPy',
    version='1.2.0',
    description='Useful tools to work with Contacts in Python',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    scripts=directories,
    author='Judah Beethoven',
    author_email='masterofcoding360@gmail.com',
    keywords=['vcf', 'contacts', 'Contacts Python', 'gmail'],
    url='https://github.com/judah-b2/PyContacts',
)

dependencies = ["email"]

setup(**setup_args, install_requires=dependencies)