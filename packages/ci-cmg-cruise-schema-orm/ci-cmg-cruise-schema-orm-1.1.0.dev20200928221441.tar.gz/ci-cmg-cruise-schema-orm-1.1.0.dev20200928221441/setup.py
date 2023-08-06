import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

with open('requirements.txt') as f:
  requirements = f.read().splitlines()

setuptools.setup(
  name="ci-cmg-cruise-schema-orm",
  version="1.1.0.dev20200928221441",
  description="ORM classes for the cruise schema",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/ci-cmg/cruise-schema-orm-py",
  package_dir={'': 'src'},
  packages=setuptools.find_packages('src'),
  classifiers=[
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: Jython",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires='>=2.7',
  install_requires=[req for req in requirements if req[:2] != "# "]
)