from setuptools import setup, find_packages
import os

with open(os.path.join(os.path.dirname(__file__), "infi", "dtypes", "nqn", "__version__.py")) as version_file:
    exec(version_file.read()) # pylint: disable=W0122

setup(name="infi.dtypes.nqn",
      classifiers=[
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
      ],
      description="Datatype for NQN",
      license="PSF",
      author="Leonid Genkin",
      author_email="lgenkin@infinidat.com",
      url="https://github.com/infinidat/infi.dtypes.nqn",
      version=__version__, # pylint: disable=E0602
      packages=find_packages(exclude=["tests"]),
      namespace_packages=["infi", "infi.dtypes"],
      zip_safe=False,
)