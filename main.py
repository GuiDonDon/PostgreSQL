import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(40) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE
            );
            """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phones (
                id SERIAL PRIMARY KEY,
                client_id INTEGER REFERENCES client(id),
                phone VARCHAR(12) UNIQUE
            );
            """)
    pass

def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        data = (first_name, last_name, email)
        cur.execute("""
            INSERT INTO client(first_name, last_name, email) VALUES (%s, %s, %s);
            """, data)
    pass

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        data = (client_id, phone)
        cur.execute("""
            INSERT INTO phones(client_id, phone) VALUES (%s, %s);
            """, data)
    pass

def change_client(conn, client_id, first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:
        if first_name is not None:
            cur.execute("""
                UPDATE client SET first_name=%s WHERE id=%s;
                """, (first_name, client_id))
        if last_name is not None:
            cur.execute("""
                UPDATE client SET last_name=%s WHERE id=%s;
                """, (last_name, client_id))
        if email is not None:
            cur.execute("""
                UPDATE client SET email=%s WHERE id=%s;
                """, (email, client_id))
    pass

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        data = (client_id, phone)
        cur.execute("""
            DELETE FROM phones WHERE client_id=%s AND phone=%s;
        """, (data))
    pass

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phones WHERE client_id=%s;
        """, (client_id,))
        cur.execute("""
            DELETE FROM client WHERE id=%s;
        """, (client_id,))
    pass

def find_client(conn, first_name='%', last_name='%', email='%', phone='%'):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT first_name, last_name, email, phone FROM client AS c LEFT JOIN phones AS p on c.id = p.client_id 
                WHERE c.first_name LIKE %s AND c.last_name LIKE %s AND c.email LIKE %s AND p.phone LIKE %s;
            """, (first_name, last_name, email, phone,))
        data = cur.fetchall()
        if data != []:
            print(data)
        else:
            print('Ничего не найдено')    
    pass


if __name__ == "__main__":
    with psycopg2.connect(database="", user="", password="") as conn:
    create_db(conn)
    add_client(conn, 'Ivan', 'Ivanov', 'ivan@mail.ru')
    add_phone(conn, 1, '+79000000001')
    add_phone(conn, 1, '+79000000002')
    change_client(conn, 1)
    delete_phone(conn, 1, '+79000000002')
    delete_client(conn, 1)
    find_client(conn)    
    pass  

conn.close()