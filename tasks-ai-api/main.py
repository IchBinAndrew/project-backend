from fastapi import FastAPI


app = FastAPI()

@app.get("/pred")
async def get_prediction(task_id: int):
    return "✅"