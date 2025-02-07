def get_connection():
    return psycopg.connect(**DB_CONFIG):
