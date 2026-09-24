from ingestion.utils import read_csv, insert_rows
from ingestion.db import get_connection

csv_path = r"C:\Users\27810\Desktop\projects\synthea\output\csv\patients.csv"

connection = get_connection()

print("Connected to PostgreSQL!")

patients = read_csv(csv_path)

insert_sql = """
    INSERT INTO raw.patients (
        id,
        birthdate,
        deathdate,
        ssn,
        drivers,
        passport,
        prefix,
        first_name,
        middle_name,
        last_name,
        suffix,
        maiden,
        marital,
        race,
        ethnicity,
        gender,
        birthplace,
        address,
        city,
        state,
        county,
        fips,
        zip,
        lat,
        lon,
        healthcare_expenses,
        healthcare_coverage,
        income
    )
    VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s
    )
    ON CONFLICT (id) DO NOTHING
"""

columns = [
    "Id",
    "BIRTHDATE",
    "DEATHDATE",
    "SSN",
    "DRIVERS",
    "PASSPORT",
    "PREFIX",
    "FIRST",
    "MIDDLE",
    "LAST",
    "SUFFIX",
    "MAIDEN",
    "MARITAL",
    "RACE",
    "ETHNICITY",
    "GENDER",
    "BIRTHPLACE",
    "ADDRESS",
    "CITY",
    "STATE",
    "COUNTY",
    "FIPS",
    "ZIP",
    "LAT",
    "LON",
    "HEALTHCARE_EXPENSES",
    "HEALTHCARE_COVERAGE",
    "INCOME",
]

insert_rows(connection, patients, insert_sql, columns)

connection.close()

print("Patients loaded:", len(patients))
print(patients.head())