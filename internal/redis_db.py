import redis
import json
from typing import Dict

# Подключение к Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def create_scenario(scenario_id: int, name: str, parameters: Dict[str, str]):
    scenario_key = f"scenario_id:{scenario_id}"
    
    scenario_data = {
        "name": name,
        "state": "inactive",
    }
    scenario_data.update(parameters)
    
    # Сохраняем данные в Redis
    redis_client.set(scenario_key, json.dumps(scenario_data))
    return

def get_scenario(scenario_id: int):
    scenario_key = f"scenario_id:{scenario_id}"
    scenario_data = redis_client.get(scenario_key)
    if scenario_data:
        return json.loads(scenario_data)
    return None

def update_scenario(scenario_id: int, state: str = None, **parameters):
    scenario_key = f"scenario_id:{scenario_id}"
    scenario_data = get_scenario(scenario_id)
    if scenario_data:
        if state is not None:
            scenario_data["state"] = state
        if parameters:
            scenario_data.update(parameters)
        redis_client.set(scenario_key, json.dumps(scenario_data))
        return scenario_data
    return None
