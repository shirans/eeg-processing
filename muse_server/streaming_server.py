from abc import abstractmethod


class StreamingServer(object):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
