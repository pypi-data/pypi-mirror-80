import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="boilerplate_django_rest_api",
    version="0.8.0",
    description="A Django app to build REST API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ravuthz/django_boilerplate/tree/rest",
    author="Ravuthz",
    author_email="ravuthz@gmail.com",
    license="MIT",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    # packages=["reader"],
    include_package_data=True,
    install_requires=[
        'constance',
        'dj_database_url',
        'django_extensions',
        'rest_framework',
        'rest_auth',
        'oauth2_provider',
        'corsheaders',
        'drf_yasg',
    ],
    # entry_points={
    #     "console_scripts": [
    #         "realpython=reader.__main__:main",
    #     ]
    # },
)