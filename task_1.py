import psycopg2
import os
import dotenv

dotenv.load_dotenv()

def task_1(command):
    
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
        cursor.execute(command)
        
        rows = cursor.fetchall()
        
        print("{:<20}".format("Name"))
        print('-'*22)
        for row in rows:
            print("{:<20}".format(*(str(value) if value is not None else '' for value in row)))
        
    
    except(Exception, psycopg2.DatabaseError) as error: 
        raise error
    
    finally:
        if conn is not None:
            conn.close()


command = """SELECT name FROM site_user WHERE cardinality(siblings) > 1;"""

if __name__=='__main__':
    task_1(command)

