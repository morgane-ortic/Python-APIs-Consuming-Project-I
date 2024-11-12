from retrieve_data import DataHandler

def main():
    data_handler = DataHandler()

    while True:
        print('----------------------------------------')
        print('1. Retrieve and save pokemon data')
        print('2. Show pokemon data')
        print('3. Exit\n')
        choice = input('Enter your choice: ')

        if choice == '1':
            while True:
                poke_num = input('\nHow many pokemons do you want to retrieve? (Leave empty to get 15)\n')
                if poke_num == '':
                    print('Retrieving pokemons from the website. Please wait... This can take up to a couple of minutes')
                    data_handler.get_data()
                    print('\nPokemons retrieved and saved.')
                    break
                else:
                    try:
                        poke_num = int(poke_num)
                        if poke_num in range(1, 151):
                            data_handler.get_data(poke_num)
                            print('\nPokemons retrieved and saved.')
                            break
                        else:
                            print('\nSorry, this is too many pokemons. 151 max.')
                    except ValueError:
                        print('\nThis is not a positive number! Unable to retrieve pokemons.')
        
        elif choice == '2':
            data_handler.show_data()

        elif choice == '3':
            print('Exiting...')
            break

        else:
            print('Invalid choice. Please try again.')

    data_handler.show_data()

if __name__ == '__main__':
    main()