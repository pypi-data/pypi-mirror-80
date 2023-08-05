import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="DevConsole",
    version="0.2.2",
    author="JasonTheDev",
    author_email="examqiename@gmail.com",
    description="A Tkinter GUI Console For Executing Commands.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RandomLolKid/PyConsole",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.6',
)