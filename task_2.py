import psycopg2
import os
import dotenv

dotenv.load_dotenv()

def task_2(command, array, id):
    
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
        
        cursor.execute(command, (array, id))
        
        conn.commit()
        cursor.close()
    
    except(Exception, psycopg2.DatabaseError) as error: 
        raise error
    finally:
        if conn is not None:
            conn.close()

command = """UPDATE site_user SET siblings = %s WHERE id = %s; """

if __name__=='__main__':
    task_2(command, ['Monique', 'Jordi'], '3')