from mpi4py import MPI
'''
def binary_search(arr, target):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Dividir la lista entre los procesos
    local_size = len(arr) // size
    start = rank * local_size
    end = start + local_size if rank < size - 1 else len(arr)

    low = start
    high = end - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid][0].lower() == target.lower():
            return arr[mid]
        elif arr[mid][0].lower() < target.lower():
            low = mid + 1
        else:
            high = mid - 1

    return None
'''
def binary_search(arr, target):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Dividir la lista entre los procesos
    local_size = len(arr) // size
    start = rank * local_size
    end = start + local_size if rank < size - 1 else len(arr)

    for i in range(start, end):
        if arr[i][0].lower() == target.lower():
            return arr[i]

    return None