__version__ = "0.1.1"

__all__ = ["AWResourcesClient"]

try:
    # Attempts to import the client class
    # Allowed to fail importing so the package metadata can be read for building
    from .analytic_workbench_clients import AWResourcesClient
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass  # pragma: no cover
