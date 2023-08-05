# replace:
# <your_package> with your actual package name.
# <you> with your name.
# <your_email> with your public email address.
# <your_github_repo_url> with your github project's url.
from setuptools import setup, find_packages

s = setup(
    name="tsemodule",
    version="1.0.0",
    license="MIT",
    description="",
    url="https://github.com/mohammadmaso/tsemodule",
    packages=find_packages(),
    install_requires=[
        'pandas',
        ],
    python_requires = ">= 3.4",
    author="Sadiq Karimi",
    author_email="m.mh.itg@gmail.com",
    
    )