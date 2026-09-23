from ingestion.db import get_connection
from ingestion.utils import read_csv

# refactor

def validate_zero_count(count, check_name):
    if count == 0:
        print(
            f"PASS: No {check_name} found."
        )
    else:
        print(
            f"FAIL: {count} {check_name} found."
        )
        
def validate_empty_list(items, check_name):
    if not items:
        print(
            f"PASS: No {check_name} found."
        )
    else:
        print(
            f"FAIL: {items}. Found {check_name}."
        )
        
def validate_row_count(expected_count, actual_count, table_name):
    if expected_count == actual_count:
        print(
            f"PASS: {table_name} row count matches"
        )
    else:
        print(
            f"FAIL: {table_name} row count does not match. "
            f"Expected {expected_count}, got {actual_count}."
        )

# csv paths

csv_path = r"C:\Users\27810\Desktop\projects\synthea\output\csv\patients.csv"
encounters_csv_path = r"C:\Users\27810\Desktop\projects\synthea\output\csv\encounters.csv"

patients = read_csv(csv_path)
expected_patient_count = len(patients)

encounters = read_csv(encounters_csv_path)
expected_encounter_count = len(encounters)

connection = get_connection()

print("Connected to PostgreSQL!")

cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM raw.patients;")

result = cursor.fetchone()

actual_patient_count = result[0]

validate_row_count(
                    expected_patient_count, 
                    actual_patient_count, 
                    "Patient"
)
    
cursor.execute("SELECT COUNT(*) FROM raw.encounters;")

result = cursor.fetchone()

actual_encounter_count = result[0]

validate_row_count(
                    expected_encounter_count,
                    actual_encounter_count,
                    "Encounter"
)
    
cursor.execute("""
    SELECT COUNT(*)
    FROM raw.patients
    WHERE id IS NULL;
""")

result = cursor.fetchone()

null_patient_id_count = result[0]

validate_zero_count(
    null_patient_id_count, 
    "NULL patient ids"
)

cursor.execute("""
               SELECT COUNT(*)
               FROM raw.encounters
               WHERE id IS NULL;
""")

result = cursor.fetchone()

null_encounter_id_count = result[0]

validate_zero_count(
    null_encounter_id_count,
    "NULL encounter ids"
)
    
cursor.execute("""
               SELECT id, COUNT(*)
               FROM raw.patients
               GROUP BY id
               HAVING count(*) > 1;
""")

duplicate_patient_ids = cursor.fetchall()

validate_empty_list(
                    duplicate_patient_ids, 
                    "duplicate patient ids"
)
    
cursor.execute("""
               SELECT id, COUNT(*)
               FROM raw.encounters
               GROUP BY id
               HAVING COUNT(*) > 1;
""")

duplicate_encounter_ids = cursor.fetchall()

validate_empty_list(
                    duplicate_encounter_ids, 
                    "duplicate encounter ids"
)
    
cursor.execute("""
               SELECT COUNT(*)
               FROM raw.encounters e
               LEFT JOIN raw.patients p
                    ON e.patient = p.id
               WHERE p.id is NULL;
""")

result = cursor.fetchone()

orphaned_encounter_count = result[0]

validate_zero_count(
    orphaned_encounter_count,
    "orphaned encounters"
)
    
cursor.execute("""
               SELECT COUNT(*)
               FROM raw.encounters
               WHERE stop_time < start_time;
""")

result = cursor.fetchone()

invalid_date_count = result[0]

validate_zero_count(
    invalid_date_count,
    "invalid dates"
)

cursor.close()
connection.close()

# Testing examples — intentionally disabled
#
# validate_zero_count(
#     3,
#     "TEST invalid records"
# )
#
# validate_empty_list(
#     [("TEST_ID", 2)],
#     "TEST duplicate ids"
# )
#
# validate_row_count(
#     100,
#     99,
#     "TEST"
# )