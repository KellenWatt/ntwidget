from kivy.properties import ListProperty

import ntcore

from ..base import NTWidget

class NTDoubleArrayWidget(NTWidget):
    ntvalue = ListProperty(None)

    def _get_topic(self) -> ntcore.DoubleArrayTopic:
        if self.table is not None:
            table = self.inst.getTable(self.table)
            return table.getDoubleArrayTopic(self.name)
        else:
            return self.inst.getDoubleArrayTopic(self.name)

    def _default_value(self) -> list[float]:
        return []

    def _update(self, evt: ntcore.Event):
        v = evt.data.value.getDoubleArray()
        self.ntvalue = v

    def on_ntvalue(self, _inst, value):
        if any(type(v) != float or type(v) != int for v in value):
            raise ValueError("list values must be numeric")
        last = self.sub.get()
        if value != last:
            self.pub.set(value)

NTNumericArrayWidget = NTDoubleArrayWidget

class NTFloatArrayWidget(NTDoubleArrayWidget):
    def _get_topic(self) -> ntcore.FloatArrayTopic:
        if self.table is not None:
            table = self.inst.getTable(self.table)
            return table.getFloatArrayTopic(self.name)
        else:
            return self.inst.getFloatArrayTopic(self.name)

    def _update(self, evt: ntcore.Event):
        v = evt.data.value.getFloatArray()
        self.ntvalue = v

class NTIntegerArrayWidget(NTWidget):
    ntvalue = ListProperty(None)

    def _get_topic(self) -> ntcore.IntegerArrayTopic:
        if self.table is not None:
            table = self.inst.getTable(self.table)
            return table.getIntegerArrayTopic(self.name)
        else:
            return self.inst.getIntegerArrayTopic(self.name)

    def _default_value(self) -> list[int]:
        return []

    def _update(self, evt: ntcore.Event):
        v = evt.data.value.getIntegerArray()
        self.ntvalue = v

    def on_ntvalue(self, _inst, value):
        if any(type(v) != int for v in value):
            raise ValueError("list values must be numeric")
        last = self.sub.get()
        if value != last:
            self.pub.set(value)

