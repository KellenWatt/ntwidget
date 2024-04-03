from kivy.properties import ListProperty

import ntcore

from ..base import NTWidget

class NTBooleanArrayWidget(NTWidget):
    ntvalue = ListProperty(None)

    def _get_topic(self) -> ntcore.BooleanArrayTopic:
        if self.table is not None:
            table = self.inst.getTable(self.table)
            return table.getBooleanArrayTopic(self.name)
        else:
            return self.inst.getBooleanArrayTopic(self.name)

    def _default_value(self) -> list[bool]:
        return []

    def _update(self, evt: ntcore.Event):
        v = evt.data.value.getBooleanArray()
        self.ntvalue = v

    def on_ntvalue(self, _inst, value):
        if any(type(v) != bool for v in value):
            raise ValueError("list values must be boolean")
        last = self.sub.get()
        if value != last:
            self.pub.set(value)
