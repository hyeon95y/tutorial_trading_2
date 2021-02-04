from abc import ABC
from abc import abstractmethod


class Pusher(ABC):
    @abstractmethod
    def send_message(self, thread, message):
        pass
