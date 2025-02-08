import sqlite3

# Initialize the database
def initialize_database():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # Create the products table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL,
            quantity INTEGER
        )
    ''')

    conn.commit()
    conn.close()

# Call the initialize_database function on application startup
initialize_database()