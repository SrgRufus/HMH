# handlers.central_event_handler.py
import logging
from typing import Callable, Dict, List
# importera 'event' hanterare
from handlers.events.event_tasks import TaskCreatedEvent

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class CentralEventHandler:
    def __init__(self):
        self._events: Dict[str, List[Callable]] = {
            "task_created": []
        }
        # Registrerar  automatiskt "core events"
        self.register_handler("task_created", TaskCreatedEvent().handle)

    def register_handler(self, event_name: str, handler: Callable):
        if event_name not in self._events:
            self._events[event_name] = []
        self._events[event_name].append(handler)
        logging.debug(f"Handler registered for event: {event_name}")

    def trigger_event(self, event_name: str, data: dict, *args, **kwargs):
        if event_name in self._events:
            for handler in self._events[event_name]:
                try:
                    handler(data, *args, **kwargs)
                except Exception as e:
                    logging.error(f"Error while handling event '{event_name}': {e}")
        else:
            logging.warning(f"No handlers registered for event: {event_name}")

# Create a global EventHandler instance
event_handler = CentralEventHandler()
