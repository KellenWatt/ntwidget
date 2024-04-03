from kivy.properties import StringProperty

import ntcore

from typing import Optional, Any

from .base import NTWidget

        
class NTStringWidget(NTWidget):
    ntvalue = StringProperty(None)
    
    def _get_topic(self) -> ntcore.StringTopic:
        if self.table is not None:
            table = self.inst.getTable(self.table)
            return table.getStringTopic(self.name)
        else:
            return self.inst.getStringTopic(self.name)
    
    def _default_value(self) -> str:
        return ""
    
    def _update(self, evt: ntcore.Event):
        v = evt.data.value.getString()
        self.ntvalue = v
    
    def on_ntvalue(self, _inst, value):
        last = self.sub.get()
        if value != last:
            self.pub.set(value)
