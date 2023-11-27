from setuptools import setup, find_namespace_packages


setup(
name = "clean_sort_package_main",
version = "0.0.1",
description = "A small clean sorted package",
author = 'Elena Polkhova',
author_email= 'ukr-towar@ukr.net',
readme = "README.md",
url = 'https://github.com/ElenaPolkhovaS/dz_sort',
license='MIT',
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
],   
include_package_data=True,
entry_points = {'console_scripts': [
    'clean_folder = clean_folder.clean:main']}
)








