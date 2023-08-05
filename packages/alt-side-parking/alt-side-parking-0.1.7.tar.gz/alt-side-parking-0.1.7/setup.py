from setuptools import find_packages, setup

######

CLASSIFIERS = [
    "Programming Language :: Python",
    "License :: OSI Approved :: MIT License",
]
DESCRIPTION = ""
KEYWORDS = ["python"]
URL = ""
AUTHOR = "Salah Ahmed"
AUTHOR_EMAIL = "salahs.email@pm.me"

REQUIREMENTS = [
    "arrow",
    "phonenumbers",
    "structlog",
    "twilio",
    "salahs-twitterbot>=1.3.0,<2.0",
]
TEST_REQUIREMENTS = [
    "automock",
    "coverage[toml]",
    "pytest-cov",
    "pytest-freezegun",
]
DEV_REQUIREMENTS = [
    "black",
    "flake8",
    "ipython",
    "pdbpp",
    "pre-commit",
    "tox",
]

#####

with open("README.rst", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="alt-side-parking",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    classifiers=CLASSIFIERS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    keywords=KEYWORDS,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    extras_require={
        "test": TEST_REQUIREMENTS,
        "dev": TEST_REQUIREMENTS + DEV_REQUIREMENTS,
    },
    entry_points=(
        """
[console_scripts]
remindme = alt_side_parking.scripts.reminder:main
"""
    ),
)
