import pymongo

def connection():
    client = pymongo.MongoClient('localhost', 27017)
    db = client['Pokedex'] 
    return client, db

def dropCollection(name):
    client, db = connection()

    #verificar si la colección existe
    if name in db.list_collection_names():
        colección = db[name]
        colección.drop()
        print(f"La colección '{name}' ha sido eliminada.")
    else:
        print(f"La colección '{name}' no existe.")
