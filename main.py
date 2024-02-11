from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.storage.jsonstore import JsonStore

from kivy.core.window import Window # del
Window.size = (1080 / 3, 2202 / 3) # del

class MainLayout(FloatLayout):

    def to_operations_list(self):
        store = JsonStore('VEEP_save.json')
        try:
            operations = store.get('VEEP')["operations"]
            self.operations_list.clear_widgets()
            for i in range (len(operations)):
                layout = RelativeLayout(size_hint_y=None, size=(1, 225 / 3)) # pix
                layout.add_widget(Button())
                layout.add_widget(Label(text=str(operations[i]['type']), size_hint=(0.5, 1)))
                layout.add_widget(Label(text=str(operations[i]['value']), size_hint=(0.5, 1), pos_hint={'right': 1}))
                self.operations_list.add_widget(layout)
        except KeyError:
            pass
        finally:
            self.screen_manager.current = 'operations'

    def add_purpose(self):
        purpose = RelativeLayout(size_hint=(None, None), size=(480 / 3, self.purposes.size[1] - 60 / 3)) # pix
        purpose.canvas.add(Color(0.19, 0.19, 0.19))
        purpose.canvas.add(RoundedRectangle(size=purpose.size, radius=[30 / 3, 30 / 3, 30 / 3, 30 / 3])) # pix
        self.purposes.add_widget(purpose)

class Add_operation_Popup(Popup):

    cant = False
    def add_action(self, instance):
        marks = ['/', '*', '+', '-']
        if (instance.text == 'С'):
            self.operation_value.text = ''
        elif (instance.text == '<-'):
            self.operation_value.text = self.operation_value.text[0:len(self.operation_value.text) - 1:]
        elif (instance.text == '='):
            try:
                value = str(eval(self.operation_value.text))
                if (float(value) != 0):
                    self.operation_value.text = value
                else:
                    self.operation_value.text = str(0)
                if (float(value) % 1 == 0):
                    value = str(int(float(value)))
                self.operation_value.text = value
            except ZeroDivisionError:
                self.operation_value.text = 'Ошибка'
            self.cant = True
        elif (instance.text == '%'):
            try:
                buf = []
                for i in marks:
                    buf.append(self.operation_value.text.rfind(i))
                self.operation_value.text = self.operation_value.text[:len(self.operation_value.text) - (len(self.operation_value.text) - max(buf) - 1):] + str((int(1000000*(float(self.operation_value.text[max(buf) + 1::]) * 0.01)-0.5)+1)/1000000)
            except ValueError:
                pass
        else:
            if (instance.text in marks) and (self.cant == True):
                self.cant = False
                self.operation_value.text += instance.text
            elif (self.cant == True):
                self.operation_value.text = instance.text
                self.cant = False
            elif (self.cant == False):
                self.operation_value.text += instance.text
        if (instance.text in marks) and (self.operation_value.text[len(self.operation_value.text)-2] in marks):
            self.operation_value.text = self.operation_value.text[0:len(self.operation_value.text) - 2:] + instance.text

    operation_type = 'rem'

    def operation_type_to_add(self, instance):
        self.operation_type = 'add'
        instance.background_color = (0.15, 0.85, 0.15, 1)
        instance.color = (1, 1, 1, 1)
        self.type_to_rem_button.background_color = (0, 0, 0, 0)
        self.type_to_rem_button.color = (1, 0.2, 0.2, 1)

    def operation_type_to_rem(self, instance):
        self.operation_type = 'rem'
        instance.background_color = (1, 0.15, 0.15, 1)
        instance.color = (1, 1, 1, 1)
        self.type_to_add_button.background_color = (0, 0, 0, 0)
        self.type_to_add_button.color = (0.2, 1, 0.2, 1)

    def add_operation(self):
        store = JsonStore('VEEP_save.json')
        self.dismiss()
        operations = []
        try:
            operations = store.get('VEEP')["operations"]
        except KeyError:
            pass
        finally:
            value = str((int(100*(eval(self.operation_value.text))-0.5)+1) / 100)
            if (float(value) % 1 == 0):
                value = str(int(float(value)))
            operations.append({'type': self.operation_type, 'value': value})
            store.put('VEEP', operations=operations)

    def close(self):
        self.dismiss()

class VEEPApp(App):
    def build(self):
        return MainLayout()

if __name__ == '__main__':
    VEEPApp().run()