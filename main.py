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
        # CATEGORIES LIST
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

            lb = Label(text=categories_names[i], size=(300 / 3, 0), pos_hint={'center_x': 0.5, 'y': -0.1}, text_size=(300 / 3, 159 / 3), font_size= 40 / 3, halign='center', valign='bottom', bold=True) # pix
            border.add_widget(lb)

            self.add_operation_categories.add_widget(border)
        self.add_operation_categories.add_widget(Widget())
        # ACCOUNTS LIST
        store = JsonStore('VEEP_save.json')

        try:
            store.get('VEEP')["accounts"]
        except KeyError:
            try:
                operations = store.get('VEEP')["operations"]
            except KeyError:
                operations = []
            store.put('VEEP', accounts=[{'id': '0', 'icon': 'case.png', 'color': '0.44, 0.54, 0.92', 'name': 'Основной', 'value': '0'}], operations=operations)

        value = 0
        try:
            operations = store.get('VEEP')["operations"]
        except KeyError:
            pass
        accounts_list = []
        try:
            accounts = store.get('VEEP')["accounts"]
            for i in accounts:
                accounts_list.append(i)
        except KeyError:
            pass
        self.accounts_list.clear_widgets()
        for i in accounts_list:
            color = i['color'].split(', ')
            border = RelativeLayout(size_hint=(None, None), size=(480 / 3, 300 / 3)) # pix
            border.canvas.add(Color(color[0], color[1], color[2]))
            border.canvas.add(RoundedRectangle(radius=[30 / 3, 30 / 3, 30 / 3, 30 / 3], size=border.size)) # pix
            img = RelativeLayout(size=(120 / 3, 120 / 3), pos=(24 / 3, 150 / 3)) # pix
            img.canvas.add(Color(1, 1, 1))
            img.canvas.add(Ellipse(size=img.size))
            img.canvas.add(Color(color[0], color[1], color[2]))
            img.canvas.add(Rectangle(size=(img.size[0]/1.5, img.size[1]/1.5), pos=(img.size[0]/6, img.size[0]/6), source='images/accounts_icons/'+i['icon']))
            border.add_widget(img)

            value_lb = Label(text=str(value), bold=True, size_hint=(None, None), size=(288 / 3, 90 / 3), pos=(180 / 3, 180 / 3), font_size=50 / 3) # pix
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

        border = RelativeLayout(size_hint=(None, None), size=(480 / 3, 300 / 3))  # pix
        border.canvas.add(Color(0.19, 0.19, 0.19))
        border.canvas.add(RoundedRectangle(radius=[30 / 3, 30 / 3, 30 / 3, 30 / 3], size=border.size)) # pix
        border.canvas.add(Color(1, 1, 1))
        border.canvas.add(Rectangle(size=(100 / 3, 100 / 3), pos=(190 / 3, 100 / 3), source='images/buttons_icons/plus_small.png')) # pix
        btn = Button(on_press=self.change_screen_to_add_account, background_color=(0, 0, 0, 0))
        border.add_widget(btn)
        self.accounts_list.add_widget(border)

        self.update()

    account_id = '0'

    def change_account_in_operation_add(self, instance):
        self.account_id = instance.text

    def change_screen_to_add_account(self, instance):
        self.screen_manager.current = 'add_account'

    def update(self):
        store = JsonStore('VEEP_save.json')
        try:
            operations = store.get('VEEP')["operations"]
            # self.operations_list.clear_widgets()
            for i in range (len(operations)):
                type = operations[i]['type']
                if type == 'rem':
                    border_color = [1, 0.15, 0.15]
                    categories_names = ['Продукты', 'Транспорт', 'Культура', 'Обучение', 'Здоровье', 'Досуг', 'Другое']
                    categories_images = ['basket.png', 'car.png', 'museum.png', 'brains.png', 'medicine.png', 'flying_snake.png', 'question.png']
                    categories_colors = [[0.91, 0.45, 0.5], [0.26, 0.19, 0.54], [0.27, 0.58, 0.29], [1, 0.63, 0], [0.7, 0.16, 0.13], [0.47, 0.87, 0.91], [0, 0.19, 0.33]]
                elif type == 'add':
                    border_color = [0.15, 0.85, 0.15]
                    categories_names = ['Зарплата', 'Пенсия', 'Подарок']
                    categories_images = ['coins.png', 'letter.png', 'prize.png']
                    categories_colors = [[1, 0.84, 0], [0.24, 0.37, 0.54], [0.84, 0.19, 0.2]]
                value = operations[i]['value']
                category = operations[i]['category']
                description = operations[i]['description']
                for j in range (len(categories_names)):
                    if categories_names[j] == category:
                        name = categories_names[j]
                        color = categories_colors[j]
                        icon = categories_images[j]
                        break

                border = RelativeLayout(size_hint=(None, None), size=(990 / 3, 225 / 3)) # pix
                border.canvas.add(Color(border_color[0], border_color[1], border_color[2]))
                border.canvas.add(Line(width=6 / 3, points=[border.width * 0.3, 0, border.width * 0.7, 0])) # pix
                border.canvas.add(Line(width=6 / 3, points=[border.width * 0.3, border.height, border.width * 0.7, border.height])) # pix
                border.canvas.add(Line(width=6 / 3, points=[0, border.height * 0.3, 0, border.height * 0.7])) # pix
                border.canvas.add(Line(width=6 / 3, points=[border.width, border.height * 0.3, border.width, border.height * 0.7])) # pix
                border.canvas.add(Color(0.19, 0.19, 0.19))
                border.canvas.add(RoundedRectangle(radius=[30 / 3, 30 / 3, 30 / 3, 30 / 3], size=border.size))

                img = RelativeLayout(size_hint=(None, None), size=(123.75 / 3, 123.75 / 3), pos=(64.35 / 3, 73.125 / 3)) # pix
                img.canvas.add(Color(color[0], color[1], color[2]))
                img.canvas.add(Ellipse(size=img.size))
                img.canvas.add(Color(2, 2, 2))
                img.canvas.add(Rectangle(size=(img.size[0] / 1.5, img.size[0] / 1.5), pos=(img.size[0] / 6, img.size[0] / 6), source='images/categories_icons/'+icon))
                border.add_widget(img)

                name_lb = Label(text=name, size=(300 / 3, 0), pos_hint={'center_x': 0.1275, 'y': -0.05}, text_size=(300 / 3, 159 / 3), font_size=40 / 3, halign='center', valign='bottom', bold=True) # pix
                border.add_widget(name_lb)

                value_lb = Label(text=value, size_hint=(None, None), size=(742.5 / 3, 112.5 / 3), pos=(247.5 / 3, 112.5 / 3), bold=True, valign='bottom', halign='center', font_size=60 / 3) # pix
                value_lb.canvas.add(Color(0.12, 0.12, 0.12))
                value_lb.canvas.add(Line(width=4 / 3, points=[value_lb.pos[0], value_lb.pos[1] + 21 / 3, value_lb.size[0] * 1.3, value_lb.pos[1] + 21 / 3])) # pix
                border.add_widget(value_lb)

                description_lb = Label(text=description, size_hint=(None, None), size=(742.5 / 3, 112.5 / 3), pos=(247.5 / 3, 0), font_size=45 / 3, valign='middle', halign='center', color=(0.75, 0.75, 0.75)) # pix
                description_lb.canvas.add(Color(0.12, 0.12, 0.12))
                description_lb.canvas.add(Line(width=4 / 3, points=[description_lb.pos[0], description_lb.pos[1] + 21 / 3, description_lb.size[0] * 1.3, description_lb.pos[1] + 21 / 3])) # pix
                border.add_widget(description_lb)

                self.operations_list.add_widget(border)

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
#-----------
        accounts_list = []
        try:
            accounts = store.get('VEEP')["accounts"]
            for i in accounts:
                accounts_list.append(i)
        except KeyError:
            pass
        self.add_operation_accounts.clear_widgets()
        for i in range (len(accounts_list)):
            color = accounts_list[i]['color'].split(', ')
            border = RelativeLayout(size_hint=(None, None), size=(283.5 / 3, 189 / 3)) # pix
            border.canvas.add(Color(color[0], color[1], color[2]))
            border.canvas.add(RoundedRectangle(radius=[30 / 3, 30 / 3, 30 / 3, 30 / 3], size=border.size)) # pix

            img = RelativeLayout(size_hint=(None, None), size=(94.5 / 3, 94.5 / 3), pos=(15 / 3, 78 / 3)) # pix
            img.canvas.add(Color(1, 1, 1))
            img.canvas.add(Ellipse(size=img.size))
            img.canvas.add(Color(color[0], color[1], color[2]))
            img.canvas.add(Rectangle(size=(img.size[0]/1.5, img.size[1]/1.5), pos=(img.size[0]/6, img.size[0]/6), source='images/accounts_icons/'+accounts_list[i]['icon']))
            border.add_widget(img)

            lb = Label(text=accounts_list[i]['value'], size_hint=(None, None), size=(283.5 / 3, 60 / 3), pos=(0, 9 / 3), padding=[15 / 3, 0, 15 / 3, 0], halign='right', valign='middle', text_size=(283.5 / 3, 60 / 3), bold=True) # pix
            border.add_widget(lb)

            btn = Button(on_press=self.change_account_in_operation_add, text=accounts_list[i]['id'], font_size=0, background_color=(0, 0, 0, 0))
            border.add_widget(btn)

            self.add_operation_accounts.add_widget(border)
        self.accounts_list.clear_widgets()
        for i in accounts_list:
            color = i['color'].split(', ')
            border = RelativeLayout(size_hint=(None, None), size=(480 / 3, 300 / 3)) # pix
            border.canvas.add(Color(color[0], color[1], color[2]))
            border.canvas.add(RoundedRectangle(radius=[30 / 3, 30 / 3, 30 / 3, 30 / 3], size=border.size)) # pix
            img = RelativeLayout(size=(120 / 3, 120 / 3), pos=(24 / 3, 150 / 3)) # pix
            img.canvas.add(Color(1, 1, 1))
            img.canvas.add(Ellipse(size=img.size))
            img.canvas.add(Color(color[0], color[1], color[2]))
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

        border = RelativeLayout(size_hint=(None, None), size=(480 / 3, 300 / 3))  # pix
        border.canvas.add(Color(0.19, 0.19, 0.19))
        border.canvas.add(RoundedRectangle(radius=[30 / 3, 30 / 3, 30 / 3, 30 / 3], size=border.size)) # pix
        border.canvas.add(Color(1, 1, 1))
        border.canvas.add(Rectangle(size=(100 / 3, 100 / 3), pos=(190 / 3, 100 / 3), source='images/buttons_icons/plus_small.png')) # pix
        btn = Button(on_press=self.change_screen_to_add_account, background_color=(0, 0, 0, 0))
        border.add_widget(btn)
        self.accounts_list.add_widget(border)

    add_account_icon = 'case.png'
    add_account_color = '0.44, 0.54, 0.92'
    example_add_account_name = ''
    def add_account(self):
        name = self.add_account_name.text
        color = self.add_account_color
        icon = self.add_account_icon
        store = JsonStore('VEEP_save.json')
        accounts = []
        operations = []
        try:
            accounts = store.get('VEEP')["accounts"]
        except KeyError:
            pass
        try:
            operations = store.get('VEEP')["operations"]
        except KeyError:
            pass
        accounts.append({'id': str(len(accounts)), 'icon': icon, 'color': color, 'name': name, 'value': '0'})
        store.put('VEEP', accounts=accounts, operations=operations)
        self.add_account_name.text = ''
        self.add_account_icon = 'case.png'
        self.add_account_color = '0.44, 0.54, 0.92'
        self.screen_manager.current = 'accounts'
        self.update()

    def add_purpose(self):
        purpose = RelativeLayout(size_hint=(None, None), size=(480 / 3, self.purposes.size[1] - 60 / 3)) # pix
        purpose.canvas.add(Color(0.19, 0.19, 0.19))
        purpose.canvas.add(RoundedRectangle(size=purpose.size, radius=[30 / 3, 30 / 3, 30 / 3, 30 / 3])) # pix
        self.purposes.add_widget(purpose)

