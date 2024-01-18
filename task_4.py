import psycopg2
import os
import dotenv

dotenv.load_dotenv()

def task_4(command):
    
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
        
        conn.commit()
        cursor.close()
    
    except(Exception, psycopg2.DatabaseError) as error: 
        raise error
    
    finally:
        if conn is not None:
            conn.close()


command = """UPDATE site_user SET site_settings = jsonb_set(site_settings::jsonb, '{notifications}', 'false')::json
            WHERE id = 3;
            """

if __name__=='__main__':
    task_4(command)

