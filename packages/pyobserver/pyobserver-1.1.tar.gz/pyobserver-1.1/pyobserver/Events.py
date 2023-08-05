import threading
from abc import ABC, abstractmethod


class BaseEvent(ABC):
    """Base event class to pass along to listeners a easy-to-read argument"""
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @abstractmethod
    def get_event_name(self) -> str:
        pass


class Observer(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def callback(self, caller, args):
        pass


class Observable(ABC):
    """Base observable class that describes an observable object. It contains all logic to manage its listeners"""
    def __init__(self):
        super().__init__()
        self.__listeners = []
        self.__lock = threading.RLock()

    def notify_listeners(self, event: BaseEvent):
        """Notifies all listeners of this Observable
        :param event: An event that will be pass along to the listeners of this Observable
        """
        self.__lock.acquire()
        try:
            listener: Observer
            for listener in self.__listeners:
                listener.callback(self, event)
        finally:
            self.__lock.release()

    def add_listener(self, listener: Observer):
        """Adds a Observer object as a listener to this Observable
        :param listener: The Observer object to be added to the listeners list for this Observable
        """
        self.__listeners.append(listener)

    def remove_listener(self, listener: Observer):
        """Removes a Observer object from the listeners list for this Observable
        :param listener: The Observer object to be removed from the listeners list for this Observable
        """
        self.__listeners.remove(listener)
