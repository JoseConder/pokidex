import tkinter as tk
from PIL import Image, ImageTk
from mpi4py import MPI
from dbcon import connection
from show import get_pokemon_names, get_pokemon_name_by_numbers, binary_search, binary_search_by_number
from tkinter import messagebox
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
        self.button_sort_by_name = tk.Button(self.window, text="Ordenar por Nombre", command=self.sort_by_name)
        self.button_sort_by_name.pack(side=tk.LEFT)

        self.button_sort_by_number = tk.Button(self.window, text="Ordenar por Número", command=self.sort_by_number)
        self.button_sort_by_number.pack(side=tk.RIGHT)

        self.entry_search = tk.Entry(self.window)
        self.entry_search.pack()

        self.button_search = tk.Button(self.window, text="Buscar por Nombre", command=self.search_pokemon)
        self.button_search.pack()
        # Entry para buscar por número
        self.entry_search_number = tk.Entry(self.window)
        self.entry_search_number.pack()

        # Botón para buscar por número
        self.button_search_number = tk.Button(self.window, text="Buscar por Número", command=self.search_pokemon_by_number)
        self.button_search_number.pack()

        self.show_pokemon()

    def show_pokemon(self):
        name, number = self.pokemons[self.index]

        self.label_name.config(text=f"Nombre: {name}")
        self.label_number.config(text=f"Número: {number}")

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

    def sort_by_name2(self):
        self.pokemons = get_pokemon_names()
        self.index = 0
        return self.pokemons

    def sort_by_number(self):
        self.pokemons = get_pokemon_name_by_numbers()
        self.index = 0
        self.show_pokemon()
    def sort_by_number2(self):
        self.pokemons = get_pokemon_name_by_numbers()
        self.index = 0
        return self.pokemons
    def sort_by_name2(self):
        self.pokemons = get_pokemon_names()
        self.index=0
        return self.pokemons
    
    def search_pokemon(self):
        pokemons = self.sort_by_name2()
        pokemons = [(name.lower(), number) for name, number in pokemons]
        search_term = self.entry_search.get().lower()
        index = binary_search(pokemons, search_term, 0, len(pokemons))
        if index != -1:
            self.index = index
            self.show_pokemon()
        else:
            print(f"No se encontró ningún Pokémon con el nombre '{search_term}'")
            messagebox.showinfo("Pokémon no encontrado", f"No se encontró ningún Pokémon con el nombre '{search_term}'")

    
    def search_pokemon_by_number(self):
        # Ordenamos la lista de Pokémon por número si aún no está ordenada
        if not all(self.pokemons[i][1] <= self.pokemons[i+1][1] for i in range(len(self.pokemons)-1)):
            self.pokemons = self.sort_by_number2()

        try:
            number_str = "#" + self.entry_search_number.get().zfill(4)  # Asegura que el número tenga 4 dígitos y el prefijo "#"
            result = binary_search_by_number(self.pokemons, number_str, 0, len(self.pokemons))
            if result:
                self.index = self.pokemons.index(result)
                self.show_pokemon()
            else:
                messagebox.showinfo("Pokémon no encontrado", f"No se encontró ningún Pokémon con el número '{number_str}'")
        except ValueError:
            messagebox.showinfo("Error", "Por favor, introduce un número válido.")

    def run(self):
        self.window.mainloop()

comm = MPI.COMM_WORLD

if comm.Get_rank() == 0:
    pokemons = get_pokemon_data()
    viewer = PokemonViewer(pokemons)
    viewer.run()
else:
    pass