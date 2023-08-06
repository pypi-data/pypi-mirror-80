from setuptools import setup, find_packages


setup(
    name="marsggbo", # Replace with your own username
    version="0.1",
    author="marsggbo",
    author_email="csxinhe@comp.hkbu.edu.hk",
    description="The boss of MARS Church",
    long_description='''I'm your boss: marsggbo''',
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests", "projects")),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)