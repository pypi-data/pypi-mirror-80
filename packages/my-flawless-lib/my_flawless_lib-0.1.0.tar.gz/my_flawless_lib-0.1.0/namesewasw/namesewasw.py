import names

def print_name():
    name = names.get_full_name()
    print(f'{name} długość: {len(name) - 1}')