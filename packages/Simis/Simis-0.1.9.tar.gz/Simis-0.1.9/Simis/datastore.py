import abc
import sys
import threading
import time
from typing import List

from Simis.Ashes import Model, Ashes


class Listener(metaclass=abc.ABCMeta):
    """
    Abstract class that automatically registers the Subclass with the Datastore so that it can be notified.
    """

    def __init__(self):
        DataStore.get_instance().register_listener(self)

    @abc.abstractmethod
    def notify(self, model: Model) -> None:
        """
        Notifies the Listener with the updated model from Ashes.
        :return:
        """
        print("METHOD IS ABSTRACT AND NOT IMPLEMENTED IN BASECLASS")


class RnaController(Listener, metaclass=abc.ABCMeta):
    """
    Abstract class that automatically registers the Subclass with the Datastore so that it can notified.
    In addition the name for the RNA is set.
    """

    def __init__(self, rna_nr: int = 0):
        """

        :param rna_nr: Number of the RNA. 0 if only 1 RNA in the structure.
        """
        super().__init__()
        if rna_nr == 0:
            self.rna_name = "RNA"
        else:
            self.rna_name = "RNA" + str(rna_nr)


class DataStore:
    """
    Manages the connection of multiple python scripts over the same connection with Ashes.
    The DataStore caches the newest model from Ashes and provides it to the objects that are listening for updates.
    """
    instance = None  # type:DataStore
    initialized = False  # type:bool
    server_name = ""  # type:str

    def __init__(self):
        self.listeners = []  # type: List[Listener]
        self.model = None  # type:Model
        self.maxTimeout = 30000  # type:int
        self.debugModeOn = False  # type:bool

    def update(self, model: Model) -> Model:
        """
        This method is to be called from the Ashes package.
        :param model: The new model
        :return:
        """
        self.model = model
        if not self.initialized:
            self.initialized = True
            return self.model

        for listener in self.listeners:
            listener.notify(self.model)
        return self.model

    def get_model(self) -> Model:
        """
        :return: The currently cached instance of the Model sent by Ashes.
        """
        return self.model

    def register_listener(self, listener: Listener) -> None:
        """
        Registers a new object to listen on updates of the Ashes Model.
        :param listener: The new listener
        :return:
        """
        self.listeners.append(listener)

    def unregister_listener(self, listener: Listener) -> bool:
        """
        Unregisters the object from the DataStore if it is registered beforehand.
        :param listener: The listener to remove
        :return: True if was in list. False if it was not.
        """
        wasin = listener in self.listeners
        if wasin:
            self.listeners.remove(listener)
        return wasin

    @classmethod
    def get_instance(cls) -> 'DataStore':
        """
        :return: The current instance of the DataStore.
        """
        return cls.instance

    @classmethod
    def __start_connection(cls) -> None:
        """
        Starts the connection with Ashes and should be called in a separate thread.
        :return:
        """
        a = Ashes(maxTimeout=DataStore.instance.maxTimeout, debugModeOn=DataStore.instance.debugModeOn)

        def update_model_inner(model):
            return DataStore.instance.update(model)

        if len(sys.argv) >= 2:
            a.connect(update_model_inner)
        elif cls.server_name:
            a.connect(update_model_inner, cls.server_name)
        else:
            a.connect(update_model_inner, "ASHES-SERVER")

    @classmethod
    def start_connection(cls, server_name: str = "") -> None:
        """
        Starts the connection with Ashes.
        :param server_name: Server name to use
        :return:
        """
        cls.server_name = server_name
        threading.Thread(target=DataStore.__start_connection).start()
        time.sleep(0.4)


DataStore.instance = DataStore()
