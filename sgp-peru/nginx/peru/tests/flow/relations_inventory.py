from faker import Faker
from faker.providers import BaseProvider
import random
fake = Faker()

   
class ThemeInventory(BaseProvider):
    def theme_inventory(self):    
        theme_inventory = random.choice(['Seguimiento estadístico', 'Registros de empresas nuevas'])
        return theme_inventory

class ThematicInventory(BaseProvider):
    def thematic_inventory(self):    
        thematic_inventory = random.choice(['Empleo', 'Gobierno', 'Economía'])
        return thematic_inventory

class StatusInventory(BaseProvider):
    def status_inventory(self):    
        status_inventory = random.choice(['Activo', 'Inactivo'])
        return status_inventory


class TypeFormatSample(BaseProvider):
    def type_format(self):
        type_format = random.choice(['.xml', '.csv', '.xls'])    
        return type_format

class TransferMediumSample(BaseProvider):
    def transfer_medium(self):
        transfer_medium = random.choice(['ftp', 'bdd', 'drive'])    
        return transfer_medium
    
class TagsSample(BaseProvider):
    def tags_sample(self):
        tags_sample = random.choice(['Noticias', 'Eventos', 'Emprendimientos'])    
        return tags_sample
    
class VariablesSample(BaseProvider):
    def variable_sample(self):
        variable_sample = random.choice(['Nombre', 'Apellido', 'Estrato'])    
        return variable_sample
    

