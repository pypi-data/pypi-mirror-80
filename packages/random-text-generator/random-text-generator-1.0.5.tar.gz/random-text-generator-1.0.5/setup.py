from setuptools import find_packages, setup
import pathlib

HERE = pathlib.Path(__file__).parent

VERSION = '1.0.5'

PACKAGE_NAME = 'random-text-generator'

AUTHOR = 'LokotamaTheMastermind'

AUTHOR_EMAIl = 'lokotamathemastermind2@gmail.com'

URL = 'https://github.com/LokotamaTheMastermind/code-generator-using-python'

LICENSE = 'MIT'

DESCRIPTION = 'Generate short, simple text codes'

LONG_DESCRIPTION = (HERE / 'README.md').read_text()

LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
    'random-string',
    'url64'
]

DOWNLOAD_URL = "https://github.com/LokotamaTheMastermind/code-generator-using-python"

KEYWORDS = [
    'python',
    'generator',
    'code',
    'encode',
    'decode',
    'random'
]

setup(
    name=PACKAGE_NAME,  # package-name-username
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIl,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    url=URL,
    packages=find_packages(),
    python_requires='>=3.0',
    install_requires=INSTALL_REQUIRES,
    keywords=KEYWORDS,
    download_url=DOWNLOAD_URL
)
