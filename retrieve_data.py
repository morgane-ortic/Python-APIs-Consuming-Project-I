import json, requests

class DataHandler:
    '''Class that will get and save the data'''

    def __init__(self, item_number):
        self.base_url = 'https://fakerapi.it/api/v2'
        self.item_number = item_number
        self.pokemons = []
        self.images = []
        self.places = []

    def get_data(self):
        self.get_pokemons()
        self.get_images()
        self.get_places()
        self.save_data()

    def save_data(self):
        with open('pokemons.json', 'w') as f:
            json.dump(self.pokemons, f, indent=4)
        with open('images.json', 'w') as f:
            json.dump(self.images, f, indent=4)
        with open('places.json', 'w') as f:
            json.dump(self.places, f, indent=4)
        

    def get_pokemons(self):
        for i in range(self.item_number):
            response = requests.get(f'{self.base_url}/custom?_quantity=1&customfield1=pokemon')
            response_data = response.json()
            pokemon_name = response_data['data'][0].get('customfield1')
            self.pokemons.append({f'pokemon_{i+1}': pokemon_name})

    def get_images(self):
        for i in range(self.item_number):
            response = requests.get(f'{self.base_url}/images?_quantity=1&_type=pokemon')
            response_data = response.json()
            image_url = response_data['data'][0].get('url')
            self.images.append({f'image_{i+1}': image_url})

    def get_places(self):
        for i in range(self.item_number):
            response = requests.get(f'{self.base_url}/places?_quantity=1')
            response_data = response.json()
            latitude = response_data['data'][0].get('latitude')
            longitude = response_data['data'][0].get('longitude')
            self.places.append({f'latitude_{i+1}': latitude, f'longitude_{i+1}': longitude})