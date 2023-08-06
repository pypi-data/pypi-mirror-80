import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='PyUnleashed',
     version='1.0.3',
     author="John Horton",
     author_email="pyunleashed@outlook.com",
     description="A wrapper with a couple of utility functions for the Unleashed Software API",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://www.adminify.me",
     license='LICENSE.txt',
     packages=setuptools.find_packages(),
     install_requires=[
        'requests'
     ],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
