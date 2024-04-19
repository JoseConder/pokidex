import tkinter as tk
from PIL import Image, ImageTk
from dbcon import connection
from show import get_pokemon_names, get_pokemon_name_by_numbers

def get_pokemon_data():
    client, db = connection()
    pokemon_collection = db['Pokemon']

    pokemon_documents = pokemon_collection.find({}, {"Name": 1, "Pokedex Number": 1})

    pokemons = [(doc["Name"], doc["Pokedex Number"]) for doc in pokemon_documents]

    client.close()

    return pokemons

class PokemonViewer:
    def __init__(self, pokemons):
        self.pokemons = pokemons
        self.index = 0

        self.window = tk.Tk()
        self.window.title("Pokédex")

        self.label_name = tk.Label(self.window)
        self.label_name.pack()

        self.label_number = tk.Label(self.window)
        self.label_number.pack()

        self.label_image = tk.Label(self.window)
        self.label_image.pack()

        # Botones para navegar entre los Pokémon
        self.button_previous = tk.Button(self.window, text="Anterior", command=self.show_previous_pokemon)
        self.button_previous.pack(side=tk.LEFT)

        self.button_next = tk.Button(self.window, text="Siguiente", command=self.show_next_pokemon)
        self.button_next.pack(side=tk.RIGHT)

        # Botones para seleccionar la lista a usar
        self.button_sort_by_name = tk.Button(self.window, text="Sort by Name", command=self.sort_by_name)
        self.button_sort_by_name.pack(side=tk.LEFT)

        self.button_sort_by_number = tk.Button(self.window, text="Sort by Number", command=self.sort_by_number)
        self.button_sort_by_number.pack(side=tk.RIGHT)

        self.show_pokemon()

    def show_pokemon(self):
        name, number = self.pokemons[self.index]

        self.label_name.config(text=f"Nombre: {name}")
        self.label_number.config(text=f"Número: #{number}")

        image_path = f"resources/pokemon/{name}.png"
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)

        self.label_image.config(image=photo)
        self.label_image.image = photo

    def show_previous_pokemon(self):
        self.index = (self.index - 1) % len(self.pokemons)
        self.show_pokemon()

    def show_next_pokemon(self):
        self.index = (self.index + 1) % len(self.pokemons)
        self.show_pokemon()

    def sort_by_name(self):
        self.pokemons = get_pokemon_names()
        self.index = 0
        self.show_pokemon()

    def sort_by_number(self):
        self.pokemons = get_pokemon_name_by_numbers()
        self.index = 0
        self.show_pokemon()

    def run(self):
        self.window.mainloop()

pokemons = get_pokemon_data()
viewer = PokemonViewer(pokemons)
viewer.run()