import requests
from datetime import datetime
from app import db  
from models import People, Planets  

# Base URL de la API SWAPI
SWAPI_BASE_URL = 'https://www.swapi.tech/api/'

# Función para obtener y almacenar datos de una categoría
def fetch_and_store_data(category):
    url = f"https://www.swapi.tech/api/{category}"
    page = 1
    
    while True:
        response = requests.get(f"{url}?page={page}")

        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code} - {response.text}")
            break

        data = response.json()
        print(data)  # Ver la respuesta completa para depuración
        
        # Asegúrate de que la respuesta contiene la clave 'meta'
        if 'meta' not in data:
            print("No 'meta' key in response data. Exiting.")
            break

        total_pages = data['meta']['total_pages']  # Obtiene el número total de páginas
        
        # Procesar los elementos
        for item in data['results']:

            # Para personas
            if category == 'people':
                person_data = {
                    'id': item['uid'],
                    'birth_year': item['properties']['birth_year'],
                    'eye_color': item['properties']['eye_color'],
                    'films': item['properties']['films'],  # Asumiendo que es un array de URLs
                    'gender': item['properties']['gender'],
                    'hair_color': item['properties']['hair_color'],
                    'height': item['properties']['height'],
                    'homeworld': item['properties']['homeworld'],
                    'mass': item['properties']['mass'],
                    'name': item['properties']['name'],
                    'skin_color': item['properties']['skin_color'],
                    'created': datetime.strptime(item['properties']['created'], "%Y-%m-%dT%H:%M:%S.%fZ"),
                    'edited': datetime.strptime(item['properties']['edited'], "%Y-%m-%dT%H:%M:%S.%fZ"),
                    'species': item['properties']['species'],  # Asumiendo que es un array de URLs
                    'starships': item['properties']['starships'],  # Asumiendo que es un array de URLs
                    'url': item['url'],
                    'vehicles': item['properties']['vehicles']  # Asumiendo que es un array de URLs
                }
                # Llamar a la función para guardar en la base de datos
                save_person_to_db(person_data)

                print(item)

            # Para planetas
            elif category == 'planets':
                planet_data = {
                    'id': item['uid'],
                    'name': item['properties']['name'],
                    'climate': item['properties']['climate'],
                    'diameter': item['properties']['diameter'],
                    'gravity': item['properties']['gravity'],
                    'orbital_period': item['properties']['orbital_period'],
                    'population': item['properties']['population'],
                    'residents': item['properties']['residents'],  # Asumiendo que es un array de URLs
                    'rotation_period': item['properties']['rotation_period'],
                    'surface_water': item['properties']['surface_water'],
                    'terrain': item['properties']['terrain'],
                    'url': item['url']
                }
                # Llamar a la función para guardar en la base de datos
                save_planet_to_db(planet_data)

        # Incrementar el número de página
        page += 1

# Funciones para guardar los datos en la base de datos
def save_person_to_db(person_data):
    new_person = Person(
        id=person_data['id'],
        birth_year=person_data['birth_year'],
        eye_color=person_data['eye_color'],
        films=person_data['films'],
        gender=person_data['gender'],
        hair_color=person_data['hair_color'],
        height=person_data['height'],
        homeworld=person_data['homeworld'],
        mass=person_data['mass'],
        name=person_data['name'],
        skin_color=person_data['skin_color'],
        created=person_data['created'],
        edited=person_data['edited'],
        species=person_data['species'],
        starships=person_data['starships'],
        url=person_data['url'],
        vehicles=person_data['vehicles']
    )
    db.session.add(new_person)
    db.session.commit()  # Guardar los cambios en la base de datos

def save_planet_to_db(planet_data):
    new_planet = Planet(
        id=planet_data['id'],
        name=planet_data['name'],
        climate=planet_data['climate'],
        diameter=planet_data['diameter'],
        gravity=planet_data['gravity'],
        orbital_period=planet_data['orbital_period'],
        population=planet_data['population'],
        residents=planet_data['residents'],
        rotation_period=planet_data['rotation_period'],
        surface_water=planet_data['surface_water'],
        terrain=planet_data['terrain'],
        url=planet_data['url']
    )
    db.session.add(new_planet)
    db.session.commit()  # Guardar los cambios en la base de datos

# Función principal para ejecutar el fetch y almacenamiento
def main():
    fetch_and_store_data('people')  # Obtener y almacenar datos de personas
    fetch_and_store_data('planets')  # Obtener y almacenar datos de planetas

if __name__ == '__main__':
    main()
