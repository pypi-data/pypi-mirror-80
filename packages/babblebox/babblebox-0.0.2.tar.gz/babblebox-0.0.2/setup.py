import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="babblebox",
    version="0.0.2",
    author="Mr.S Mechatronics",
    author_email="mr.smechatronics@gmail.com",
    description="An Ai Driven ChatBot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MrSMechatronics/ChatBox",
    packages=setuptools.find_packages(),
    install_requires=[
        'pikle'
        'nltk'
        'numpy'
        'tflearn'
        'tensorflow'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='<3.8',
)