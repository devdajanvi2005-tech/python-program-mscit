from datetime import datetime
from pathlib import Path
from urllib.parse import quote

from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import (
    create_engine, Column, Integer, String,
    Boolean, DateTime
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session


# Create FastAPI application
app = FastAPI()

# Session configuration
app.add_middleware(
    SessionMiddleware,
    secret_key="change-this-to-a-random-secret-key"
)

# Create templates folder
Path("templates").mkdir(exist_ok=True)

templates = Jinja2Templates(directory="templates")


# SQLite database configuration
DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# Task table
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(String(300), default="")
    priority = Column(String(20), default="Medium")
    is_completed = Column(Boolean, default=False)
    created_by = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)


# Create database table automatically
Base.metadata.create_all(bind=engine)


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Check logged-in user's name
def current_user(request: Request):
    return request.session.get("username")


# Login page
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    if current_user(request):
        return RedirectResponse("/", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


# Login user
@app.post("/login")
def login(
    request: Request,
    username: str = Form(...)
):
    username = username.strip()

    if not username:
        return RedirectResponse(
            "/login", status_code=303
        )

    request.session["username"] = username

    return RedirectResponse("/", status_code=303)


# Home page: display Pending and Completed tasks
@app.get("/", response_class=HTMLResponse)
def home(
    request: Request,
    db: Session = Depends(get_db)
):
    username = current_user(request)

    if not username:
        return RedirectResponse(
            "/login", status_code=303
        )

    tasks = (
        db.query(Task)
        .filter(Task.created_by == username)
        .order_by(Task.id.desc())
        .all()
    )

    pending_tasks = [
        task for task in tasks
        if not task.is_completed
    ]

    completed_tasks = [
        task for task in tasks
        if task.is_completed
    ]

    theme = request.cookies.get("theme", "light")

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "username": username,
            "pending_tasks": pending_tasks,
            "completed_tasks": completed_tasks,
            "theme": theme
        }
    )


# Add a new task
@app.post("/add")
def add_task(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    priority: str = Form("Medium"),
    db: Session = Depends(get_db)
):
    username = current_user(request)

    if not username:
        return RedirectResponse(
            "/login", status_code=303
        )

    title = title.strip()
    description = description.strip()

    if (
        not title
        or len(title) > 150
        or len(description) > 300
        or priority not in ["High", "Medium", "Low"]
    ):
        return RedirectResponse("/", status_code=303)

    task = Task(
        title=title,
        description=description,
        priority=priority,
        is_completed=False,
        created_by=username,
        created_at=datetime.now()
    )

    db.add(task)
    db.commit()

    return RedirectResponse("/", status_code=303)


# Toggle Pending / Completed
@app.get("/toggle/{id}")
def toggle_task(
    id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    username = current_user(request)

    if not username:
        return RedirectResponse(
            "/login", status_code=303
        )

    task = (
        db.query(Task)
        .filter(
            Task.id == id,
            Task.created_by == username
        )
        .first()
    )

    if task:
        task.is_completed = not task.is_completed
        db.commit()

    return RedirectResponse("/", status_code=303)


# Display edit form
@app.get("/edit/{id}", response_class=HTMLResponse)
def edit_task(
    id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    username = current_user(request)

    if not username:
        return RedirectResponse(
            "/login", status_code=303
        )

    task = (
        db.query(Task)
        .filter(
            Task.id == id,
            Task.created_by == username
        )
        .first()
    )

    if not task:
        return RedirectResponse("/", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={"task": task, "username": username}
    )


# Update an existing task
@app.post("/update/{id}")
def update_task(
    id: int,
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    priority: str = Form("Medium"),
    db: Session = Depends(get_db)
):
    username = current_user(request)

    if not username:
        return RedirectResponse(
            "/login", status_code=303
        )

    task = (
        db.query(Task)
        .filter(
            Task.id == id,
            Task.created_by == username
        )
        .first()
    )

    if not task:
        return RedirectResponse("/", status_code=303)

    title = title.strip()
    description = description.strip()

    if (
        not title
        or len(title) > 150
        or len(description) > 300
        or priority not in ["High", "Medium", "Low"]
    ):
        return RedirectResponse(
            f"/edit/{id}", status_code=303
        )

    task.title = title
    task.description = description
    task.priority = priority

    db.commit()

    return RedirectResponse("/", status_code=303)


# Delete a task
@app.post("/delete/{id}")
def delete_task(
    id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    username = current_user(request)

    if not username:
        return RedirectResponse(
            "/login", status_code=303
        )

    task = (
        db.query(Task)
        .filter(
            Task.id == id,
            Task.created_by == username
        )
        .first()
    )

    if task:
        db.delete(task)
        db.commit()

    return RedirectResponse("/", status_code=303)


# Save selected theme in a cookie
@app.get("/set-theme/{theme}")
def set_theme(request: Request, theme: str):
    if not current_user(request):
        return RedirectResponse("/login", status_code=303)

    if theme not in ["light", "dark"]:
        return RedirectResponse("/", status_code=303)

    response = RedirectResponse("/", status_code=303)

    response.set_cookie(
        key="theme",
        value=theme,
        max_age=30 * 24 * 60 * 60,
        httponly=True,
        samesite="lax"
    )

    return response


# Logout user
@app.get("/logout")
def logout(request: Request):
    request.session.clear()

    response = RedirectResponse(
        "/login", status_code=303
    )

    response.delete_cookie("theme")

    return response