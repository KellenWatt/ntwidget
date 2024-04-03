from kivy.properties import ObjectProperty

import ntcore

from typing import Optional, Any

from .base import NTWidget

class NTRawWidget(NTWidget):
    ntvalue = ObjectProperty(None)
    
    def _get_topic(self) -> ntcore.RawTopic:
        if self.table is not None:
            table = self.inst.getTable(self.table)
            return table.getRawTopic(self.name)
        else:
            return self.inst.getRawTopic(self.name)
    
    def _default_value(self) -> bytes:
        return bytes(0)
    
    def _update(self, evt: ntcore.Event):
        v = evt.data.value.getRaw()
        self.ntvalue = v
    
    def on_ntvalue(self, _inst, value):
        if not isinstance(value, (bytes, bytearray, memoryview)):
            try:
                value = bytes(value)
            except:
                raise ValueError("values must conform to the buffer protocol")
        last = bytes(self.sub.get())
        if value != last:
            self.pub.set(value)
