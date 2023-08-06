from marshmallow import Schema as Schema_
from typing import ClassVar, Type, Optional, List
from marshmallow_dataclass import dataclass as ma_dataclass
from dataclasses import field


@ma_dataclass
class PatientCard:
    patient_ids: List[int] = field(metadata=dict(data_key="patientIds"))
    name: str
    container_id: str = field(metadata=dict(data_key="containerId"))
    dataset_release_id: str = field(metadata=dict(data_key="dataSetReleaseIdentifier"))
    dataset_schema: str = field(metadata=dict(data_key="dataSetSchema"))
    description: Optional[str] = ""
    id: Optional[int] = None
    asset_id: Optional[str] = None
    Schema: ClassVar[Type[Schema_]] = Schema_  # needed for type checking
