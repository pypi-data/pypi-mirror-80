import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-nabu", # Replace with your own username
    version="0.1.0",
    author="Tim Guicherd",
    author_email="tim@grut.org",
    description="A small and efficient Markdown to HTML publishing platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/timoguic/nabu",
    packages=setuptools.find_packages(),
    install_requires=[
        'markdown2',
        'Jinja2',
        'PyYAML',
        'watchgod',
    ],
    entry_points={
        'console_scripts': ['nabu=nabu.__main__:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)