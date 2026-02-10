# 📦 Vortex Installation Guide

## System Requirements
- **Python**: 3.8 or higher
- **Termux**: Latest version (for Android installation)
- **Storage**: ~50MB free space
- **Memory**: 256MB RAM minimum

## 🚀 Quick Installation

### For Termux/Android:
```bash
# Update packages
pkg update && pkg upgrade

# Install Python and pip
pkg install python python-pip

# Install core dependencies
pip install numpy pyyaml

# Clone vortex repository
git clone https://gitlab.com/gitdeeper3/vortex.git
cd vortex

# Install vortex in development mode
pip install -e .
```

For Linux/macOS:

```bash
# Ensure Python 3.8+ is installed
python3 --version

# Install pip if not present
sudo apt-get install python3-pip  # Ubuntu/Debian
# or
brew install python3              # macOS

# Install dependencies
pip3 install numpy pyyaml

# Clone and install vortex
git clone https://gitlab.com/gitdeeper3/vortex.git
cd vortex
pip3 install -e .
```

🔧 Manual Installation (Advanced)

Step 1: Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv vortex_env
source vortex_env/bin/activate  # Linux/macOS
# or
vortex_env\Scripts\activate     # Windows

# Install required packages
pip install numpy>=1.21.0 pyyaml>=6.0.0
```

Step 2: Install Vortex Package

```bash
# Method 1: Editable installation (for development)
pip install -e .

# Method 2: Regular installation
python setup.py install

# Method 3: From source
python -m pip install .
```

📊 Verification

After installation, verify everything works:

```bash
# Test import
python -c "import vortex; print('✅ vortex imported successfully')"

# Run test suite
python run_tests.py

# Expected output:
# ✅ 14/14 tests passed
```

🐛 Troubleshooting

Common Issues:

1. ImportError: No module named 'numpy'
   ```bash
   pip install numpy
   # or on Termux:
   pkg install python-numpy
   ```
2. Permission denied errors
   ```bash
   # Use virtual environment
   python -m venv myenv
   source myenv/bin/activate
   pip install -e .
   ```
3. ModuleNotFoundError for vortex
   ```bash
   # Ensure you're in the vortex directory
   cd /path/to/vortex
   # Reinstall in development mode
   pip install -e .
   ```
4. Termux storage issues
   ```bash
   # Grant storage permissions
   termux-setup-storage
   # Install in home directory
   cd ~
   git clone https://gitlab.com/gitdeeper3/vortex.git
   ```

Platform-Specific Notes:

Termux/Android:

· Use pkg install for system packages
· Install in ~ for best compatibility
· May need additional permissions for file operations

Windows:

· Use Python from python.org or Microsoft Store
· May need to add Python to PATH
· Consider using WSL for better compatibility

macOS:

· Homebrew is recommended for package management
· May need to install Xcode Command Line Tools

📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Open an issue on GitLab: https://gitlab.com/gitdeeper3/vortex/-/issues
3. Ensure your GitLab repository exists and is accessible
