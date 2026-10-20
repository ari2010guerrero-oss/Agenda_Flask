from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)


def registrar_rutas(app, get_db):

    @app.route("/")
    def inicio():
        conexion = get_db()
        actividades = conexion.execute("""
            SELECT * FROM actividades
            ORDER BY fecha ASC, id DESC
        """).fetchall()
        conexion.close()

        return render_template(
            "index.html",
            actividades=actividades
        )

    @app.route("/agregar", methods=["POST"])
    def agregar():
        titulo = request.form.get("titulo", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        fecha = request.form.get("fecha", "").strip()

        if not titulo or not fecha:
            flash("Escribe un título y selecciona una fecha.", "error")
            return redirect(url_for("inicio"))

        conexion = get_db()
        conexion.execute("""
            INSERT INTO actividades (titulo, descripcion, fecha)
            VALUES (?, ?, ?)
        """, (titulo, descripcion, fecha))
        conexion.commit()
        conexion.close()

        flash("¡Actividad agregada correctamente!", "success")
        return redirect(url_for("inicio"))

    @app.route("/editar/<int:id>", methods=["GET", "POST"])
    def editar(id):
        conexion = get_db()

        actividad = conexion.execute(
            "SELECT * FROM actividades WHERE id = ?", (id,)
        ).fetchone()

        if actividad is None:
            conexion.close()
            flash("La actividad no existe.", "error")
            return redirect(url_for("inicio"))

        if request.method == "POST":
            titulo = request.form.get("titulo", "").strip()
            descripcion = request.form.get("descripcion", "").strip()
            fecha = request.form.get("fecha", "").strip()

            if not titulo or not fecha:
                conexion.close()
                flash("El título y la fecha son obligatorios.", "error")
                return redirect(url_for("editar", id=id))

            conexion.execute("""
                UPDATE actividades
                SET titulo = ?, descripcion = ?, fecha = ?
                WHERE id = ?
            """, (titulo, descripcion, fecha, id))

            conexion.commit()
            conexion.close()

            flash("¡Actividad actualizada!", "success")
            return redirect(url_for("inicio"))

        conexion.close()
        return render_template("editar.html", actividad=actividad)

    @app.route("/completar/<int:id>", methods=["POST"])
    def completar(id):
        conexion = get_db()

        conexion.execute("""
            UPDATE actividades
            SET completada = CASE
                WHEN completada = 0 THEN 1
                ELSE 0
            END
            WHERE id = ?
        """, (id,))

        conexion.commit()
        conexion.close()

        flash("Estado de la actividad actualizado.", "success")
        return redirect(url_for("inicio"))

    @app.route("/eliminar/<int:id>", methods=["POST"])
    def eliminar(id):
        conexion = get_db()

        conexion.execute(
            "DELETE FROM actividades WHERE id = ?", (id,)
        )

        conexion.commit()
        conexion.close()

        flash("Actividad eliminada.", "success")
        return redirect(url_for("inicio"))