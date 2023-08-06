import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Market-Analytics",
    version="0.0.8",
    author="Wesley Laurence",
    author_email="wesleylaurencetech@gmail.com",
    description="Toolkit for Stock Market analysis and visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wesleyLaurence/Stock-Market-Analytics",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
	package_data={'': ['data/*.csv']},
    install_requires = [
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
        'pymongo',
        'yahoo-fin',
        'flask',
        'werkzeug',
        'cryptography',
        'tweepy',
        'wikipedia'
    ] 
)