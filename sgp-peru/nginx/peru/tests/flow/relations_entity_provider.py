from faker import Faker
from faker.providers import BaseProvider
import random
fake = Faker()

   
class SectorEntity(BaseProvider):
    def type_sector(self):    
        type_sector = random.choice(['Agropecuario', 'Textil', 'Financiero'])
        return type_sector

class TypeEntity(BaseProvider):
    def type_entity(self):    
        type_entity = random.choice(['Mixta', 'Privada', 'Publica'])
        return type_entity

class StatusEntity(BaseProvider):
    def status(self):    
        status = random.choice(['Activo', 'Inactivo'])
        return status


class DomainEntity(BaseProvider):
    def domain(self):    
        return f'www{fake.first_name().lower()}.com'
    