from kivy.uix.widget import Widget
from kivy.properties import StringProperty, AliasProperty
from kivy.core.window import Window

import ntcore

from typing import Optional, Any



def topic_from_parts(self, value) -> bool:
    # leading forward slash is optional
    parts = value.removeprefix("/").rsplit("/", 1)
    if len(parts) > 1:
        self.table = parts[0]
    else:
        self.table = ""

    self.name = parts[-1]
    #  return True

class NTWidget(Widget):
    inst: ntcore.NetworkTableInstance
    sub: ntcore.Subscriber
    pub: ntcore.Publisher

    name = StringProperty(None)
    table = StringProperty(None)

    topic = AliasProperty(lambda self: f"/{self.table}/{self.name}", topic_from_parts)

    @classmethod
    def set_team(cls, team: int, port: int = 0):
        if hasattr(cls, "address"):
            raise ValueError("changing server address more than once is not supported")
        cls.address = f"10.{team//100}.{team%100}.2"
        cls.port = 0

    @classmethod
    def set_server(cls, address: str, port: int = 0):
        if hasattr(cls, "address"):
            raise ValueError("changing server address more than once is not supported")
        cls.address = address
        cls.port = port

    def __init__(self, inst: Optional[ntcore.NetworkTableInstance] = None, **kwargs):
        if not hasattr(type(self), "address") or not hasattr(type(self), "port"):
            raise ValueError("server address has not been set (use NTWidget.set_team() or NTWidget.set_address())")

        super().__init__(**kwargs)

        #  if self.name is None:
        #      raise ValueError("NetworkTables topic name not provided")

        if inst is None:
            inst = ntcore.NetworkTableInstance.getDefault()

        self.inst = inst

        if not self.inst.isConnected():
            self.inst.startClient4("Trellis")
            self.inst.setServer(type(self).address, type(self).port)
            Window.bind(on_request_close=lambda _evt: self.inst.stopClient())


        #  topic = self._get_topic()
        #  self.sub = topic.subscribe(self._default_value())
        #  self.pub = topic.publish()
        #  
        #  self.value_listener = self.inst.addListener(self.sub, ntcore.EventFlags.kValueAll, self._update)

        Window.bind(on_request_close=lambda _evt: self._shutdown())

    def on_name(self, _inst, value):
        if value is None:
            return
        if hasattr(self, "sub"):
            self._shutdown()
        topic = self._get_topic()
        self.sub = topic.subscribe(self._default_value())
        self.pub = topic.publish()

        self.value_listener = self.inst.addListener(self.sub, ntcore.EventFlags.kValueAll, self._update)

    def _get_topic(self) -> ntcore.Topic:
        raise NotImplementedError()

    def _default_value(self) -> Any:
        raise NotImplementedError()

    def _update(self, evt: ntcore.Event):
        raise NotImplementedError()

    def _shutdown(self):
        self.inst.removeListener(self.value_listener)
        self.sub.close()
        self.pub.close()

# Lovely idea, but doesn't seem to play nice with Kivy's autogeneration
#  def NTProperty(ntkind: str, default_value: Any, prop_type: type, prop_name: str = "ntvalue"):
#      def write_methods(cls: type):
#          setattr(cls, prop_name, prop_type(None, name=prop_name))
#  
#          get_topic_method = f"get{ntkind}Topic"
#          def _get_topic(self) -> ntcore.Topic:
#              if self.table is not None:
#                  table = self.inst.getTable(self.table)
#                  return getattr(table, get_topic_method)(self.name)
#              else:
#                  return getattr(self.inst, get_topic_method)(self.name)
#  
#          cls._get_topic = _get_topic
#  
#          cls._default_value = lambda self: default_value
#  
#          def _update(self, evt: ntcore.Event):
#              v = getattr(evt.data.value, f"get{ntkind}")()
#              setattr(self, prop_name, v)
#  
#          cls._update = _update
#  
#          def on_(self, _inst, value):
#              last = self.sub.get()
#              if value != last:
#                  self.pub.set(value)
#  
#          setattr(cls, f"on_{prop_name}", on_)
#  
#          return cls
#  
#      return write_methods
