from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, RoundedRectangle, Ellipse, Rectangle, Line
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.storage.jsonstore import JsonStore

from kivy.core.window import Window # del
Window.size = (1080 / 3, 2202 / 3) # del

class MainLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.update()
        # CATEGORIES LIST
        store = JsonStore('VEEP_save.json')
        try:
            operations = store.get('VEEP')["operations"]
            value = 0
            for i in operations:
                if i['type'] == 'add':
                    value += float(i['value'])
                elif i['type'] == 'add':
                    value -= float(i['value'])
            if value % 1 == 0:
                value = int(value)

        except KeyError:
            pass
        self.add_operation_categories.clear_widgets()
        categories_names = ['Продукты', 'Транспорт', 'Культура', 'Обучение', 'Здоровье', 'Досуг', 'Другое']
        categories_images = ['basket.png', 'car.png', 'museum.png', 'brains.png', 'medicine.png', 'flying_snake.png', 'question.png']
        categories_colors = [[0.91, 0.45, 0.5], [0.26, 0.19, 0.54], [0.27, 0.58, 0.29], [1, 0.63, 0], [0.7, 0.16, 0.13], [0.47, 0.87, 0.91], [0, 0.19, 0.33]]
        for i in range (len(categories_names)):
            border = RelativeLayout(size_hint=(None, 1)) # pix
            border.size=(150 / 3, border.size[1]) # pix
            btn = Button(background_color=(0, 0, 0, 0), text=categories_names[i], font_size=0, size_hint=(1, 1), on_press=self.change_category)
            border.add_widget(btn)
            img = RelativeLayout(size=(120 / 3, 120 / 3), pos_hint={'center_x': 0.6, 'y': 0.25}) # pix
            img.canvas.add(Color(categories_colors[i][0], categories_colors[i][1], categories_colors[i][2]))
            img.canvas.add(Ellipse(size=img.size)) # pix
            img.canvas.add(Color(1.5, 1.5, 1.5))
            img.canvas.add(Rectangle(pos=(img.size[0] / 2 - 37.5 / 3, img.size[0] / 2 - 37.5 / 3), size=(75 / 3, 75 / 3), source='images/categories_icons/'+categories_images[i])) # pix
            border.add_widget(img)

            lb = Label(text=categories_names[i], size=(200, 0), pos_hint={'center_x': 0.5, 'y': -0.1}, text_size=(200, 159 / 3), font_size= 40 / 3, halign='center', valign='bottom', bold=True) # pix
            border.add_widget(lb)

            self.add_operation_categories.add_widget(border)
        self.add_operation_categories.add_widget(Widget())
        # ACCOUNTS LIST
        self.accounts_list.clear_widgets()
        accounts_list = [{'icon': 'case.png', 'color': [0.36, 0.5, 0.92], 'name': 'Основной', 'value': str(value)}]
        for i in accounts_list:
            border = RelativeLayout(size_hint=(None, None), size=(480 / 3, 300 / 3)) # pix
            border.canvas.add(Color(0.36, 0.5, 0.92))
            border.canvas.add(RoundedRectangle(radius=[30 / 3, 30 / 3, 30 / 3, 30 / 3], size=border.size)) # pix
            img = RelativeLayout(size=(120 / 3, 120 / 3), pos=(24 / 3, 150 / 3)) # pix
            img.canvas.add(Color(1, 1, 1))
            img.canvas.add(Ellipse(size=img.size))
            img.canvas.add(Color(i['color'][0], i['color'][1], i['color'][2]))
            img.canvas.add(Rectangle(size=(img.size[0]/1.5, img.size[1]/1.5), pos=(img.size[0]/6, img.size[0]/6), source='images/accounts_icons/'+i['icon']))
            border.add_widget(img)

            value_lb = Label(text=i['value'], bold=True, size_hint=(None, None), size=(288 / 3, 90 / 3), pos=(180 / 3, 180 / 3), font_size=50 / 3) # pix
            value_lb.text_size = value_lb.size
            value_lb.halign = 'center'
            value_lb.valign = 'bottom'
            value_lb.canvas.add(Color(0.19, 0.19, 0.19))
            value_lb.canvas.add(Line(width=4 / 3, points=[value_lb.pos[0], value_lb.y, value_lb.width * 1.625, value_lb.y])) # pix
            border.add_widget(value_lb)

            name_lb = RelativeLayout(size_hint=(None, None), size=(480 / 3, 75 / 3), pos=(0, 15 / 3)) # pix
            name_lb.canvas.add(Color(0.19, 0.19, 0.19))
            name_lb.canvas.add(Rectangle(size=name_lb.size, pos=name_lb.pos))
            lb = Label(text=i['name'], bold=True, pos=(0, 15 / 3), padding=[15 / 3, 0, 15 / 3, 6 / 3])
            name_lb.add_widget(lb)

            border.add_widget(name_lb)
            self.accounts_list.add_widget(border)

    def update(self):
        store = JsonStore('VEEP_save.json')
        try:
            operations = store.get('VEEP')["operations"]
            self.operations_list.clear_widgets()
            for i in range (len(operations)):
                layout = RelativeLayout(size_hint_y=None, size=(1, 225 / 3)) # pix
                layout.add_widget(Button())
                layout.add_widget(Label(text=str(operations[i]['type']), size_hint=(0.5, 0.5)))
                layout.add_widget(Label(text=str(operations[i]['value']), size_hint=(0.5, 0.5), pos_hint={'right': 1}))
                layout.add_widget(Label(text=str(operations[i]['category']), size_hint=(0.5, 0.5), pos_hint={'top': 1}))
                layout.add_widget(Label(text=str(operations[i]['description']), size_hint=(0.5, 0.5), pos_hint={'top': 1, 'right': 1}))
                self.operations_list.add_widget(layout)
            summ = 0
            for i in operations:
                if i['type'] == 'add':
                    summ += float(i['value'])
            if summ % 1 == 0:
                summ = int(summ)
            self.main_income_info.text = str(summ)
            summ = 0
            for i in operations:
                if i['type'] == 'rem':
                    summ += float(i['value'])
            if summ % 1 == 0:
                summ = int(summ)
            self.main_expenses_info.text = str(summ)
            summ = 0
            for i in operations:
                if i['type'] == 'add':
                    summ += float(i['value'])
                elif i['type'] == 'rem':
                    summ -= float(i['value'])
            if summ % 1 == 0:
                summ = int(summ)
            self.main_sum_info.text = str(summ)
        except KeyError:
            pass

    def add_purpose(self):
        purpose = RelativeLayout(size_hint=(None, None), size=(480 / 3, self.purposes.size[1] - 60 / 3)) # pix
        purpose.canvas.add(Color(0.19, 0.19, 0.19))
        purpose.canvas.add(RoundedRectangle(size=purpose.size, radius=[30 / 3, 30 / 3, 30 / 3, 30 / 3])) # pix
        self.purposes.add_widget(purpose)

    def add_account(self):
        account = RelativeLayout(size_hint=(None, None), size=(480 / 3, 300 / 3)) # pix
        account.canvas.add(Color(0.19, 0.19, 0.19))
        account.canvas.add(RoundedRectangle(radius=[30 / 3, 30 / 3, 30 / 3, 30 / 3], size=account.size)) # pix
        self.accounts_list.add_widget(account)
