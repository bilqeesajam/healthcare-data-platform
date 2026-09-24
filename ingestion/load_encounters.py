from ingestion.utils import read_csv, insert_rows
from ingestion.db import get_connection

csv_path = r"C:\Users\27810\Desktop\projects\synthea\output\csv\encounters.csv"

encounters = read_csv(csv_path)

connection = get_connection()

print("Connected to PostgreSQL!")

insert_sql = """
    INSERT INTO raw.encounters (
        id,
        start_time,
        stop_time,
        patient,
        organization,
        provider,
        payer,
        encounterclass,
        code,
        description,
        base_encounter_cost,
        total_claim_cost,
        payer_coverage,
        reasoncode,
        reasondescription
    )
    VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s
    )
    ON CONFLICT (id) DO NOTHING
""" 

columns = [
    "Id",
    "START",
    "STOP",
    "PATIENT",
    "ORGANIZATION",
    "PROVIDER",
    "PAYER",
    "ENCOUNTERCLASS",
    "CODE",
    "DESCRIPTION",
    "BASE_ENCOUNTER_COST",
    "TOTAL_CLAIM_COST",
    "PAYER_COVERAGE",
    "REASONCODE",
    "REASONDESCRIPTION",
]

insert_rows(connection, encounters, insert_sql, columns)

print("Encounters inserted successfully!")

connection.close()

print("Encounters loaded:", len(encounters))
print(encounters.head())