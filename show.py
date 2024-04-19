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

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    count = 0

    if rank == 0:
        print("Ordenar por Alfabeto o por Numero?")
        print("1. Alfabeto \n2. Numero")
        choice = input("Ingrese su eleccion (1 o 2): ")
    else:
        choice = None

    choice = comm.bcast(choice, root=0)

    if choice == "1":
        pokemons = get_pokemon_names()
    elif choice == "2":
        pokemons = get_pokemon_name_by_numbers()
    elif choice == None:
        print("Opcion Invalida")
        exit()

    if rank == 0:
        for pokemon in pokemons:
            name, number = pokemon
            count += 1
            try:
                print(f"Nombre: {name}, Numero: {number}, Cuenta: {count}")
            except UnicodeEncodeError:
                print(f"Nombre: {name.encode('ascii', 'ignore').decode()}, Numero: {number}, Cuenta: {count}")
        print(f"Total de pokemons: {count}")
