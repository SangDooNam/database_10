import psycopg2
import os
import dotenv

dotenv.load_dotenv()

def task_3(command, array, id):
    
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

command = """UPDATE site_user SET availability = ROW(%s::JSONB[]) WHERE id = %s; """
insert_data = ['{"start_time":"09:00:00"}', '{"end_time": "10:00:00"}']


if __name__=='__main__':
    task_3(command, insert_data, '3')