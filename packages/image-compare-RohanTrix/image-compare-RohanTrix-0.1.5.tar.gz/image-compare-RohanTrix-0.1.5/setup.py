import setuptools

setuptools.setup(
    name="image-compare-RohanTrix", # Replace with your own username
    version="0.1.5",
    author="Rohan Sirohia",
    author_email="rohanyehyeah@gmail.com",
    description="Applies FLANN based feature matching between two images and return a similarity percentage.",
    url="https://github.com/RohanTrix/Image-Compare",
    packages=['src'],
    license = 'MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)