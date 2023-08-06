from setuptools import setup, find_packages


try:
    with open("README.md", "r") as readme:
        long_description = readme.read()
except:
    long_description = "Library for easier translating book pages in png."

setup(
    name="easyepub",
    version="0.0.1",
    description="Library for easier translating book pages in png.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="xcaq",
    author_email="swipduces@yandex.com",
    python_requires=">=3.6.0",
    url="https://github.com/xcaq/easyepub",
    packages=find_packages(),
    install_requires=["pydantic", "WeasyPrint", "lxml", "Pillow"],
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ]
)
