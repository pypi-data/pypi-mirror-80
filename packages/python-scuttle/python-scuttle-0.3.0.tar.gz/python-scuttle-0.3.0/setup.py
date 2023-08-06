try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='python-scuttle',
    use_scm_version=True,
    packages=['scuttle', 'scuttle.versions'],
    url="http://github.com/scuttle/python-scuttle",
    license="MIT",
    author="Ross Williams",
    author_email="ross@rossjrw.com",
    description="Python wrapper for SCUTTLE API.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    setup_requires=["setuptools_scm"],
    install_requires=["requests", "wrapt"],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.8',
)
