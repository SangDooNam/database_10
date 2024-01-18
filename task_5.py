import psycopg2
import os
import dotenv

dotenv.load_dotenv()

def task_5(command_find, command):
    
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
        cursor.execute(command_find)
        
        id = cursor.fetchone()
        
        cursor.execute(command, id)
        
        conn.commit()
        cursor.close()
    
    except(Exception, psycopg2.DatabaseError) as error: 
        raise error
    
    finally:
        if conn is not None:
            conn.close()


command_find = """SELECT id FROM site_user WHERE role < 'Moderator';"""

command = """UPDATE site_user SET role = 'Moderator' WHERE id = %s;
            """

if __name__=='__main__':
    task_5(command_find, command)

