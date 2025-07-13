from pydantic import BaseModel, ConfigDict


class TaskMultifactorRelevancyDataModel(BaseModel):
    query: str
    title: str
    cpu: str
    ram: str
    storage: str
    gpu: str

    model_config = ConfigDict(from_attributes=True)

class TaskCommentAttitudeDataModel(BaseModel):
    comment: str

    model_config = ConfigDict(from_attributes=True)

class TaskStatementsLogicalConnectionDataModel(BaseModel):
    statement1: str
    statement2: str

    model_config = ConfigDict(from_attributes=True)

class TaskGenreAndStyleDefinitionDataModel(BaseModel):
    text: str

    model_config = ConfigDict(from_attributes=True)