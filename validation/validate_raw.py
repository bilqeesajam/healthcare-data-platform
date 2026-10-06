from ingestion.db import get_connection
from ingestion.utils import read_csv

# Validation helper functions

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

# Source data

csv_path = r"C:\Users\27810\Desktop\projects\synthea\output\csv\patients.csv"
encounters_csv_path = r"C:\Users\27810\Desktop\projects\synthea\output\csv\encounters.csv"
conditions_csv_path = r"C:\Users\27810\Desktop\projects\synthea\output\csv\conditions.csv"

patients = read_csv(csv_path)
expected_patient_count = len(patients)

encounters = read_csv(encounters_csv_path)
expected_encounter_count = len(encounters)

conditions = read_csv(conditions_csv_path)
expected_condition_count = len(conditions)

# Database connection

connection = get_connection()

print("Connected to PostgreSQL!")

cursor = connection.cursor()

# --- Row count validation ---

# Patients

cursor.execute("SELECT COUNT(*) FROM raw.patients;")

result = cursor.fetchone()

actual_patient_count = result[0]

validate_row_count(
    expected_patient_count,
    actual_patient_count,
    "Patient"
)


# Encounters

cursor.execute("SELECT COUNT(*) FROM raw.encounters;")

result = cursor.fetchone()

actual_encounter_count = result[0]

validate_row_count(
    expected_encounter_count,
    actual_encounter_count,
    "Encounter"
)

# Conditions

cursor.execute("SELECT COUNT(*) FROM raw.conditions;")

result = cursor.fetchone()

actual_condition_count = result[0]

validate_row_count(
    expected_condition_count,
    actual_condition_count,
    "Condition"
)

# --- NULL validation ---

# Patients

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


# Encounters

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
# Conditions

cursor.execute("""
    SELECT COUNT(*)
    FROM raw.conditions
    WHERE patient IS NULL
        OR encounter IS NULL;
 """)

result = cursor.fetchone()

null_condition_reference_count = result [0]

validate_zero_count(
    null_condition_reference_count,
    "conditions with NULL patient or encounter references"
)

# --- Duplicate validation ---

# Patients

cursor.execute("""
    SELECT id, COUNT(*)
    FROM raw.patients
    GROUP BY id
    HAVING COUNT(*) > 1;
""")

duplicate_patient_ids = cursor.fetchall()

validate_empty_list(
    duplicate_patient_ids,
    "duplicate patient ids"
)


# Encounters

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

# Conditions

cursor.execute("""
    SELECT patient, encounter, code, COUNT(*)
    FROM raw.conditions
    GROUP BY patient, encounter, code
    HAVING COUNT(*) > 1;
""")

duplicate_conditions = cursor.fetchall()

validate_empty_list(
    duplicate_conditions,
    "duplicate conditions"
)

# --- Referential integrity validation ---

# Encounters -> Patients

cursor.execute("""
    SELECT COUNT(*)
    FROM raw.encounters e
    LEFT JOIN raw.patients p
        ON e.patient = p.id
    WHERE p.id IS NULL;
""")

result = cursor.fetchone()

orphaned_encounter_count = result[0]

validate_zero_count(
    orphaned_encounter_count,
    "orphaned encounters"
)

# conditions -> patient

cursor.execute("""
    SELECT COUNT(*)
    FROM raw.conditions c
    LEFT JOIN raw.patients p
        ON c.patient = p.id
    WHERE p.id IS NULL;
""")

result = cursor.fetchone()

orphaned_condition_patient_count = result[0]

validate_zero_count(
    orphaned_condition_patient_count,
    "conditions with orphaned patient references"
)

# conditions -> encounters
cursor.execute("""
    SELECT COUNT(*)
    FROM raw.conditions c
    LEFT JOIN raw.encounters e
        ON  c.encounter = e.id
    WHERE e.id IS NULL;
""")

result = cursor.fetchone()

orphaned_condition_encounter_count = result[0]

validate_zero_count(
    orphaned_condition_encounter_count,
    "conditions with orphaned encounter references"
)

# --- Date validation ---

# Encounters

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

# Conditions

cursor.execute("""
               SELECT  COUNT(*)
               FROM raw.conditions
               WHERE stop_date < start_date;
""")

result = cursor.fetchone()

invalid_condition_date_count = result[0]

validate_zero_count(
    invalid_condition_date_count,
    "conditions with invalid dates"
)

# Cleanup

cursor.close()
connection.close()

# Testing examples — intentionally disabled

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