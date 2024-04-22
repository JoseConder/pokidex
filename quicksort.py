from mpi4py import MPI

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivote = arr[len(arr) // 2]
    izquierda = [x for x in arr if x < pivote]
    medio = [x for x in arr if x == pivote]
    derecha = [x for x in arr if x > pivote]
    return quicksort(izquierda) + medio + quicksort(derecha)

def parallel_quicksort(arr, comm):
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    chunks = None
    if size == 1:
        return quicksort(arr)
    
    local_elements = None
    if rank == 0:
        chunks = [[] for _ in range(size)]
        chunk_size = len(arr) // size
        for i in range(size - 1):
            chunks[i] = arr[i * chunk_size:(i + 1) * chunk_size]
        chunks[size - 1] = arr[(size - 1) * chunk_size:]
        local_elements = chunks[0]
    
    local_elements = comm.scatter(chunks, root=0)
    local_elements = quicksort(local_elements)
    sorted_arr = comm.gather(local_elements, root=0)
    
    if rank == 0:
        return quicksort([elem for sublist in sorted_arr for elem in sublist])
