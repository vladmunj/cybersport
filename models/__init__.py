import importlib
import pkgutil
from models.base import Base

for module in pkgutil.iter_modules(__path__):
    if module.name == 'base': continue
    importlib.import_module(
        f"{__name__}.{module.name}"
    )