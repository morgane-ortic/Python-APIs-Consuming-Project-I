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
            living_place, country_code = self.get_places_extra(latitude, longitude)
            self.places.append({f'latitude_{i+1}': latitude, f'longitude_{i+1}': longitude, f'living_place_{i+1}': living_place, f'country_code_{i+1}': country_code})


    def get_places_extra(self, latitude, longitude):
        config = self.read_json_file('config')
        geonames_username = config['geonames_username']

        for i in range(self.item_number):
            # calculate coordinates of a 50km box around the point
            north = str(latitude + 0.225)
            south = str(latitude - 0.225)
            east = str(longitude + 0.225)
            west = str(longitude - 0.225)

            response = requests.get(f'http://api.geonames.org/citiesJSON?north={north}&south={south}&east={east}&west={west}&lang=de&username={geonames_username}')
            response_data = response.json()
            nearby_places = response_data.get('geonames', [])

            if not nearby_places:
                living_place = 'the ocean'
                country_code = 'N/A'
            else:
                living_place, country_code = self.get_closest_place(nearby_places, latitude, longitude)
            return living_place, country_code


    def get_closest_place(self, nearby_places, latitude, longitude):
        closest_place = None
        min_distance = float('inf')
        for place in nearby_places:
            place_lat = float(place['lat'])
            place_lon = float(place['lng'])
            distance = ((latitude - place_lat) ** 2 + (longitude - place_lon) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_place = place['name']
                country_code = place['countrycode']
        return closest_place, country_code     


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
                    'living_place': self.places[i][f'living_place_{i+1}'],
                    'country_code': self.places[i][f'country_code_{i+1}'],
                    'latitude': self.places[i][f'latitude_{i+1}'],
                    'longitude': self.places[i][f'longitude_{i+1}']
                },
            }
            self.poke_data.append(pokelocation)

    def print_data(self):
        code_table = self.read_json_file('country_codes')
        self.code_to_name_map = {country['code']: country['name'] for country in code_table}
        for i, pokemon in enumerate(self.poke_data, start=1):
            country_code = pokemon['location']['country_code']         
            country_name = self.code_to_name_map.get(country_code, "Unknown country code")
            print('--------')
            print(f'Pokemon {i}')
            print('--------')
            print(f'Name: {pokemon['pokemon']}')
            print(f'Image: {pokemon['image']}')
            print(f'Living Place: {pokemon['location']['living_place']}')
            print(f'Country: {country_name}')
            print(f'Latitude: {pokemon['location']['latitude']}')
            print(f'Longitude: {pokemon['location']['longitude']}')
        print('--------')