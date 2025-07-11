from pydantic import BaseModel, ConfigDict


class TaskMultifactorRelevancyDataModel(BaseModel):
    query: str
    title: str
    cpu: str
    ram: str
    storage: str
    gpu: str

    model_config = ConfigDict(from_attributes=True)