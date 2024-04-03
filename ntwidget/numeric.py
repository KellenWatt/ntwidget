from kivy.properties import NumericProperty
from kivy.core.window import Window

import ntcore

from typing import Optional, Any

from .base import NTWidget

class NTDoubleWidget(NTWidget):
    ntvalue = NumericProperty(None)
    
    def _get_topic(self) -> ntcore.DoubleTopic:
        if self.table is not None:
            table = self.inst.getTable(self.table)
            return table.getDoubleTopic(self.name)
        else:
            return self.inst.getDoubleTopic(self.name)
    
    def _default_value(self) -> float:
        return 0.0
    
    def _update(self, evt: ntcore.Event):
        v = evt.data.value.getDouble()
        self.ntvalue = v
    
    def on_ntvalue(self, _inst, value):
        last = self.sub.get()
        if value != last:
            self.pub.set(value)

        
NTNumericWidget = NTDoubleWidget

class NTFloatWidget(NTWidget):
    ntvalue = NumericProperty(None)
    
    def _get_topic(self) -> ntcore.FloatTopic:
        if self.table is not None:
            table = self.inst.getTable(self.table)
            return table.getFloatTopic(self.name)
        else:
            return self.inst.getFloatTopic(self.name)
    
    def _default_value(self) -> float:
        return 0.0
    
    def _update(self, evt: ntcore.Event):
        v = evt.data.value.getFloat()
        self.ntvalue = v
    
    def on_ntvalue(self, _inst, value):
        last = self.sub.get()
        if value != last:
            self.pub.set(value)

class NTIntegerWidget(NTWidget):
    ntvalue = NumericProperty(None)
    
    def _get_topic(self) -> ntcore.IntegerTopic:
        if self.table is not None:
            table = self.inst.getTable(self.table)
            return table.getIntegerTopic(self.name)
        else:
            return self.inst.getIntegerTopic(self.name)
    
    def _default_value(self) -> int:
        return 0
    
    def _update(self, evt: ntcore.Event):
        v = evt.data.value.getInteger()
        self.ntvalue = v
    
    def on_ntvalue(self, _inst, value):
        last = self.sub.get()
        if value != last:
            self.pub.set(value)



DEFAULT_NT_INSTANCE = ntcore.NetworkTableInstance.getDefault()
def bind_double(prop_name: str, 
                name: str, 
                table: str = "", 
                default_value: float = 0.0, 
                inst: Optional[ntcore.NetworkTableInstance] = None):
    if inst is None:
        inst = ntcore.NetworkTableInstance.getDefault()
    def bind(cls: type) -> type:
        nonlocal table
        init = cls.__init__
        sub_name = f"__{table.replace('/', '_')}__{name}_subscriber"
        pub_name = f"__{table.replace('/', '_')}__{name}_publisher"
        listener_name = f"__{table.replace('/', '_')}__{name}_listener"

        def new_init(self, **kwargs):
            nonlocal table
            init(self, **kwargs)
            if len(table) == 0:
                table = inst.getTable(table)
            else:
                table = inst
            topic = table.getDoubleTopic(name)
            setattr(self, sub_name, topic.subscribe(default_value))
            setattr(self, pub_name, topic.publish())
            
            def send(_inst, value):
                last = getattr(self, sub_name).get()
                if value != last:
                    getattr(self, pub_name).set(value)

            self.bind(**{prop_name: send})
       
            def update(evt: ntcore.Event):
                prop_setter = self.setter(prop_name)
                prop_setter(self, evt.data.value.getDouble())
                #  prop.fset(self, evt.data.value.getDouble())

            listener = inst.addListener(getattr(self, sub_name), ntcore.EventFlags.kValueAll, update)
            setattr(self, listener_name, listener)

            def shutdown():
                inst.removeListener(self.value_listener)
                getattr(self, sub_name).close()
                getattr(self, pub_name).close()

            Window.bind(on_request_close=lambda _evt: shutdown())

        cls.__init__ = new_init
        return cls
    return bind
