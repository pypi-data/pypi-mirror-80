import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='tu_connect',
    version='1.0.0',
    author='Rogerio Domingues',
    author_email='rogerio.domingues@transunion.com',
    description=u'Connection to TU API BRZ',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://service.zipcode.com.br/api/help',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)