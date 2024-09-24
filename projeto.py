import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

# Banco de dados
class RentalDB:
    def __init__(self):
        self.conn = sqlite3.connect("rentals.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS rentals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                rent_date TEXT NOT NULL,
                return_date TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add_rental(self, name, rent_date, return_date):
        self.cursor.execute("INSERT INTO rentals (name, rent_date, return_date) VALUES (?, ?, ?)", (name, rent_date, return_date))
        self.conn.commit()

    def get_all_rentals(self):
        self.cursor.execute("SELECT * FROM rentals")
        return self.cursor.fetchall()

    def delete_rental(self, rental_id):
        self.cursor.execute("DELETE FROM rentals WHERE id = ?", (rental_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

# Interface do Usuário
class RentalApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = RentalDB()
        self.orientation = 'vertical'

        # Entrada de Nome
        self.name_input = TextInput(hint_text='Nome do Cliente', size_hint=(1, 0.1))
        self.add_widget(self.name_input)

        # Entrada de Data de Aluguel
        self.rent_date_input = TextInput(hint_text='Data de Aluguel (dd/mm/yyyy)', size_hint=(1, 0.1))
        self.add_widget(self.rent_date_input)

        # Entrada de Data de Devolução
        self.return_date_input = TextInput(hint_text='Data de Devolução (dd/mm/yyyy)', size_hint=(1, 0.1))
        self.add_widget(self.return_date_input)

        # Botão de Adicionar
        self.add_button = Button(text='Adicionar Aluguel', size_hint=(1, 0.1))
        self.add_button.bind(on_press=self.add_rental)
        self.add_widget(self.add_button)

        # Área de Listagem
        self.list_area = ScrollView(size_hint=(1, 0.6))
        self.list_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        self.list_area.add_widget(self.list_layout)
        self.add_widget(self.list_area)

        # Atualizar a lista de aluguéis
        self.update_rental_list()

    def add_rental(self, instance):
        name = self.name_input.text
        rent_date = self.rent_date_input.text
        return_date = self.return_date_input.text

        if name and rent_date and return_date:
            self.db.add_rental(name, rent_date, return_date)
            self.name_input.text = ''
            self.rent_date_input.text = ''
            self.return_date_input.text = ''
            self.update_rental_list()

    def delete_rental(self, rental_id):
        self.db.delete_rental(rental_id)
        self.update_rental_list()

    def update_rental_list(self):
        # Limpa a lista atual
        self.list_layout.clear_widgets()

        rentals = self.db.get_all_rentals()

        for rental in rentals:
            rental_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            rental_box.add_widget(Label(text=f"{rental[1]} - {rental[2]} até {rental[3]}", size_hint_x=0.8))

            delete_button = Button(text="Excluir", size_hint_x=0.2)
            delete_button.bind(on_press=lambda instance, rental_id=rental[0]: self.delete_rental(rental_id))
            rental_box.add_widget(delete_button)

            self.list_layout.add_widget(rental_box)

class RentalAppMain(App):
    def build(self):
        return RentalApp()

if __name__ == '__main__':
    RentalAppMain().run()
