import json, requests

class DataHandler:
    '''Class that will get and save the data'''

    def __init__(self):
        self.base_url = 'https://fakerapi.it/api/v2'
        self.pokemons = []
        self.images = []
        self.places = []

    def get_data(self, item_number=15):
        self.item_number = item_number
        self.get_pokemons()
        self.get_images()
        self.get_places()
        self.save_data()

    def show_data(self):
        self.create_dicts()
        self.print_data()

    def save_data(self):
        with open('pokemons.json', 'w') as f:
            json.dump(self.pokemons, f, indent=4)
        with open('images.json', 'w') as f:
            json.dump(self.images, f, indent=4)
        with open('places.json', 'w') as f:
            json.dump(self.places, f, indent=4)

    def read_json_file(self, data_type):
        with open(f'{data_type}.json', 'r') as file:
            return json.load(file)
        
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

    def create_dicts(self):

        if not self.pokemons:
            self.pokemons = self.read_json_file('pokemons')
        if not self.images:
            self.images = self.read_json_file('images')
        if not self.places:
            self.places = self.read_json_file('places')

        pokemons_num = len(self.pokemons)
        images_num = len(self.images)
        places_num = len(self.places)
        
        # in case the lists have a different number of items,
        # the script will leave aside the data that has no corresponding data in other lists
        dict_num = min(pokemons_num, images_num, places_num)

        self.poke_data = []
        for i in range(dict_num):
            pokelocation = {
                'pokemon': self.pokemons[i][f'pokemon_{i+1}'],
                'image': self.images[i][f'image_{i+1}'],
                'location': {
                    'latitude': self.places[i][f'latitude_{i+1}'],
                    'longitude': self.places[i][f'longitude_{i+1}']
                },
            }
            self.poke_data.append(pokelocation)


    def print_data(self):
        for i, pokemon in enumerate(self.poke_data, start=1):            
            print('--------')
            print(f'Pokemon {i}')
            print('--------')
            print(f'Name: {pokemon['pokemon']}')
            print(f'Image: {pokemon['image']}')
            print(f'Latitude: {pokemon['location']['latitude']}')
            print(f'Longitude: {pokemon['location']['longitude']}')
        print('--------')