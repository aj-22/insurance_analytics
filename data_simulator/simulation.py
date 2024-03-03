import connection
from faker import Faker
import uuid
from datetime import datetime
import os
import random
from connection import SQL
import json
import time

class Lead_Generator:
    def __init__(self):
        self.output_dir = '''.\\data_output'''
        self.sql = SQL()
        self.faker = Faker('en_IN')
        
        self.sql.cursor.execute('SELECT trim(name_of_city) FROM dev.cities')
        self.cities = self.sql.cursor.fetchall()

        self.sql.cursor.execute('''SELECT agent_id FROM staging.agent;''')
        self.agents = self.sql.cursor.fetchall()

        self.sql.cursor.execute('''SELECT lead_id, first_name, last_name, city, date_of_birth, agent_id, lead_status 
                                FROM dev.bronze__vw_lead_lambda
                                where lead_status not in ('Dropped','Converted');
                                ''')
        self.existing_leads = self.sql.cursor.fetchall()

    def create_fake_person(self):
        first_name = self.faker.first_name()
        last_name = self.faker.first_name()
        date_of_birth = self.faker.date()
        return first_name, last_name, date_of_birth

    def create_new_lead(self):
        cities = self.cities
        agents = self.agents

        lead_id = 'lead-' + str(uuid.uuid4())
        first_name, last_name, date_of_birth = self.create_fake_person()
        city = random.choice(cities)[0]
        agent_id = random.choice(agents)[0]
        lead_status = 'New'
        loaded_at = str(datetime.now())

        return {
            'lead_id':lead_id,
            'first_name':first_name,
            'last_name':last_name,
            'city':city,
            'date_of_birth':date_of_birth,
            'agent_id':agent_id,
            'lead_status':lead_status,
            'loaded_at':loaded_at
        }

    def insert_customer_lead_mapping(self, lead_id, customer_id):
        self.sql.cursor.execute(f'''insert into staging.customer_lead_mapping values ('{lead_id}','{customer_id}',current_timestamp)''')
        self.sql.cursor.commit()

    def insert_customer(self, customer_id, first_name, last_name, city, date_of_birth ):
        self.sql.cursor.execute(f'''insert into staging.customer values ('{customer_id}', \
                                '{first_name}', '{last_name}', '{city}', '{date_of_birth}', current_timestamp)''')
        self.sql.cursor.commit()

    def insert_policy(self,customer_id):
        policy_id = 'policy-'+ str(uuid.uuid4())
        policy_type = random.choice(['Life','Auto','Health'])
        coverage_details = 'Details'
        premium_amount = random.choice([250,500,750,1000])
        datetime_now = datetime.now()
        start_date = str(datetime_now.strftime('%Y-%m-%d'))
        future_years = random.choice([1,2,3,4,5])
        future_date = datetime(datetime_now.year+future_years, datetime_now.month, datetime_now.day, datetime_now.hour, 
                               datetime_now.minute, datetime_now.second, 0)
        end_date = str(future_date.strftime('%Y-%m-%d'))

        self.sql.cursor.execute(f'''insert into staging.policy values ('{policy_id}', '{policy_type}', \
                        '{coverage_details}', {premium_amount}, '{start_date}', '{end_date}', \
                        '{customer_id}', current_timestamp)''')
        self.sql.cursor.commit()

    def update_existing_lead(self):
        if len(self.existing_leads) < 1:
            return self.create_new_lead()

        lead_id, first_name, last_name, city, date_of_birth, agent_id, lead_status = random.choice(self.existing_leads)

        self.existing_leads = [elem for elem in self.existing_leads if elem[0] != lead_id]

        if lead_status == 'New':
            lead_status = 'Contacted'
        elif lead_status == 'Contacted':
            lead_status = 'In Process'
        elif lead_status == 'In Process':
            if random.random() > 0.5:
                lead_status = 'Converted'
            else:
                lead_status = 'Dropped'

        if lead_status == 'Converted':
            customer_id = 'cust-' + str(uuid.uuid4())
            self.insert_customer_lead_mapping(lead_id, customer_id)
            self.insert_customer(customer_id, first_name, last_name, city, date_of_birth)
            self.insert_policy(customer_id)

        return {
            'lead_id':lead_id,
            'first_name':first_name,
            'last_name':last_name,
            'city':city,
            'date_of_birth':str(date_of_birth),
            'agent_id':agent_id,
            'lead_status':lead_status,
            'loaded_at':str(datetime.now())
        }

    def write_data(self, data):
        filename = 'TXN'+datetime.now().strftime("%Y%m%d%H%M%S%f") +'.json'
        with open(self.output_dir + '\\' + filename, 'w') as f:
            f.write(json.dumps(data))

    def generate_leads(self, number = 20):
        for _ in range(number):
            if random.random() > 0.6:
                data = self.create_new_lead()
            else:
                data = self.update_existing_lead()
            self.write_data(data)
            time.sleep(0.5)
        
        

if __name__ == '__main__':
    generator = Lead_Generator()
    generator.generate_leads()