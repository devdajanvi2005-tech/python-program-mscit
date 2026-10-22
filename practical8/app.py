from flask import Flask, render_template, request
from datetime import date
from database import db, Task

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():

    pending_tasks = Task.query.filter_by(status="Pending").all()

    in_progress_tasks = Task.query.filter_by(status="In Progress").all()

    completed_tasks = Task.query.filter_by(status="Completed").all()

    return render_template(
        "home.html",
        pending_tasks=pending_tasks,
        in_progress_tasks=in_progress_tasks,
        completed_tasks=completed_tasks,
        edit_task=None,
        message=None,
        today=date.today().isoformat()
    )


@app.route("/add", methods=["POST"])
def add_task():

    title = request.form["title"]
    description = request.form["description"]
    priority = request.form["priority"]
    status = request.form["status"]
    due_date = request.form["due_date"]

    if due_date < date.today().isoformat():

        return render_template(
            "home.html",
            pending_tasks=Task.query.filter_by(status="Pending").all(),
            in_progress_tasks=Task.query.filter_by(status="In Progress").all(),
            completed_tasks=Task.query.filter_by(status="Completed").all(),
            edit_task=None,
            message="Past date is not allowed!",
            today=date.today().isoformat()
        )

    if status == "Completed":

        return render_template(
            "home.html",
            pending_tasks=Task.query.filter_by(status="Pending").all(),
            in_progress_tasks=Task.query.filter_by(status="In Progress").all(),
            completed_tasks=Task.query.filter_by(status="Completed").all(),
            edit_task=None,
            message="Completed task cannot be added!",
            today=date.today().isoformat()
        )

    task = Task(
        title=title,
        description=description,
        priority=priority,
        status=status,
        due_date=date.fromisoformat(due_date)
    )

    db.session.add(task)
    db.session.commit()

    return render_template(
        "home.html",
        pending_tasks=Task.query.filter_by(status="Pending").all(),
        in_progress_tasks=Task.query.filter_by(status="In Progress").all(),
        completed_tasks=Task.query.filter_by(status="Completed").all(),
        edit_task=None,
        message="Task created successfully!",
        today=date.today().isoformat()
    )


@app.route("/edit/<int:id>")
def edit_task(id):

    task = Task.query.get_or_404(id)

    return render_template(
        "home.html",
        pending_tasks=Task.query.filter_by(status="Pending").all(),
        in_progress_tasks=Task.query.filter_by(status="In Progress").all(),
        completed_tasks=Task.query.filter_by(status="Completed").all(),
        edit_task=task,
        message=None,
        today=date.today().isoformat()
    )


@app.route("/update/<int:id>", methods=["POST"])
def update_task(id):

    task = Task.query.get_or_404(id)

    title = request.form["title"]
    description = request.form["description"]
    priority = request.form["priority"]
    status = request.form["status"]
    due_date = request.form["due_date"]

    if due_date < date.today().isoformat():

        return render_template(
            "home.html",
            pending_tasks=Task.query.filter_by(status="Pending").all(),
            in_progress_tasks=Task.query.filter_by(status="In Progress").all(),
            completed_tasks=Task.query.filter_by(status="Completed").all(),
            edit_task=task,
            message="Past date is not allowed!",
            today=date.today().isoformat()
        )

    task.title = title
    task.description = description
    task.priority = priority
    task.status = status
    task.due_date = date.fromisoformat(due_date)

    db.session.commit()

    return render_template(
        "home.html",
        pending_tasks=Task.query.filter_by(status="Pending").all(),
        in_progress_tasks=Task.query.filter_by(status="In Progress").all(),
        completed_tasks=Task.query.filter_by(status="Completed").all(),
        edit_task=None,
        message="Task updated successfully!",
        today=date.today().isoformat()
    )


@app.route("/delete/<int:id>")
def delete_task(id):

    task = Task.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    return render_template(
        "home.html",
        pending_tasks=Task.query.filter_by(status="Pending").all(),
        in_progress_tasks=Task.query.filter_by(status="In Progress").all(),
        completed_tasks=Task.query.filter_by(status="Completed").all(),
        edit_task=None,
        message="Task deleted successfully!",
        today=date.today().isoformat()
    )


if __name__ == "__main__":
    app.run(debug=True)