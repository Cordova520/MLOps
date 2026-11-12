from setuptools import setup, find_packages

with open("requirements.txt", "r") as file:
    requirements = [line for line in file.read().split("\n")]

setup(
    name="summarize",
    description="Demo python CLI Tool to summartize text using HuggingFace Transformers",
    packages=find_packages(),
    author="Daniel Cordova",
    entry_points="""
    [console_scripts]
    summarize=summarize.main:main""",
    install_requires=requirements,
    version="0.0.1",
    url="https://github.com/Cordova520/MLOps/tree/main/python_essentials/HUGGINGFACE_SUMMARIZATION",
)   