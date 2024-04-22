from mpi4py import MPI
from dbcon import connection
from quicksort import parallel_quicksort


def get_pokemon_names():
    client, db = connection()
    pokemon_collection = db['Pokemon']

    pokemon_documents = pokemon_collection.find({}, {"Name": 1})

    pokemon_names = [doc["Name"] for doc in pokemon_documents]

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    
    pokemon_names = parallel_quicksort(pokemon_names, comm)

    pokemons = [] 

    if rank == 0:  
        for name in pokemon_names:
            pokemon_number = pokemon_collection.find_one({"Name": name})["Pokedex Number"]
            pokemon = [name, pokemon_number]
            pokemons.append(pokemon)  

    client.close()

    return pokemons  

def get_pokemon_name_by_numbers():
    client, db = connection()
    pokemon_collection = db['Pokemon']

    pokemon_documents = pokemon_collection.find({}, {"Pokedex Number": 1})

    pokemon_numbers = [doc["Pokedex Number"] for doc in pokemon_documents]

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    pokemon_numbers = parallel_quicksort(pokemon_numbers, comm)

    pokemons = [] 

    if rank == 0:  
        for number in pokemon_numbers:
            pokemon_name = pokemon_collection.find_one({"Pokedex Number": number})["Name"]
            pokemon = [pokemon_name, number]
            pokemons.append(pokemon)  

    client.close()

    return pokemons

def binary_search(data, key, start_index, end_index):
    low = start_index
    high = end_index - 1
    while low <= high:
        mid = (low + high) // 2
        if data[mid][0] == key:
            return mid  
        elif data[mid][0] < key:
            low = mid + 1
        else:
            high = mid - 1
    return -1  

def show_pokemon(pokemons):
    count = 0
    for pokemon in pokemons:
            name, number = pokemon
            count += 1
            try:
                print(f"Nombre: {name}, Numero: {number}, Contador: {count}")
            except UnicodeEncodeError:
                print(f"Nombre: {name.encode('ascii', 'ignore').decode()}, Numero: {number}, Contador: {count}")
            print(f"Total de Pokemon: {count}")

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        print("¿Que te gustaria hacer?")
        print("1. Ordenar alfabeticamente")
        print("2. Ordenar por numero de Pokedex")
        print("3. Buscar un Pokemon por nombre")
        choice = input("Ingrese su eleccion (1, 2 o 3): ")
    else:
        choice = None

    choice = comm.bcast(choice, root=0)

    if choice == "1":
        pokemons = get_pokemon_names()
        show_pokemon(pokemons)
    elif choice == "2":
        pokemons = get_pokemon_name_by_numbers()
        show_pokemon(pokemons)
    elif choice == "3":
        if rank == 0:
            pokemon_name = input("Ingresa el nombre del Pokemon que deseas buscar: ")
        else:
            pokemon_name = None

        pokemon_name = comm.bcast(pokemon_name, root=0)
        pokemons = get_pokemon_names()
        index = binary_search(pokemons, pokemon_name, 0, len(pokemons))
        if index != -1:
            print("Pokemon encontrado:", pokemons[index][0])
        else:
            print("Pokemon no encontrado.")
    elif choice is None:
        print("Opción inválida")
        exit()
