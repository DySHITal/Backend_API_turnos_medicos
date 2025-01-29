
def cargar_datos(test_db):
    with open("datos_test.sql", encoding="utf-8") as f:
        sql_script = f.read()
    with test_db.get_connection() as conn:
        cursor = conn.cursor()
        sql_statements = sql_script.split(";")
        for statement in sql_statements:
            if statement.strip():
                cursor.execute(statement)
        conn.commit()

def eliminar_datos(test_db):
    with test_db.get_connection() as conn:
        if not conn.is_connected():
            conn.ping(reconnect=True)
        cursor = conn.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE paciente;")
        cursor.execute("ALTER TABLE paciente AUTO_INCREMENT = 1;")
        cursor.execute("TRUNCATE TABLE profesional;")
        cursor.execute("ALTER TABLE profesional AUTO_INCREMENT = 1;")
        cursor.execute("TRUNCATE TABLE cancelacion;")
        cursor.execute("ALTER TABLE cancelacion AUTO_INCREMENT = 1;")
        cursor.execute("TRUNCATE TABLE turno;")
        cursor.execute("ALTER TABLE turno AUTO_INCREMENT = 1;")
        cursor.execute("TRUNCATE TABLE disponibilidad;")
        cursor.execute("ALTER TABLE disponibilidad AUTO_INCREMENT = 1;")
        cursor.execute("TRUNCATE TABLE obra_social;")
        cursor.execute("ALTER TABLE obra_social AUTO_INCREMENT = 1;")
        cursor.execute("TRUNCATE TABLE profesional_obrasocial;")
        cursor.execute("ALTER TABLE profesional_obrasocial AUTO_INCREMENT = 1;")
        cursor.execute("TRUNCATE TABLE realizado_por;")
        cursor.execute("ALTER TABLE realizado_por AUTO_INCREMENT = 1;")
        conn.commit()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")  
        conn.commit()