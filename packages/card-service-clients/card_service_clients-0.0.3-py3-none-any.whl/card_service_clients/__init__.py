__version__ = "0.0.3"

__all__ = ["CardServicePatientCardClient", "PatientCard"]

try:
    # Attempts to import the client class
    # Allowed to fail importing so the package metadata can be read for building
    from .patient_card_client import CardServicePatientCardClient
    from .models import PatientCard
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass  # pragma: no cover
