"""
Path utilities using relative paths for GitLab compatibility.
"""
import os
import sys
from pathlib import Path

def get_project_root() -> Path:
    """Get the project root directory using relative path."""
    # Get the directory containing this file
    current_file = Path(__file__).resolve()
    
    # Go up to project root (src/utils/ -> src/ -> project root)
    project_root = current_file.parent.parent.parent
    
    return project_root

def get_data_path(filename: str = "") -> Path:
    """Get path to data directory or specific data file."""
    project_root = get_project_root()
    data_dir = project_root / "data"
    
    if filename:
        return data_dir / filename
    return data_dir

def get_config_path(filename: str = "") -> Path:
    """Get path to config directory or specific config file."""
    project_root = get_project_root()
    config_dir = project_root / "config"
    
    if filename:
        return config_dir / filename
    return config_dir

def get_report_path(frequency: str = "daily", filename: str = "") -> Path:
    """Get path to reports directory or specific report file."""
    project_root = get_project_root()
    reports_dir = project_root / "reports" / frequency
    
    if filename:
        return reports_dir / filename
    return reports_dir

def get_src_path() -> Path:
    """Get path to src directory."""
    return get_project_root() / "src"

def get_tests_path() -> Path:
    """Get path to tests directory."""
    return get_project_root() / "tests"

def get_examples_path() -> Path:
    """Get path to examples directory."""
    return get_project_root() / "examples"

def get_docs_path() -> Path:
    """Get path to docs directory."""
    return get_project_root() / "docs"

# Make directories if they don't exist
def ensure_directories():
    """Ensure all necessary directories exist."""
    directories = [
        get_data_path(),
        get_config_path(),
        get_report_path("daily"),
        get_report_path("weekly"),
        get_report_path("monthly"),
        get_report_path("archived"),
        get_examples_path(),
        get_docs_path(),
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    
    print(f"✅ Directories ensured at: {get_project_root()}")

if __name__ == "__main__":
    ensure_directories()