#--------------------------------------------------------
    cant = False
    def add_action(self, instance):
        marks = ['/', '*', '+', '-']
        if (instance.text == 'С'):
            self.operation_value.text = '0'
        elif (instance.text == '<-'):
            self.operation_value.text = self.operation_value.text[0:len(self.operation_value.text) - 1:]
            if (self.operation_value.text == ''):
                self.operation_value.text = '0'
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
            if (self.operation_value.text == '0' and instance.text not in marks):
                self.operation_value.text = ''
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

    def change_category(self, instance):
        self.operation_category = instance.text
        print (self.operation_category)

    operation_type = 'rem'
    operation_category = 'Другое'
    def operation_type_to_add(self, instance):
        self.operation_type = 'add'
        instance.background_color = (0.15, 0.85, 0.15, 1)
        instance.color = (1, 1, 1, 1)
        self.type_to_rem_button.background_color = (0, 0, 0, 0)
        self.type_to_rem_button.color = (1, 0.2, 0.2, 1)
        self.add_operation_categories.clear_widgets()
        categories_names = ['Зарплата', 'Пенсия', 'Подарок']
        categories_images = ['coins.png', 'letter.png', 'prize.png']
        categories_colors = [[1, 0.84, 0], [0.24, 0.37, 0.54], [0.84, 0.19, 0.2]]
        for i in range (len(categories_names)):
            border = RelativeLayout(size_hint=(None, 1)) # pix
            border.size=(150 / 3, border.size[1]) # pix
            btn = Button(background_color=(0, 0, 0, 0), text=categories_names[i], font_size=0, size_hint=(1, 1), on_press=self.change_category)
            border.add_widget(btn)
            img = RelativeLayout(size=(120 / 3, 120 / 3), pos_hint={'center_x': 0.6, 'y': 0.25}) # pix
            img.canvas.add(Color(categories_colors[i][0], categories_colors[i][1], categories_colors[i][2]))
            img.canvas.add(Ellipse(size=img.size)) # pix
            img.canvas.add(Color(1.5, 1.5, 1.5))
            img.canvas.add(Rectangle(pos=(img.size[0] / 2 - 37.5 / 3, img.size[0] / 2 - 37.5 / 3), size=(75 / 3, 75 / 3), source='images/categories_icons/'+categories_images[i])) # pix
            border.add_widget(img)

            lb = Label(text=categories_names[i], size=(200, 0), pos_hint={'center_x': 0.5, 'y': -0.1}, text_size=(200, 159 / 3), font_size= 40 / 3, halign='center', valign='bottom', bold=True) # pix
            border.add_widget(lb)

            self.add_operation_categories.add_widget(border)
        self.add_operation_categories.add_widget(Widget())

    def operation_type_to_rem(self, instance):
        self.operation_type = 'rem'
        instance.background_color = (1, 0.15, 0.15, 1)
        instance.color = (1, 1, 1, 1)
        self.type_to_add_button.background_color = (0, 0, 0, 0)
        self.type_to_add_button.color = (0.2, 1, 0.2, 1)
        self.add_operation_categories.clear_widgets()
        categories_names = ['Продукты', 'Транспорт', 'Культура', 'Обучение', 'Здоровье', 'Досуг', 'Другое']
        categories_images = ['basket.png', 'car.png', 'museum.png', 'brains.png', 'medicine.png', 'flying_snake.png', 'question.png']
        categories_colors = [[0.91, 0.45, 0.5], [0.26, 0.19, 0.54], [0.27, 0.58, 0.29], [1, 0.63, 0], [0.7, 0.16, 0.13], [0.47, 0.87, 0.91], [0, 0.19, 0.33]]
        for i in range (len(categories_names)):
            border = RelativeLayout(size_hint=(None, 1)) # pix
            border.size=(150 / 3, border.size[1]) # pix
            btn = Button(background_color=(0, 0, 0, 0), text=categories_names[i], font_size=0, size_hint=(1, 1), on_press=self.change_category)
            border.add_widget(btn)
            img = RelativeLayout(size=(120 / 3, 120 / 3), pos_hint={'center_x': 0.6, 'y': 0.25}) # pix
            img.canvas.add(Color(categories_colors[i][0], categories_colors[i][1], categories_colors[i][2]))
            img.canvas.add(Ellipse(size=img.size)) # pix
            img.canvas.add(Color(1.5, 1.5, 1.5))
            img.canvas.add(Rectangle(pos=(img.size[0] / 2 - 37.5 / 3, img.size[0] / 2 - 37.5 / 3), size=(75 / 3, 75 / 3), source='images/categories_icons/'+categories_images[i])) # pix
            border.add_widget(img)

            lb = Label(text=categories_names[i], size=(200, 0), pos_hint={'center_x': 0.5, 'y': -0.1}, text_size=(200, 159 / 3), font_size= 40 / 3, halign='center', valign='bottom', bold=True) # pix
            border.add_widget(lb)

            self.add_operation_categories.add_widget(border)
        self.add_operation_categories.add_widget(Widget())

    def add_operation(self):
        store = JsonStore('VEEP_save.json')
        operations = []
        try:
            operations = store.get('VEEP')["operations"]
        except KeyError:
            pass
        except SyntaxError:
            pass
        value = str((int(100 * (eval(self.operation_value.text)) - 0.5) + 1) / 100)
        if (float(value) % 1 == 0):
            value = str(int(float(value)))
        operations.append({'type': self.operation_type, 'value': value, 'category': self.operation_category, 'description': self.add_operation_description.text})
        store.put('VEEP', operations=operations)
        print(store.get('VEEP')['operations'])
        self.operation_value.text = '0'
        self.add_operation_description.text = ''
        self.operation_category = 'Другое'
        self.screen_manager.current = 'operations'
        self.update()

class VEEPApp(App):
    def build(self):
        return MainLayout()

if __name__ == '__main__':
    VEEPApp().run()