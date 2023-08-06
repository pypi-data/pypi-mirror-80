import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="image-compare-RohanTrix", # Replace with your own username
    version="0.0.2",
    author="Rohan Sirohia",
    author_email="rohanyehyeah@gmail.com",
    description="Applies FLANN based feature matching between two images and return a similarity percentage.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RohanTrix/Image-Compare",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)