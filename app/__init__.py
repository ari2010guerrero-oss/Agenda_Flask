from flask import Flask
import sqlite3
import os


def crear_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "agenda_escolar_306"

    base_datos = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "agenda.db"
    )

    def get_db():
        conexion = sqlite3.connect(base_datos)
        conexion.row_factory = sqlite3.Row
        return conexion

    # Crear la tabla automáticamente
    conexion = get_db()
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS actividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            fecha TEXT NOT NULL,
            completada INTEGER NOT NULL DEFAULT 0
        )
    """)
    conexion.commit()
    conexion.close()

    from app.routes import registrar_rutas
    registrar_rutas(app, get_db)

    return app