import setuptools

setuptools.setup(
    name="toolstack",
    version="0.1.5",
    author="Mohammed Yusuf Khan",
    author_email="hello@mykhan.me",
    description="A collection of useful tools to speed-up the data processing, cleaning and pipelining.",
    url="https://github.com/getmykhan/toolstack",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=['toolkit', 'nlp', 'data cleaning', 'toolstack', 'data science', 'machine learning'],
    install_requires=['pandas', 'numpy', 'tqdm'],
    python_requires='>=3.7',
)
