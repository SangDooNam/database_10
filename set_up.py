import psycopg2
import os
import dotenv

dotenv.load_dotenv()

def setup(command_create_roles, 
        command_create_time_range,
        command_check_type,
        command_create_table,
        command_insert,
        data):
    
    conn = None
    
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('PASSWORD'),
            port=os.getenv('DB_PORT')
        )

        cursor = conn.cursor()
        
        def type_exists(type_name):
            cursor.execute(command_check_type, (type_name,))
            return cursor.fetchone() is not None
        
        def row_exists(id):
            cursor.execute('SELECT id FROM site_user WHERE id = %s' , (id,))
            return cursor.fetchone() is not None
        
        if not type_exists('roles'):
            cursor.execute(command_create_roles)
        if not type_exists('time_range'):
            cursor.execute(command_create_time_range)
        
        cursor.execute(command_create_table)
        
        for dictonary in data:
            insert_data = (
                dictonary['name'],
                dictonary['role'],
                dictonary['birthdate'],
                dictonary['siblings'],
                dictonary['availability'],
                dictonary['site_settings'],
                dictonary['created_on']
            )
            if not row_exists(dictonary['id']):
                cursor.execute(command_insert, insert_data)
        
        cursor.execute('SELECT * FROM site_user;')
        rows = cursor.fetchall()
        
        print("{:<3} | {:<15} | {:<40} | {:<7} | {:<10} | {:<12} | {:<20} | {:<200} | {:<20} | {:<20} | {:<20}".format(
            "ID","Name","UUID","Avatar","Role","Birthdate","Siblings","Availability","Site settings","Created on","Avtive_for"
        ))
        print('-' * 230)
        for row in rows:
            print("{:<3} | {:<15} | {:<40} | {:<7} | {:<10} | {:<12} | {:<20} | {:<200} | {:<20} | {:<20} | {:<20}".format(
                *(str(value) if value is not None else '' for value in row)
            ))
        
        
        
        conn.commit()
        cursor.close()
        
    except(Exception, psycopg2.DatabaseError) as error:
        raise error
    finally:
        if conn is not None:
            conn.close()

command_create_roles = """
                        CREATE TYPE roles AS ENUM(
                                    'Anonymous',
                                    'Guest',
                                    'User',
                                    'Moderator',
                                    'Admin'
                                    );"""


command_create_time_range = """
                            CREATE TYPE time_range AS(
                            time_range JSONB[])"""


command_check_type = """
                    SELECT typname 
                    FROM pg_catalog.pg_type 
                    WHERE typname = %s;
                    """


command_create_table = """
                    CREATE TABLE IF NOT EXISTS site_user (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    uuid UUID DEFAULT uuid_generate_v4(),
                    avatar BYTEA,
                    role ROLES DEFAULT 'Anonymous',
                    birthdate DATE,
                    siblings TEXT[],
                    availability time_range,
                    site_settings JSON,
                    created_on TIMESTAMP,
                    active_for INTERVAL DAY 
                    );"""

command_insert = """INSERT INTO site_user (
                name,  
                role,
                birthdate, 
                siblings, 
                availability,
                site_settings,
                created_on)
                VALUES (
                    %s ,%s ,%s ,%s , ROW(%s::JSON[]) , %s, %s);
                """


data = [
    {'id':'1',
    'name':'Miriam Valira',
    'role':'Admin',
    'birthdate':'1995-08-29',
    'siblings':['Dani', 'Louis'],
    'availability':['{"start_time": "12:00:00"}','{"end_time": "15:00:00"}'],
    'site_settings':'{"background": "red", "notifications": false}',
    'created_on':'2015-09-23 08:56:00'
    },
    {'id':'2',
    'name':'Johann Müller',
    'role':'User',
    'birthdate':'2002-05-09',
    'siblings':[],
    'availability':['{"start_time": "09:00:00"}','{"end_time": "14:00:00"}',
                     '{"start_time": "18:00:00"}','{"end_time": "20:00:00"}'],
    'site_settings':'{"notifications": true}',
    'created_on':'2017-05-01 13:03:00'
    },
    {'id':'3',
    'name':'Louise Clark',
    'role':'Moderator',
    'birthdate':'1992-05-03',
    'siblings':['Monique'],
    'availability':['{"start_time": "09:00:00"}','{"end_time": "12:00:00"}',
                     '{"start_time": "13:00:00"}','{"end_time": "17:00:00"}'],
    'site_settings':'{"notifications": true}',
    'created_on':'2007-03-21 10:31:00'
    }
    ]


if __name__=='__main__':
    setup(command_create_roles, 
        command_create_time_range,
        command_check_type,
        command_create_table,
        command_insert,
        data)