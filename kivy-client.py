import ntcore
from ntwidget.numeric import NTDoubleWidget
from ntwidget.numeric import bind_double


from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout

NTDoubleWidget.set_server("localhost")

#  @bind_double("value", "num")
class NTSlider(NTDoubleWidget, Slider):
    #  pass
    def __init__(self, **kwargs):
        NTDoubleWidget.__init__(self, **kwargs)
        Slider.__init__(self)
    
        self.bind(value=self.setter("ntvalue"))
        self.bind(ntvalue=self.setter("value"))


class Thing(BoxLayout):
    pass;

class ClientApp(App):
    def build(self):
        return Thing()
        #  w = NTSlider(min=-1, max=1)
        #  w.bind(ntvalue=lambda _, val: print(val))

        return l

if __name__ == "__main__":
    ClientApp().run()

