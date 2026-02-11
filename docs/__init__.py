"""
Documentation for the Vortex framework.

Contains user guides, API references, scientific documentation,
and technical specifications for the Vortex forecasting system.
"""

__version__ = "1.0.0"
__description__ = "Documentation for Vortex framework"

# Documentation sections
DOC_SECTIONS = [
    'installation',
    'api_reference',
    'scientific_methodology',
    'validation_results',
    'citation_guide'
]

def get_doc_path(section=''):
    """Get path to documentation directory or section"""
    import os
    docs_dir = os.path.dirname(__file__)
    if section:
        return os.path.join(docs_dir, section)
    return docs_dir

__all__ = ['get_doc_path', 'DOC_SECTIONS']
