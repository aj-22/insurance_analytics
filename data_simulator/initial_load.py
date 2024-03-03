from connection import SQL
from faker import Faker
import uuid
from datetime import datetime
import os
import random

class Dry_Loader:
    def __init__(self):
        self.sql = SQL()
        self.faker = Faker('en_IN')

    def create_fake_person(self):
        first_name = self.faker.first_name()
        last_name = self.faker.first_name()
        date_of_birth = self.faker.date()
        return first_name, last_name, date_of_birth

    def fetch_cities(self):
        self.sql.cursor.execute('SELECT name_of_city FROM dev.cities')
        return self.sql.cursor.fetchall()
    
    def load_agents(self, number = 10):
        cities = self.fetch_cities()
        for _ in range(number):
            agent_id = 'agent-' + str(uuid.uuid4())
            first_name, last_name, date_of_birth = self.create_fake_person()
            city = random.choice(cities)[0]
            hire_date = str(datetime.now().strftime('%Y-%m-%d'))

            self.sql.cursor.execute(f'''INSERT INTO staging.agent values('{agent_id}', '{first_name}', '{last_name}', \
                             '{city}', '{date_of_birth}', '{hire_date}', current_timestamp)''')
            self.sql.cursor.commit()

    def __del__(self):
        del self.sql

if __name__ == '__main__':
    loader = Dry_Loader()
    loader.load_agents(80)



