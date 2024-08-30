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
                
    def _generate_person_name(self):
        first_name = []
        last_name = []
        with open("./models/person_first_name.txt", "r") as urlFile:
            first_name = urlFile.read().split('\n')
        with open("./models/person_last_name.txt", "r") as urlFile:
            last_name = urlFile.read().split('\n')
        total = len(first_name) * len(last_name)
        sam = random.sample(range(total), 100)
        names = [f'{first_name[s // len(last_name)]} {last_name[s % len(last_name)]}' for s in sam]
        print(names)
        
    def _generate_address(self):
        public_places = []
        first_name = []
        last_name = []
        with open("./models/public_place.txt", "r") as places:
            public_places = places.read().split('\n')
            print(public_places)
        with open("./models/person_first_name.txt", "r") as firstname:
            first_name = firstname.read().split('\n')
        with open("./models/person_last_name.txt", "r") as lastname:
            last_name = lastname.read().split('\n')
        total = len(first_name) * len(public_places)
        sam = random.sample(range(total), 100)
        addresses = [f'{public_places[s // len(public_places)]} {first_name[s // len(last_name)]} {last_name[s % len(last_name)]} N. {random.randint(0,1000)}' for s in sam]
        return addresses
        
    def _get_random_townhouse_name(sefl):
        townhouse_name = []
        with open("./models/townhouse_name.txt", "r") as townhouse:
            townhouse_name = townhouse.read().split('\n')
            print(townhouse_name)
        total = len(townhouse_name)
        sam = random.sample(range(total), 100)
        print(sam)
        townhouses = [f'{townhouse_name[s]}' for s in sam]
        print(townhouses)
        
    