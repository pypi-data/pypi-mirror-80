import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README.md file
README = (HERE / "README.md").read_text()

setup(
    name="bitmast_paystack",
    version="1.0a6",
    description="Python wrapper for PayStack Gateway API",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Bitmast Digital Services",
    author_email="bitmastdigital@gmail.com",
    license="APACHE",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
         'Topic :: Software Development :: Build Tools',

        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=['paystack', 'paystack/config', 'paystack/log', 'paystack/tests', 'paystack/util'],
    include_package_data=True,
    install_requires=['requests', 'design-pattern-toolkit']
)
