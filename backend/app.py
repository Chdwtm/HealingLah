from flask import Flask, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Konfigurasi database SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inisialisasi SQLAlchemy
db = SQLAlchemy(app)

# Model User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Model Project
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Model Task
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default="Pending")
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

# Endpoint untuk membuat tabel database
@app.route('/init-db', methods=['GET'])
def init_db():
    with app.app_context():
        db.create_all()  # Buat tabel
    return jsonify({"message": "Database and tables created successfully!"})

# Endpoint untuk register user
@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    # Hash password and save user
    hashed_password = generate_password_hash(password, method="sha256")
    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 200

# Endpoint untuk login user
@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({"message": "Login successful"}), 200

# Endpoint untuk mendapatkan semua proyek
@app.route("/api/projects", methods=["GET"])
def get_projects():
    projects = Project.query.all()
    return jsonify([{
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "created_by": project.created_by
    } for project in projects])

# Endpoint untuk menambah proyek baru
@app.route("/api/projects", methods=["POST"])
def add_project():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    created_by = data.get("created_by")

    if not name or not created_by:
        return jsonify({"message": "Name and created_by are required"}), 400

    new_project = Project(name=name, description=description, created_by=created_by)
    db.session.add(new_project)
    db.session.commit()

    return jsonify({"message": "Project added successfully"}), 200

# Endpoint untuk menambah tugas ke dalam proyek
@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.json
    title = data.get("title")
    description = data.get("description")
    status = data.get("status")
    project_id = data.get("project_id")

    if not title or not project_id:
        return jsonify({"message": "Title and project_id are required"}), 400

    new_task = Task(title=title, description=description, status=status, project_id=project_id)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"message": "Task added successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
