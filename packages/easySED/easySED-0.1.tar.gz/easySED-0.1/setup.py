import setuptools

# include additional packages as well - requests , tabulate , json

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easySED", # Replace with your own username
    version="0.1",
    author="Harsh Native",
    author_email="Harshnative@gmail.com",
    description="This module to used to add military level encryption system to your project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/harshnative/easy-secure-encryptor-decryptor-module_python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "onetimepad", "cryptography" ,
    ]
)