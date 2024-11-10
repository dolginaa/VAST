from .redis_db import get_scenario

class StateMachine:
    def __init__(self):
        self.state_dict = {
            "init_startup": "Initializing startup",
            "in_startup_processing": "Processing startup",
            "init_shutdown": "Initializing shutdown",
            "in_shutdown_processing": "Processing shutdown",
            "active": "Active",
            "inactive": "Inactive",
        }
        
        # Словарь для обработки переходов
        self.transitions = {
            ("inactive", "init_startup"): self.startup,
            ("init_startup", "in_startup_processing"): self.processing_startup,
            ("in_startup_processing", "active"): self.activate,
            ("active", "init_shutdown"): self.shutdown,
            ("init_shutdown", "in_shutdown_processing"): self.processing_shutdown,
            ("in_shutdown_processing", "inactive"): self.deactivate,
        }

    def change_state(self, scenario_id: int, new_state: str):
        """
        Изменение состояния сценария.
        """ 
        current_state = self.get_current_state(scenario_id)
        if current_state not in self.state_dict:
            raise ValueError(f"Scenario {scenario_id} not found in Redis")
        
        # Проверяем, что новое состояние корректно
        if new_state not in self.state_dict:
            raise ValueError(f"Invalid state: {new_state}")
        
        # Пытаемся найти и выполнить переход, если он существует
        transition = (current_state, new_state)
        if transition in self.transitions:
            print(f"Changing state of scenario {scenario_id} from {current_state} to {new_state}")
            self.transitions[transition](scenario_id)
        else:
            raise ValueError(f"Can't change state from {current_state} to {new_state}")

    def get_current_state(self, scenario_id: int):
        """
        Возвращает текущее состояние сценария.
        """
        scenario_data = get_scenario(scenario_id)
        if not scenario_data:
            raise ValueError(f"Scenario {scenario_id} not found in Redis")
        cur_state = scenario_data["state"]
        return cur_state

    def startup(self, scenario_id: int):
        print(f"Scenario {scenario_id} is starting up.")
        # Логика старта

    def processing_startup(self, scenario_id: int):
        print(f"Scenario {scenario_id} is processing startup.")
        # Логика промежуточного состояния старта

    def activate(self, scenario_id: int):
        print(f"Scenario {scenario_id} is now active.")
        # Логика активации сценария

    def shutdown(self, scenario_id: int):
        print(f"Scenario {scenario_id} is shutting down.")
        # Логика остановки

    def processing_shutdown(self, scenario_id: int):
        print(f"Scenario {scenario_id} is processing shutdown.")
        # Логика промежуточного состояния остановки

    def deactivate(self, scenario_id: int):
        print(f"Scenario {scenario_id} is now inactive.")
        # Логика завершения работы
