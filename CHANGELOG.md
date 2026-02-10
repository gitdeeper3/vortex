# Changelog

All notable changes to the `vortex-by-gitdeeper` project will be documented in this file.

The project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features
- GPU acceleration support for simulations
- Extended visualization capabilities
- Additional turbulence models
- Parallel processing support
- API documentation with Sphinx

## [0.2.0] - 2026-02-10

### ✨ Added
- **Complete PyPI metadata** with full project description
- **Comprehensive README.md** with badges and documentation
- **PyPI classifiers**: 
  - Development Status :: 3 - Alpha
  - Intended Audience :: Science/Research
  - Topic :: Scientific/Engineering :: Physics
  - Topic :: Scientific/Engineering :: Simulation
- **Search keywords**: vortex, simulation, cfd, fluid-dynamics, physics, scientific
- **Automatic badges**: Python Version, MIT License, PyPI Version
- **Project URLs**: GitLab repository link

### 📝 Updated
- **setup.py** with complete author information and metadata
- **Package structure** for better module organization
- **Import system** for reliable module loading
- **Documentation** with practical usage examples

### 🐛 Fixed
- **PyPI description issue** - Full description now displays correctly
- **Module import errors** in `src/__init__.py`
- **Package naming conflict** resolved with unique name

### 🔧 Technical Improvements
- **Build system**: Modern setuptools with `pyproject.toml`
- **Python compatibility**: >=3.8
- **Dependency management**: numpy>=1.20.0
- **Modular architecture**: Clean separation of concerns

## [0.1.0] - 2026-02-10

### 🚀 Initial Release
- **Core simulation algorithms**:
  - `TimeStepper`: Numerical integration algorithm
  - `VortexEngine`: Main simulation engine
- **Modular package structure**:
  - `algorithms/`: Numerical methods and solvers
  - `core/`: Core simulation engine and models
  - `io/`: Data input/output operations
  - `parameters/`: Simulation parameters and configurations
  - `utils/`: Utility functions and helpers
  - `visualization/`: Data visualization tools
- **Comprehensive test suite** (14 tests, all passing)
- **Initial PyPI publication**
- **GitLab repository integration**

### 📦 Packaging Foundation
- Basic `setup.py` configuration
- `pyproject.toml` for modern Python packaging
- Dual distribution: source (.tar.gz) and wheel (.whl)
- Minimal dependency specification

## Release Philosophy

### Version Numbering
- **MAJOR** version (X.0.0): Incompatible API changes
- **MINOR** version (0.X.0): New functionality (backward compatible)
- **PATCH** version (0.0.X): Bug fixes (backward compatible)

### Release Cycle
- **Alpha** (0.X.Y): Early development, API may change
- **Beta** (0.X.Y): Feature complete, testing phase
- **Stable** (1.0.0+): Production ready

## Acknowledgments

This project builds upon:
- Python scientific computing ecosystem
- Computational fluid dynamics research
- Open-source software best practices

---
*This changelog is maintained according to [Keep a Changelog](https://keepachangelog.com/) principles.*
