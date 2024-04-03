from kivy.properties import BooleanProperty

import ntcore

from typing import Optional, Any

from .base import NTWidget

class NTBooleanWidget(NTWidget):
    ntvalue = BooleanProperty(None)
    
    def _get_topic(self) -> ntcore.BooleanTopic:
        if self.table is not None:
            table = self.inst.getTable(self.table)
            return table.getBooleanTopic(self.name)
        else:
            return self.inst.getBooleanTopic(self.name)
    
    def _default_value(self) -> bool:
        return False
    
    def _update(self, evt: ntcore.Event):
        v = evt.data.value.getBoolean()
        self.ntvalue = v
    
    def on_ntvalue(self, _inst, value):
        last = self.sub.get()
        if value != last:
            self.pub.set(value)

        
