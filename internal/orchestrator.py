from pydantic import BaseModel
from typing import Dict
from .redis_db import get_scenario, create_scenario, update_scenario
from .state_machine import StateMachine
from .kafka_pc import KafkaProducer, KafkaConsumer


class Orchestrator:
    def __init__(self, kafka_producer: KafkaProducer, kafka_consumer: KafkaConsumer):
        self.state_machine = StateMachine()
        self.kafka_producer = kafka_producer
        self.kafka_consumer = kafka_consumer

    def get_scenario(self, scenario_id: int):
        """
        Получение информации о сценарии.
        """
        scenario_data = get_scenario(scenario_id)
        if not scenario_data:
            raise ValueError(f"Scenario {scenario_id} not found in Redis")
        return scenario_data

    def create_scenario(self, scenario_id: int, name: str, parameters: dict):
        """
        Создание нового сценария.
        """
        scenario_data = create_scenario(scenario_id, name, parameters)
        return scenario_data

    def change_scenario_state(self, scenario_id: int, new_state: str):
        """
        Изменение состояния сценария с помощью стейт-машины и обновление в Redis.
        """
        try:
            # Используем стейт-машину для изменения состояния
            self.state_machine.change_state(scenario_id, new_state)

            # Обновляем состояние сценария в Redis
            scenario_data = update_scenario(scenario_id, state=new_state)
            if not scenario_data:
                raise ValueError(f"Failed to update state for Scenario {scenario_id}")
            return scenario_data
        except Exception as e:
            raise ValueError(f"Error changing state: {e}")
