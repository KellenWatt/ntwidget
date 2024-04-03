from kivy.properties import ListProperty

import ntcore

from ..base import NTWidget

class NTStringArrayWidget(NTWidget):
    ntvalue = ListProperty(None)

    def _get_topic(self) -> ntcore.StringArrayTopic:
        if self.table is not None:
            table = self.inst.getTable(self.table)
            return table.getStringArrayTopic(self.name)
        else:
            return self.inst.getStringArrayTopic(self.name)

    def _default_value(self) -> list[str]:
        return []

    def _update(self, evt: ntcore.Event):
        v = evt.data.value.getStringArray()
        self.ntvalue = v

    def on_ntvalue(self, _inst, value):
        if any(type(v) != str for v in value):
            raise ValueError("list values must be strings")
        last = self.sub.get()
        if value != last:
            self.pub.set(value)
