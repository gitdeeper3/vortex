# Vortex Framework
## Multi-Parameter Assessment Protocol for Tropical Cyclone Rapid Intensification

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active--development-orange)

## 📍 Repository Locations

This project is mirrored across multiple platforms:

- **Primary Repository**: https://gitlab.com/gitdeeper3/vortex
- **Mirrors**:
  - **Codeberg**: https://codeberg.org/gitdeeper2/vortex/
  - **Bitbucket**: https://bitbucket.org/gitdeeper3/vortex/
  - **PyPI**: https://pypi.org/project/vortex/

## Overview

The **Vortex Multi-Parameter Assessment Protocol** is an operational research framework for predicting Rapid Intensification (RI) in tropical cyclones.

## Core Parameters (8-Parameter Framework)

| # | Parameter | Symbol | Description |
|---|-----------|--------|-------------|
| 1 | Ocean Heat Content | OHC | Thermal energy in upper ocean |
| 2 | Eyewall Symmetry | σ_sym | Structural organization index |
| 3 | Vertical Wind Shear | VWS | 850-200 hPa wind difference |
| 4 | Mid-Level Humidity | RH_mid | 700-500 hPa relative humidity |
| 5 | Low-Level Vorticity | ζ_850 | 850 hPa relative vorticity |
| 6 | Convective Organization | Org_conv | Inner-core convection coherence |
| 7 | Outflow Efficiency | Eff_outflow | Upper-level ventilation |
| 8 | Intensity Trend | ΔInt_trend | 6-12h intensity changes |

## Quick Start

```bash
# Clone from any repository
git clone https://gitlab.com/gitdeeper3/vortex.git
cd vortex

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

Project Structure

```
vortex/
├── src/                    # Source code
├── data/                   # Data directory
├── config/                 # Configuration files
├── tests/                  # Test suite
├── reports/                # Report system
├── examples/               # Usage examples
└── docs/                   # Documentation
```

Installation

Basic Installation

```bash
pip install -r requirements.txt
pip install -e .
```

From PyPI

```bash
# Install from PyPI
pip install vortex

# Install specific version
pip install vortex==1.0.0
```

Usage

```python
from vortex.core.vortex_engine import VortexEngine
from vortex.algorithms.time_stepping import EnhancedTimeSteppingForecast

# Initialize engine for Atlantic basin
engine = VortexEngine(basin="atlantic")

# Initialize forecaster
forecaster = EnhancedTimeSteppingForecast()

# Generate forecast
forecast = forecaster.forecast_intensity(
    initial_intensity_kt=75.0,
    mpi_trajectory=[80.0, 85.0, 90.0, 95.0],
    environmental_trends={
        "vws": [12.0, 10.0, 8.0, 6.0],
        "sst": [28.5, 28.8, 29.0, 29.2]
    },
    time_horizon_hours=24
)

print(f"RI Probability: {forecast['ri_probability_time_series'][-1]:.1%}")
```

Documentation

Full documentation is available in the docs/ directory:

· API Reference
· Scientific Methodology
· Validation Results
· Installation Guides

Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting contributions.

License

This project is licensed under the MIT License - see the LICENSE file for details.

Citation and Distribution

📚 Academic Citation (Zenodo)

For academic publications, please cite using the Zenodo DOI:

```bibtex
@software{vortex_framework_2026,
  author = {Baladi, Samir},
  title = {Vortex Multi-Parameter Assessment Protocol for Tropical Cyclone Rapid Intensification},
  year = {2026},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.xxxxxxx},
  url = {https://doi.org/10.5281/zenodo.xxxxxxx},
  version = {1.0.0}
}
```

Zenodo Archive: https://zenodo.org/records/xxxxxxx

📦 Package Distribution (PyPI)

The Vortex package is available on PyPI:

```bash
# Install from PyPI
pip install vortex
```

PyPI Package: https://pypi.org/project/vortex/

Current Version: 1.0.0

PyPI Citation:

```bibtex
@software{vortex_pypi_2026,
  author = {Baladi, Samir},
  title = {vortex: Python package for tropical cyclone RI forecasting},
  year = {2026},
  publisher = {PyPI},
  url = {https://pypi.org/project/vortex/},
  version = {1.0.0}
}
```

🔗 Repository Citations

For referencing specific repository versions:

GitLab:

```bibtex
@software{vortex_gitlab_2026,
  author = {Baladi, Samir},
  title = {Vortex Framework - GitLab Repository},
  year = {2026},
  publisher = {GitLab},
  url = {https://gitlab.com/gitdeeper3/vortex},
  note = {Version 1.0.0, commit: [specific commit hash]}
}
```

Contact

Samir Baladi

· Role: Interdisciplinary AI Researcher, Scientific Software Developer
· Email: gitdeeper@gmail.com
· ORCID: 0009-0003-8903-0029
· Phone: +1-614-264-2074
· GitLab: @gitdeeper
· Research Interests: Applied AI/ML in geosciences, computational meteorology, scientific software development

Project Links

· GitLab (Primary): https://gitlab.com/gitdeeper3/vortex
· Codeberg: https://codeberg.org/gitdeeper2/vortex/
· Bitbucket: https://bitbucket.org/gitdeeper3/vortex/
· PyPI: https://pypi.org/project/vortex/
· Zenodo: https://zenodo.org/records/xxxxxxx
