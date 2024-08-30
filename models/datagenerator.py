import csv
import random
from datetime import date, datetime

class DataGenerator:

    def __init__(self, filename):
        self._sufix = datetime.today().strftime('%d/%m/%Y').replace('/','')
        self._filename = f"{filename}{self._sufix}"
        with open(f"{self._filename}.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(("years", "salary"))
            i = 0
            while i < 1000:
                years = random.randint(1, 10)
                salary = years * 200 + 2000 + random.randint(1, 400)
                writer.writerow((years, salary))
                i += 1
                
    def _generate_person_name(self, number_records):
        first_names = []
        last_names = []
        with open("./models/person_s.txt", "r") as urlFile:
            first_names = urlFile.read().split('\n')
        with open("./models/person_last_name.txt", "r") as urlFile:
            last_names = urlFile.read().split('\n')
        total = len(first_names) * len(last_names)
        sam = random.sample(range(total), number_records)
        persons_names = [f'{first_names[s // len(last_names)]} {last_names[s % len(last_names)]}' for s in sam]
        return persons_names
        
    def _generate_address(self, number_records):
        public_places = []
        first_names = []
        last_names = []
        with open("./models/public_place.txt", "r") as places:
            public_places = places.read().split('\n')
            print(public_places)
        with open("./models/person_first_name.txt", "r") as firstname:
            first_names = firstname.read().split('\n')
        with open("./models/person_last_name.txt", "r") as lastname:
            last_names = lastname.read().split('\n')
        total = len(first_names) * len(public_places)
        sam = random.sample(range(total), number_records)
        addresses = [f'{public_places[s // len(public_places)]} {first_names[s // len(last_names)]} {last_names[s % len(last_names)]} N. {random.randint(0,1000)}' for s in sam]
        return addresses
        
    def _get_random_townhouse_names(self, number_records):
        townhouse_names = []
        with open("./models/townhouse_name.txt", "r") as townhouse:
            townhouse_names = townhouse.read().split('\n')
        total = len(townhouse_names)
        sam = random.sample(range(total), number_records)
        townhouses = [f'{townhouse_names[s]}' for s in sam]
        return townhouses
        
    def _get_ramdom_property_type(self, number_records):
        property_types = [] 
        with open("./models/property_type.txt", "r") as property:
            property_types = property.read().split('\n')
        total = len(property_types)
        sam = random.sample(range(total), number_records)
        property_types = [f'{property_types[s]}' for s in sam]
        print(property_types)
        
        
    """
    Um arquivo de morador deve conter:
        . Nome de morador
        . Id de identificação do morador
        . Condominio onde mora
    """    
    def create_resident_file(self):
        person_names = self._generate_person_name(3)
        
    
    """
    Um  arquivo de 
    """
    
    def create_property_file(self):
        pass
    
    def create_transaction_file(self):
        pass
    
    def create_townhouse_file(self):
        pass
    
    
        
        
    