#--------------------------------------------------------
    cant = False
    def add_action(self, instance):
        marks = ['/', '*', '+', '-', '.']
        if (instance.text == 'С'):
            self.operation_value.text = '0'
        elif (instance.text == '<-'):
            self.operation_value.text = self.operation_value.text[0:len(self.operation_value.text) - 1:]
            if (self.operation_value.text == ''):
                self.operation_value.text = '0'
        elif (instance.text == '.'):
            text = self.operation_value.text
            if (self.operation_value.text[len(self.operation_value.text) - 1] not in marks):
                text = text.replace('/', '_')
                text = text.replace('*', '_')
                text = text.replace('+', '_')
                text = text.replace('-', '_')
                text = text.split('_')
                text = text[len(text) - 1]
                if text.find('.') < 0:
                    if (self.operation_value.text == '0' and instance.text not in marks and instance.text != '.'):
                        self.operation_value.text = ''
                    self.operation_value.text += '.'
        elif (instance.text == '='):
            try:
                value = eval(self.operation_value.text)
                if (float(value) % 1 == 0):
                    value = str(int(float(value)))
                else:
                    value = str((int(100 * value - 0.5) + 1) / 100)
                if (float(value) != 0):
                    self.operation_value.text = value
                else:
                    self.operation_value.text = str(0)
                if (float(value) % 1 == 0):
                    value = str(int(float(value)))
                self.operation_value.text = value
                self.cant = True
            except ZeroDivisionError:
                self.operation_value.text = 'Ошибка'
                self.cant = True
            except SyntaxError:
                pass
        elif (instance.text == '%'):
            try:
                text = self.operation_value.text
                text = text.replace('/', '_')
                text = text.replace('*', '_')
                text = text.replace('+', '_')
                text = text.replace('-', '_')
                text = text.split('_')
                new_text = str((int(10000 * (float(text[len(text) - 1]) * 0.01) - 0.5) + 1) / 10000)
                text = text[len(text) - 1]
                print (text)
                print (new_text)
                print (self.operation_value.text[:len(self.operation_value.text) - len(text)])
                self.operation_value.text = self.operation_value.text[:len(self.operation_value.text) - len(text)] + new_text
            except ValueError:
                pass
        else:
            if (self.operation_value.text == '0' and instance.text not in marks and instance.text != '.'):
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

    operation_type = 'rem'
    operation_category = 'Другое'
    def operation_type_to_add(self, instance):
        self.operation_type = 'add'
        self.operation_category = 'Зарплата'
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
        self.operation_category = 'Другое'
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
        accounts = []
        try:
            operations = store.get('VEEP')["operations"]
        except KeyError:
            pass
        except SyntaxError:
            pass
        try:
            if eval(self.operation_value.text) != 0:
                value = str((int(100 * (eval(self.operation_value.text)) - 0.5) + 1) / 100)
                if (float(value) % 1 == 0):
                    value = str(int(float(value)))
                operations.append({'type': self.operation_type, 'value': value, 'category': self.operation_category, 'description': self.add_operation_description.text})
                try:
                    accounts = store.get('VEEP')["accounts"]
                except KeyError:
                    pass
                for i in range (len(accounts)):
                    if accounts[i]['id'] == self.account_id:
                        acc = accounts[i]
                if self.operation_type == 'add':
                    acc['value'] = str(float(acc['value']) + float(value))
                elif self.operation_type == 'rem':
                    acc['value'] = str(float(acc['value']) - float(value))
                if (float(acc['value']) % 1 == 0):
                    acc['value'] = str(int(float(acc['value'])))
                accounts.remove(acc)
                accounts.insert(0, acc)
                store.put('VEEP', accounts=accounts, operations=operations)
                self.operation_value.text = '0'
                self.add_operation_description.text = ''
                self.operation_category = 'Другое'
                self.screen_manager.current = 'operations'
                self.update()
            else:
                self.operation_value.text = 'Укажите число больше "0"'
                self.cant = True
        except SyntaxError:
            pass

    def change_account_icon_in_account_add(self, icon):
        self.add_account_icon = icon
        color = self.add_account_color.split(', ')

        self.add_account_example_border_border.clear_widgets()
        border = RelativeLayout(size_hint=(None, None), size=(480 / 3, 300 / 3)) # pix
        border.canvas.add(Color(color[0], color[1], color[2]))
        border.canvas.add(RoundedRectangle(radius=[30 / 3, 30 / 3, 30 / 3, 30 / 3], size=border.size))  # pix
        img = RelativeLayout(size=(120 / 3, 120 / 3), pos=(24 / 3, 150 / 3))  # pix
        img.canvas.add(Color(1, 1, 1))
        img.canvas.add(Ellipse(size=img.size))
        img.canvas.add(Color(color[0], color[1], color[2]))
        img.canvas.add(Rectangle(size=(img.size[0] / 1.5, img.size[1] / 1.5), pos=(img.size[0] / 6, img.size[0] / 6), source='images/accounts_icons/' + icon))
        border.add_widget(img)

        value_lb = Label(text='0', bold=True, size_hint=(None, None), size=(288 / 3, 90 / 3), pos=(180 / 3, 180 / 3), font_size=50 / 3)  # pix
        value_lb.text_size = value_lb.size
        value_lb.halign = 'center'
        value_lb.valign = 'bottom'
        value_lb.canvas.add(Color(0.19, 0.19, 0.19))
        value_lb.canvas.add(Line(width=4 / 3, points=[value_lb.pos[0], value_lb.y, value_lb.width * 1.6, value_lb.y])) # pix
        border.add_widget(value_lb)

        name_lb = RelativeLayout(size_hint=(None, None), size=(480 / 3, 75 / 3), pos=(0, 15 / 3))  # pix
        name_lb.canvas.add(Color(0.19, 0.19, 0.19))
        name_lb.canvas.add(Rectangle(size=name_lb.size, pos=name_lb.pos))
        lb = Label(text=self.example_add_account_name, bold=True, pos=(0, 15 / 3), padding=[15 / 3, 0, 15 / 3, 6 / 3]) # pix
        name_lb.add_widget(lb)

        border.add_widget(name_lb)
        self.add_account_example_border_border.add_widget(border)

    def change_account_color_in_account_add(self, color):
        self.add_account_color = color
        icon = self.add_account_icon
        color = color.split(', ')

        self.add_account_example_border_border.clear_widgets()
        border = RelativeLayout(size_hint=(None, None), size=(480 / 3, 300 / 3)) # pix
        border.canvas.add(Color(color[0], color[1], color[2]))
        border.canvas.add(RoundedRectangle(radius=[30 / 3, 30 / 3, 30 / 3, 30 / 3], size=border.size)) # pix
        img = RelativeLayout(size=(120 / 3, 120 / 3), pos=(24 / 3, 150 / 3)) # pix
        img.canvas.add(Color(1, 1, 1))
        img.canvas.add(Ellipse(size=img.size))
        img.canvas.add(Color(color[0], color[1], color[2]))
        img.canvas.add(Rectangle(size=(img.size[0] / 1.5, img.size[1] / 1.5), pos=(img.size[0] / 6, img.size[0] / 6), source='images/accounts_icons/' + icon))
        border.add_widget(img)

        value_lb = Label(text='0', bold=True, size_hint=(None, None), size=(288 / 3, 90 / 3), pos=(180 / 3, 180 / 3), font_size=50 / 3) # pix
        value_lb.text_size = value_lb.size
        value_lb.halign = 'center'
        value_lb.valign = 'bottom'
        value_lb.canvas.add(Color(0.19, 0.19, 0.19))
        value_lb.canvas.add(Line(width=4 / 3, points=[value_lb.pos[0], value_lb.y, value_lb.width * 1.6, value_lb.y])) # pix
        border.add_widget(value_lb)

        name_lb = RelativeLayout(size_hint=(None, None), size=(480 / 3, 75 / 3), pos=(0, 15 / 3)) # pix
        name_lb.canvas.add(Color(0.19, 0.19, 0.19))
        name_lb.canvas.add(Rectangle(size=name_lb.size, pos=name_lb.pos))
        lb = Label(text=self.example_add_account_name, bold=True, pos=(0, 15 / 3), padding=[15 / 3, 0, 15 / 3, 6 / 3]) # pix
        name_lb.add_widget(lb)

        border.add_widget(name_lb)
        self.add_account_example_border_border.add_widget(border)

    def change_account_name_in_account_add(self):
        self.example_add_account_name = self.add_account_name.text
        color = self.add_account_color
        icon = self.add_account_icon

        self.add_account_color = color
        icon = self.add_account_icon
        color = color.split(', ')

        self.add_account_example_border_border.clear_widgets()
        border = RelativeLayout(size_hint=(None, None), size=(480 / 3, 300 / 3)) # pix
        border.canvas.add(Color(color[0], color[1], color[2]))
        border.canvas.add(RoundedRectangle(radius=[30 / 3, 30 / 3, 30 / 3, 30 / 3], size=border.size)) # pix
        img = RelativeLayout(size=(120 / 3, 120 / 3), pos=(24 / 3, 150 / 3))  # pix
        img.canvas.add(Color(1, 1, 1))
        img.canvas.add(Ellipse(size=img.size))
        img.canvas.add(Color(color[0], color[1], color[2]))
        img.canvas.add(Rectangle(size=(img.size[0] / 1.5, img.size[1] / 1.5), pos=(img.size[0] / 6, img.size[0] / 6), source='images/accounts_icons/' + icon))
        border.add_widget(img)

        value_lb = Label(text='0', bold=True, size_hint=(None, None), size=(288 / 3, 90 / 3), pos=(180 / 3, 180 / 3), font_size=50 / 3) # pix
        value_lb.text_size = value_lb.size
        value_lb.halign = 'center'
        value_lb.valign = 'bottom'
        value_lb.canvas.add(Color(0.19, 0.19, 0.19))
        value_lb.canvas.add(Line(width=4 / 3, points=[value_lb.pos[0], value_lb.y, value_lb.width * 1.6, value_lb.y])) # pix
        border.add_widget(value_lb)

        name_lb = RelativeLayout(size_hint=(None, None), size=(480 / 3, 75 / 3), pos=(0, 15 / 3)) # pix
        name_lb.canvas.add(Color(0.19, 0.19, 0.19))
        name_lb.canvas.add(Rectangle(size=name_lb.size, pos=name_lb.pos))
        lb = Label(text=self.example_add_account_name, bold=True, pos=(0, 15 / 3), padding=[15 / 3, 0, 15 / 3, 6 / 3]) # pix
        name_lb.add_widget(lb)

        border.add_widget(name_lb)
        self.add_account_example_border_border.add_widget(border)

class VEEPApp(App):
    def build(self):
        return MainLayout()

if __name__ == '__main__':
    VEEPApp().run()