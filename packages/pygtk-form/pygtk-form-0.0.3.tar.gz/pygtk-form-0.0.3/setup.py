import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pygtk-form",
    version="0.0.3",
    author="Olivier Cartier",
    author_email="cestoliv@chevro.fr",
    description="Create forms very easily for your scripts with GTK !",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cestoliv/pygtk_form",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[

    ],
    include_package_data = True
)
