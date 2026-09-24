from ingestion.utils import read_csv, insert_rows
from ingestion.db import get_connection

csv_path = r"C:\Users\27810\Desktop\projects\synthea\output\csv\conditions.csv"

conditions = read_csv(csv_path)

connection = get_connection()

print("Connected to PostgreSQL!")

insert_sql = """
    INSERT INTO raw.conditions (
        start_date,
        stop_date,
        patient,
        encounter,
        system,
        code,
        description
    )
    VALUES (
        %s, %s, %s, %s, %s, %s, %s
    )
    
    ON CONFLICT (patient, encounter, code) DO NOTHING
"""

columns = [
    "START",
    "STOP",
    "PATIENT",
    "ENCOUNTER",
    "SYSTEM",
    "CODE",
    "DESCRIPTION"
]

insert_rows(connection, conditions, insert_sql, columns)

print("Conditions inserted successfully!")

connection.close()

print("Conditions loaded:", len(conditions))
print(conditions.head())