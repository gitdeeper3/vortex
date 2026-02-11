from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
long_description = fh.read()

setup(
name="vortex",
version="1.0.0",
author="Samir Baladi",
author_email="gitdeeper@gmail.com",
description="Multi-Parameter Assessment Protocol for Tropical Cyclone Rapid Intensification",
long_description=long_description,
long_description_content_type="text/markdown",
url="https://gitlab.com/gitdeeper3/vortex",
project_urls={
"GitLab": "https://gitlab.com/gitdeeper3/vortex",
"Codeberg": "https://codeberg.org/gitdeeper2/vortex/",
"Bitbucket": "https://bitbucket.org/gitdeeper3/vortex/",
"PyPI": "https://pypi.org/project/vortex/",
"Bug Tracker": "https://gitlab.com/gitdeeper3/vortex/-/issues",
"Documentation": "https://gitlab.com/gitdeeper3/vortex/-/tree/main/docs",
},
classifiers=[
"Programming Language :: Python :: 3",
"Programming Language :: Python :: 3.8",
"Programming Language :: Python :: 3.9",
"Programming Language :: Python :: 3.10",
"Programming Language :: Python :: 3.11",
"Programming Language :: Python :: 3.12",
"License :: OSI Approved :: MIT License",
"Operating System :: OS Independent",
"Development Status :: 4 - Beta",
"Intended Audience :: Science/Research",
"Topic :: Scientific/Engineering :: Atmospheric Science",
"Topic :: Scientific/Engineering :: Artificial Intelligence",
],
package_dir={"": "src"},
packages=find_packages(where="src"),
python_requires=">=3.8",
install_requires=[
"numpy>=1.21.0",
"pyyaml>=6.0.0",
],
extras_require={
"dev": [
"pytest>=7.0.0",
"pytest-cov>=4.0.0",
"black>=23.0.0",
"flake8>=6.0.0",
"mypy>=1.0.0",
],
"docs": [
"sphinx>=7.0.0",
"sphinx-rtd-theme>=1.3.0",
"myst-parser>=2.0.0",
],
"full": [
"scipy>=1.7.0",
"xarray>=0.20.0",
"matplotlib>=3.4.0",
"netCDF4>=1.5.0",
"h5py>=3.0.0",
],
},
entry_points={
"console_scripts": [
"vortex-forecast=vortex_operational:main",
"vortex-reports=report_manager:main",
],
},
include_package_data=True,
keywords="meteorology tropical-cyclones forecasting rapid-intensification",
)
