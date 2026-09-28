from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import date
from db_config import get_db_connection, create_table

app = Flask(__name__)
app.secret_key = "todo_secret_key"


create_table()

@app.route("/")
def home():

    conn = get_db_connection()

    today = date.today().isoformat()

    pending_tasks = conn.execute("""
        SELECT * FROM tasks
        WHERE is_completed = 0
        AND due_date >= ?
        ORDER BY due_date
    """, (today,)).fetchall()

    
    completed_tasks = conn.execute("""
        SELECT * FROM tasks
        WHERE is_completed = 1
        AND due_date >= ?
        ORDER BY due_date
    """, (today,)).fetchall()

    conn.close()

    return render_template(
        "home.html",
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks,
        today=today
    )

@app.route("/add", methods=["POST"])
def add_task():

    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    priority = request.form.get("priority", "")
    due_date = request.form.get("due_date", "")

    today = date.today().isoformat()

    if title == "":
        flash("Task title is required!")
        return redirect(url_for("home"))

    
    if due_date == "":
        flash("Due date is required!")
        return redirect(url_for("home"))

    if due_date < today:
        flash("Past date is not allowed!")
        return redirect(url_for("home"))

    conn = get_db_connection()

    conn.execute("""
        INSERT INTO tasks
        (title, description, priority, is_completed, due_date)
        VALUES (?, ?, ?, 0, ?)
    """, (
        title,
        description,
        priority,
        due_date
    ))

    conn.commit()
    conn.close()

    flash("Task added successfully!")

    return redirect(url_for("home"))

@app.route("/toggle/<int:id>")
def toggle_task(id):

    conn = get_db_connection()

    conn.execute("""
        UPDATE tasks
        SET is_completed = 1
        WHERE id = ?
    """, (id,))

    conn.commit()
    conn.close()

    flash("Task completed successfully!")

    return redirect(url_for("home"))



@app.route("/edit/<int:id>", methods=["POST"])
def update_task(id):

    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    priority = request.form.get("priority", "")
    due_date = request.form.get("due_date", "")

    today = date.today().isoformat()

    if title == "":
        flash("Task title is required!")
        return redirect(url_for("home"))

    if due_date == "":
        flash("Due date is required!")
        return redirect(url_for("home"))

    if due_date < today:
        flash("Past date is not allowed!")
        return redirect(url_for("home"))

    conn = get_db_connection()

    conn.execute("""
        UPDATE tasks
        SET title = ?,
            description = ?,
            priority = ?,
            due_date = ?
        WHERE id = ?
    """, (
        title,
        description,
        priority,
        due_date,
        id
    ))

    conn.commit()
    conn.close()

    flash("Task updated successfully!")

    return redirect(url_for("home"))

@app.route("/delete/<int:id>", methods=["POST"])
def delete_task(id):

    conn = get_db_connection()

    conn.execute("""
        DELETE FROM tasks
        WHERE id = ?
    """, (id,))

    conn.commit()
    conn.close()

    flash("Task deleted successfully!")

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)