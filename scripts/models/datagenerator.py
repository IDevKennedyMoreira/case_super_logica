import csv
import random
import uuid
from datetime import datetime

class DataGenerator:

    """
    Método construtor para a criação de dados para testes
    """
    def __init__(self, file_folder_destination):
        self._sufix = datetime.now().strftime('%m%d%Y%H%M%S')
        self._file_folder_destination = file_folder_destination
        
    """
    Gera nomes de pessoas aleatórios a partir dos arquivos presentes na pasta de matéria prima de dados (rawmaterial)
    """    
    def _generate_person_name(self, number_records):
        first_names = []
        last_names = []
        with open("rawmaterial/person_first_name.txt", "r") as urlFile:
            first_names = urlFile.read().split('\n')
        with open("rawmaterial/person_last_name.txt", "r") as urlFile:
            last_names = urlFile.read().split('\n')
        total = len(first_names) * len(last_names)
        sam = random.sample(range(total), number_records)
        persons_names = [f'{first_names[s // len(last_names)]} {last_names[s % len(last_names)]}' for s in sam]
        return persons_names
    
    """
    Gera endereços aleatórios a partir dos arquivos presentes na pasta de matéria prima de dados (rawmaterial)
    """    
    def _generate_address(self, number_records):
        public_places = []
        first_names = []
        last_names = []
        with open("rawmaterial/public_place.txt", "r") as places:
            public_places = places.read().split('\n')
        with open("rawmaterial/person_first_name.txt", "r") as firstname:
            first_names = firstname.read().split('\n')
        with open("rawmaterial/person_last_name.txt", "r") as lastname:
            last_names = lastname.read().split('\n')
        total = len(first_names) * len(public_places)
        sam = random.sample(range(total), number_records)
        addresses = [f'{public_places[s // len(public_places)]} {first_names[s // len(last_names)]} {last_names[s % len(last_names)]} N. {random.randint(0,1000)}' for s in sam]
        return addresses
    
    """
    Gera nomes de condominios aleatórios a partir dos arquivos presentes na pasta de matéria prima de dados (rawmaterial)
    """  
    def _get_random_townhouse_names(self, number_records):
        townhouse_names = []
        with open("rawmaterial/townhouse_name.txt", "r") as townhouse:
            townhouse_names = townhouse.read().split('\n')
        total = len(townhouse_names)
        sam = random.sample(range(total), number_records)
        townhouses = [f'{townhouse_names[s]}' for s in sam]
        return townhouses
    
    """
    Gera tipos de propriedade aleatórios a partir dos arquivos presentes na pasta de matéria prima de dados (rawmaterial)
    """ 
    def _get_ramdom_property_type(self, number_records):
        property_types = [] 
        with open("rawmaterial/property_type.txt", "r") as property:
            property_types = property.read().split('\n')
        total = len(property_types)
        sam = random.sample(range(total), number_records)
        property_types = [f'{property_types[s]}' for s in sam]
        return property_types
        
        
    """
    Um arquivo de morador deve conter:
        . Id de identificação do morador
        . Nome de morador
        . Condominio onde mora
    """    
    def create_resident_file(self):
        person_id_list = [f"{str(uuid.uuid4()).replace('-','')}" for i in range(3)]
        person_names_list = self._generate_person_name(3)
        townhouse_id_list = self.townhouse_id_list[:]
        with open(f"./datalake/landing/dim_moradores/moradores{self._sufix}.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(("morador_id", "morador_nome","condominio_id"))
            i = 0
            while i < 3:
                writer.writerow((person_id_list[i], person_names_list[i],townhouse_id_list[i]))
                i += 1
        return
        
    """
    Criar arquivos de propriedades na pasta de destino selecionada na construção do objeto
    Um  arquivo de imovel deve conter:
        .Id da propriedade
        .Tipo do imóvel
        .Id do condominio
        .Valor do imóvel
    """
    def create_property_file(self):
        property_id_list = [f"{str(uuid.uuid4()).replace('-','')}" for i in range(3)]
        property_type_list = self._get_ramdom_property_type(3)
        townhouse_id_list = []
        townhouse_id_list = self.townhouse_id_list[:]
        property_value_list = [f'R${str(random.randrange(200000, 800000))},00' for i in range(3)]
        with open(f"./datalake/landing/dim_imoveis/imoveis{self._sufix}.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(("imovel_id", "tipo", "condominio_id", "valor"))
            i = 0
            while i < 3:
                writer.writerow((property_id_list[i], property_type_list[i],townhouse_id_list[i], property_value_list[i]) )
                i += 1
        return
        
        
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
        with open(f"{self._file_folder_destination}/condominios{self._sufix}.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(("condominio_id", "condominio_nome","condominio_endereco"))
            i = 0
            while i < 3:
                writer.writerow((townhouse_id_list[i], townhouse_names_list[i],townhouse_address_list[i]))
                i += 1
        #Persistindo dados em objeto na memoria para gerar vinculo entre os arquivos
        self.townhouse_id_list = townhouse_id_list
        return