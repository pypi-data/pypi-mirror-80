import setuptools

with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()
setuptools.setup(
    name="Otpwd",
    version="0.0.6",
    author='v-k',
    author_email="vvvkkk1960@outlook.com",
    description="Dynamic encryption software program",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        
    ],
)
