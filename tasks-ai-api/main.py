from fastapi import FastAPI
from aiokafka import AIOKafkaProducer
from contextlib import asynccontextmanager
from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from enums import TaskCategoryEnum
from pydantic_models import TaskMultifactorRelevancyDataModel
from functools import partial
from launch_laptop_recommendation import predict_from_input as laptop_recommendation
import asyncio
import uvicorn


class TaskModel(BaseModel):
    id: int
    assigned_user_id: Optional[int]
    category: TaskCategoryEnum
    data_json: dict[str, Any]

    file_key_1: Optional[str]
    file_key_2: Optional[str]

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

class PredictionModel(BaseModel):
    task_id: int
    prediction: str

    model_config = ConfigDict(from_attributes=True)

producer = None

async def get_producer():
    global producer
    if producer is None:
        producer = AIOKafkaProducer(
            bootstrap_servers="kafka:9092",
            acks='all',  # Wait for all replicas to acknowledge
            enable_idempotence=True  # Prevent message duplication
        )
        await producer.start()
    return producer

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Trying to create kafka producer task")
    try:
        await get_producer()
        # asyncio.create_task(process_messages())  # Run in background
    except Exception as e:
        print(f"Error when trying to initialize task: {e}")
    yield
    if producer:
        await producer.stop()


async def predict_laptop_relevancy(task_id: int, data: TaskMultifactorRelevancyDataModel):
    producer = await get_producer()
    prediction = await asyncio.get_event_loop().run_in_executor(
        None,  # Uses default ThreadPoolExecutor
        partial(laptop_recommendation,
            data.query,
            data.title,
            data.cpu,
            data.ram,
            data.storage,
            data.gpu
        )  # Partial binds args
    )
    print(prediction)
        # 3. Publish result async (non-blocking)
    await producer.send(
        'ai_predictions',
        value=PredictionModel(task_id=task_id, prediction=prediction).model_dump_json().encode('utf-8')
    )


app = FastAPI()

@app.post("/pred")
async def get_prediction(task: TaskModel):
    if task.category == TaskCategoryEnum.MULTIFACTOR_RELEVANCY:
        data = TaskMultifactorRelevancyDataModel.model_validate(task.data_json)
        coro = predict_laptop_relevancy(task_id=task.id, data=data)
        asyncio.create_task(coro)
    return "OK"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7070)