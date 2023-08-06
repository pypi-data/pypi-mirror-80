import setuptools

with open("README.md", "r") as fh:
        long_description = fh.read()

setuptools.setup(
        name="tentacle-tentacle",
        version="0.0.4",
        author="Münch Willert",
        author_email="moritzmuench@mailbox.org",
        description="Manage sensors and measurements",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://willipink.eu/git/tentacle",
        packages=setuptools.find_packages(),
        classifiers=[
                    "Programming Language :: Python :: 3",
                    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                    "Operating System :: OS Independent",
                ],
        python_requires='>=3.7',
)
