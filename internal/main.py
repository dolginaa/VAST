from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from .orchestrator import Orchestrator
from .state_machine import StateMachine
from .redis_db import create_scenario
from typing import Dict
from .kafka_pc import KafkaProducer, KafkaConsumer
from videoanalytics.inference import Inference

# Пример модели для запроса с описанием сценария
class ChangeStateRequest(BaseModel):
    state: str
    scenario_id: int

    @validator("state")
    def validate_state(cls, v):
        if v not in {"start", "kill"}:
            raise ValueError("State must be 'start' or 'kill'")
        return v

# Модель для тела запроса
class ScenarioRequest(BaseModel):
    scenario_id: int
    name: str
    parameters: Dict[str, str]


app = FastAPI()
kafka_producer = KafkaProducer(bootstrap_servers="localhost:9092", topic_name="video_frames")
kafka_consumer = KafkaConsumer(bootstrap_servers="localhost:9092", topic_name="video_frames", group_id="inference_group")

# Создание экземпляров компонентов
orchestrator = Orchestrator(kafka_producer, kafka_consumer)
state_machine = StateMachine()
inference = Inference(kafka_consumer)

@app.get("/api/scenario")
async def get_scenario_info(scenario_id: int):
    try:
        scenario = orchestrator.get_scenario(scenario_id)
        return scenario
    except:
        raise HTTPException(status_code=404, detail="Scenario not found")

@app.post("/api/state")
async def change_state(state_request: ChangeStateRequest):
    try:
        orchestrator.change_scenario_state(state_request.scenario_id, state_request.state)
        return {"message": f"State of scenario {state_request.scenario_id} changed to {state_request.state}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/scenarios")
async def create_scenario_api(request: ScenarioRequest):
    create_scenario(request.scenario_id, request.name, request.parameters)
    return