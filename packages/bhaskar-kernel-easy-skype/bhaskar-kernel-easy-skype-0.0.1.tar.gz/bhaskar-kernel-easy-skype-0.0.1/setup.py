import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="bhaskar-kernel-easy-skype",  # Replace with your own username
    version="0.0.1",
    author="Bhaskar Singh",
    author_email="bhaskar.kernel@gmail.com",
    description="A simple skype file downloader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/algorithmgeeker/easy_skype",
    install_requires=[
        'requests',
        'tqdm',
        'argparse',
        'skpy',
        'rich'
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['easy_skype=skype_downloader.skype_main:main']
    },
    python_requires='>=3.6',
)
