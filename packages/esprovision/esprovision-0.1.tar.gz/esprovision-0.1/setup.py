from setuptools import setup, find_packages
from io import open
from os import path
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent
# The text of the README file
README = (HERE / "README.md").read_text()
# automatically captured required modules for install_requires in requirements.txt and as well as configure dependency links
with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]

setup(
    name='esprovision',
    description='A command-line tool for provisioning multiple esphome devices through tuya-convert.',
    version='0.1',
    py_modules=['esprovision'],
    packages=find_packages(),  # list of all packages
    install_requires=install_requires,
    entry_points='''
        [console_scripts]
        esprovision=esprovision:provision
    ''',
    author="Jacob Rodgers",
    keyword="esphome, tuya-convert, provision, cli",
    long_description=README,
    long_description_content_type="text/markdown",
    license='MIT',
    url='https://github.com/yudjinn/esprovision',
    author_email='yudjinncoding@gmail.com',
)
