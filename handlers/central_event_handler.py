# handlers.central_event_handler.py : Centraliserar eventhantering.
import logging
from typing import Callable, Dict, List

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class CentralEventHandler:
    def __init__(self):
        self._events = {}
        self.handlers: Dict[str, List[Callable]] = {}

    # Registrerar en hanterare för ett specifikt event.
    def register_handler(self, event_name, handler):
        if event_name not in self._events:
            self._events[event_name] = []
        self._events[event_name].append(handler)
        logging.debug(f"Handler registered for event: {event_name}")

    # Utlöser eventet och anropar alla registrerade hanterare.
    def trigger_event(self, event_name, *args, **kwargs):
        if event_name in self._events:
            for handler in self._events[event_name]:
                try:
                    handler(*args, **kwargs)
                except Exception as e:
                    logging.error(f"Error while handling event '{event_name}': {e}")
        else:
            logging.warning(f"No handlers registered for event: {event_name}")


# Skapa en global EventHandler-instans
event_handler = CentralEventHandler()

