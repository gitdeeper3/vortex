import sys

class ImportPatcher:
    def __init__(self):
        self.patched_modules = {}
        
    def find_spec(self, fullname, path, target=None):
        if fullname in ['cartopy', 'metpy', 'netCDF4', 'sklearn', 'tensorflow', 'h5py']:
            print(f"Patched import: {fullname}")
            # Create empty module
            from importlib.util import spec_from_loader, module_from_spec
            from importlib.machinery import ModuleSpec
            
            spec = ModuleSpec(fullname, None)
            module = module_from_spec(spec)
            module.__file__ = f"<patched {fullname}>"
            module.__version__ = "1.0.0"
            
            # Add to sys.modules
            sys.modules[fullname] = module
            return spec
            
sys.meta_path.insert(0, ImportPatcher())
