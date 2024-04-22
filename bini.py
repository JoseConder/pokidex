from mpi4py import MPI
from show import get_pokemon_names

def binary_search(data, key, start_index, end_index):
    low = start_index
    high = end_index - 1
    while low <= high:
        mid = (low + high) // 2
        if data[mid][0] == key:
            return data[mid][1], mid  # Devuelve tanto el Pokémon encontrado como su índice
        elif data[mid][0] < key:
            low = mid + 1
        else:
            high = mid - 1
    return "", -1  # Valor sentinela para indicar que el Pokémon no fue encontrado


if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    pokemon_data = get_pokemon_names()

    chunk_size = len(pokemon_data) // size
    remainder = len(pokemon_data) % size

    if rank < remainder:
        chunk_size += 1

    start_index = rank * chunk_size
    end_index = min(start_index + chunk_size, len(pokemon_data))

    # Realiza la búsqueda binaria solo en los índices que le corresponden al proceso actual
    result, index = binary_search(pokemon_data, 'Gabite', start_index, end_index)


    # Reduce los resultados de búsqueda de todos los procesos a un solo resultado
    final_index = comm.reduce(index, op=MPI.MAX, root=0)

    # Proceso 0 muestra el resultado final
    if rank == 0:
        if final_index != -1:  # Si se encontró el Pokémon en al menos una partición
            print("Pokemon encontrado:", pokemon_data[final_index][0])
        else:
            print("Pokemon no encontrado.")