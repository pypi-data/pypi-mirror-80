from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
        name="pieoffice",
        description="A terminal based script converter for ancient (Proto-)Indo-European languages.",
        url="https://gitlab.com/caiogeraldes/pieoffice",
        long_description=long_description,
        long_description_content_type="text/markdown",
        version="1.0.5",
        license="MIT",
        author="Caio Geraldes",
        author_email="caiogeraldes@protonmail.com",
        packages=find_packages(),
        entry_points={
        'console_scripts': [
           'pieoffice=pieoffice.__main__:main'
            ]
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        install_requires=['betacode'],
        python_requires=">=3.6",
)
