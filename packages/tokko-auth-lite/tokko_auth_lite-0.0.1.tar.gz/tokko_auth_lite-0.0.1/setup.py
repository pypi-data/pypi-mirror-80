import os
from setuptools import find_packages, setup

readme_file = os.path.join(os.path.dirname(__file__), 'README.md')

with open(readme_file) as readme:
    README = f"{readme.read()}"

README = README.replace(README.split('# Install')[0], '')

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(

    name="tokko_auth_lite",
    version="0.0.1",
    license="BSD License",
    packages=find_packages(),
    include_package_data=True,
    description="Tokko Auth2 flavor.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/TokkoLabs/auth-plugins/tokko_auth_lite.git",
    author="Jose Salgado",
    author_email="jsalgado@navent.com",

    install_requires=[
        "arrow",
        "pyjwt",
        "pycrypto",
        "python-jwt",
        "python-jose",
        "PyCryptodome",
    ],

    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
