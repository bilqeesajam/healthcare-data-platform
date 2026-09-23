import pandas as pd

def read_csv(csv_path):
    data = pd.read_csv(csv_path)
    data = data.astype(object).where(pd.notna(data), None)

    return data

def insert_rows(connection, data, insert_sql, columns):
    cursor = connection.cursor()

    for _, row in data.iterrows():
        values = tuple(row[column] for column in columns)
        cursor.execute(insert_sql, values)

    connection.commit()
    cursor.close()