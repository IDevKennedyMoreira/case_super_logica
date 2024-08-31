import csv
import random
import uuid
from datetime import date, datetime

class DataGenerator:

    def __init__(self):
        self._townhouse_id_list = [0,1,2]
        self._sufix = datetime.today().strftime('%d/%m/%Y').replace('/','')
                
    def _generate_person_name(self, number_records):
        first_names = []
        last_names = []
        with open("./models/person_first_name.txt", "r") as urlFile:
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
        
        
    """
    Um arquivo de morador deve conter:
        . Id de identificação do morador
        . Nome de morador
        . Condominio onde mora
    """    
    def create_resident_file(self):
        person_id_list = [f"{str(uuid.uuid4()).replace('-','')}" for i in range(3)]
        person_names_list = self._generate_person_name(3)
        townhouse_names_list = self._get_random_townhouse_names(3)
        with open(f"moradores.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(("morador_id", "morador_nome","condominio_id"))
            i = 0
            while i < 3:
                writer.writerow((person_id_list[i], person_names_list[i],townhouse_names_list[i]))
                i += 1
        return
        
    """
    Um  arquivo de imovel deve conter:
        .Id da propriedade
        .Tipo do imóvel
        .Id do condominio
        .Valor do imóvel
    """
    def create_property_file(self):
        print(self.townhouse_id_list)
        property_id_list = [f"{str(uuid.uuid4()).replace('-','')}" for i in range(3)]
        property_type_list = self._get_ramdom_property_type(3)
        property_value_list = [f"R$ {str(random.randrange(200000, 800000))}" for i in range(3)]
        with open(f"imoveis.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(("imovel_id", "tipo", "condominio_id", "valor"))
            i = 0
            while i < 3:
                writer.writerow
                (
                    (
                        property_id_list[i], 
                        property_type_list[i],
                        self._townhouse_id_list[i], 
                        property_value_list[i]
                    )
                )
                i += 1
        return
        
        
        pass
    
    def create_transaction_file(self):
        pass
    
    """
    Um arquivo de condominio deve conter:
        . Id do condominio
        . Nome do condominio
        . Endereco do condominio
    """    
    def create_townhouse_file(self):
        townhouse_id_list = [f"{str(uuid.uuid4()).replace('-','')}" for i in range(3)]
        townhouse_names_list = self._get_random_townhouse_names(3)
        townhouse_address_list = self._generate_address(3)
        with open(f"../storage/condominios.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(("condominio_id", "condominio_nome","condominio_endereco"))
            i = 0
            while i < 3:
                writer.writerow((townhouse_id_list[i], townhouse_names_list[i],townhouse_address_list[i]))
                i += 1
        #Persistindo dados em objeto na memoria para gerar vinculo entre os arquivos
        self.townhouse_id_list = townhouse_id_list
        return
    
    """
    Método para orquestração de criação de arquivos
    """ 
    def create_files(self):
        self.create_townhouse_file()
