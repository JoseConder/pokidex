import os
from bs4 import BeautifulSoup
from dbcon import connection
from mpi4py import MPI
import requests

# Función para descargar y guardar la imagen
def download_and_save_image(img_url, filename):
    if os.path.exists(filename):
        print(f"La imagen '{filename}' ya existe.")
        return False
    else:
        response = requests.get(img_url)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
            return True
        else:
            return False

# Función para procesar la información de los Pokémon
def process_pokemon_info(pokemon_list_section):
    for pokemon_card in pokemon_list_section.find_all('div', class_='infocard'):
        try:
            name = pokemon_card.find('a', class_='ent-name').text
            pokedex_number = pokemon_card.find('small').text.strip()
            existing_pokemon = pokemon_collection.find_one({"Name": name})

            if existing_pokemon:
                print(f"Salteando: {name} ya existe en la base de datos.")
            else:
                type_elements = pokemon_card.find_all('a', class_='itype')
                types = [type_element.text.strip() for type_element in type_elements]
                img_url = pokemon_card.find('img')['src']
                filename = f"./resources/pokemon/{name}.png"

                if download_and_save_image(img_url, filename):
                    print(f"Guardado: {filename}")
                    pokemon_data = {
                        "Name": name,
                        "Pokedex Number": pokedex_number,
                        "Types": types,
                        "Image": filename
                    }
                    result = pokemon_collection.insert_one(pokemon_data)
                    print("Pokemon insertado correctamente con ID:", result.inserted_id)
                    print(f"Se insertó: {name}, Número: {pokedex_number}, Tipo(s): {', '.join(types)}")
                else:
                    print(f"Fallo al descargar la imagen de: {name}")

        except Exception as e:
            print(f"Error procesando: {e}")

# Inicialización de MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Obtén la colección de MongoDB
client, db = connection()
pokemon_collection = db['Pokemon']

# Hacer el request a la URL
response = requests.get("https://pokemondb.net/pokedex/national")

if response.status_code == 200:
    # Parsear el HTML
    soup = BeautifulSoup(response.content, "html.parser")
    pokemon_list_sections = soup.find_all('div', class_='infocard-list infocard-list-pkmn-lg')

    # Distribuir trabajo entre procesos MPI
    chunk_size = len(pokemon_list_sections) // size
    start_index = rank * chunk_size
    end_index = (rank + 1) * chunk_size if rank < size - 1 else len(pokemon_list_sections)
    
    for i in range(start_index, end_index):
        process_pokemon_info(pokemon_list_sections[i])

else:
    print(f"Error al hacer la solicitud. Código de estado: {response.status_code}")

# Cerrar la conexión a la base de datos
client.close()
