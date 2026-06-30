from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import os, sys, secrets, datetime

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "data")
FRONTEND_DIR = os.path.normpath(os.path.join(BASE, "..", "frontend"))
PAGES_DIR = os.path.join(FRONTEND_DIR, "pages")
ASSETS_DIR = os.path.join(FRONTEND_DIR, "assets")
CSS_DIR = os.path.join(FRONTEND_DIR, "css")
JS_DIR = os.path.join(FRONTEND_DIR, "js")

sys.path.insert(0, BASE)

app = Flask(__name__)
CORS(app)

# ── Database ──────────────────────────────────────────────────────────────────
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///counsellor_ai.db"
app.config["SQLALCHEMY_TRAC" \
"K_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# ── Models ────────────────────────────────────────────────────────────────────
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    current_address = db.Column(db.String(255))
    permanent_address = db.Column(db.String(255))
    hobbies = db.Column(db.String(255))
    clubs = db.Column(db.String(255))
    volunteer_work = db.Column(db.String(255))
    languages_known = db.Column(db.String(255))
    platforms = db.Column(db.String(255))
    specializations = db.Column(db.String(255))
    certifications = db.Column(db.String(255))
    career_goals = db.Column(db.String(255))
    preferred_industries = db.Column(db.String(255))
    internships = db.Column(db.String(255))


class Accommodation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50))
    city = db.Column(db.String(100))
    area = db.Column(db.String(100))
    rent = db.Column(db.Integer)
    contact = db.Column(db.String(50))
    amenities = db.Column(db.String(255))
    gender = db.Column(db.String(20))
    description = db.Column(db.Text)


class MessTiffin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50))
    city = db.Column(db.String(100))
    area = db.Column(db.String(100))
    monthly_cost = db.Column(db.Integer)
    contact = db.Column(db.String(50))
    cuisine = db.Column(db.String(100))
    timing = db.Column(db.String(100))
    description = db.Column(db.Text)


class Scholarship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    provider = db.Column(db.String(200))
    amount = db.Column(db.String(100))
    eligibility = db.Column(db.Text)
    deadline = db.Column(db.String(50))
    category = db.Column(db.String(100))
    apply_link = db.Column(db.String(500))
    description = db.Column(db.Text)


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    exam = db.Column(db.String(100))
    subject = db.Column(db.String(100))
    resource_type = db.Column(db.String(50))
    year = db.Column(db.String(10))
    description = db.Column(db.Text)
    file_url = db.Column(db.String(500))
    is_free = db.Column(db.Boolean, default=True)
    downloads = db.Column(db.Integer, default=0)
    tags = db.Column(db.String(300))


# ── Auth Models ───────────────────────────────────────────────────────────────
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default="student")  # student / admin
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "username": self.username,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class AuthToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    token = db.Column(db.String(64), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    user = db.relationship("User", backref="tokens")


# ── Load CSV data ─────────────────────────────────────────────────────────────
def load_csv(filename):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()


mhtcet_data = load_csv("college_cutoffs.csv")
pharmacy_data = load_csv("pharmacy_colleges_cutoffs.csv")
bitsat_data = load_csv("BITSAT_Cutoffs.csv")
jee_data = load_csv("iit-and-nit-colleges-admission-criteria-version-2.csv")


# ── Static file serving ───────────────────────────────────────────────────────
@app.route("/")
def home():
    return send_from_directory(PAGES_DIR, "index.html")


@app.route("/pages/<path:filename>")
def serve_page(filename):
    return send_from_directory(PAGES_DIR, filename)


@app.route("/assets/<path:filename>")
def serve_asset(filename):
    return send_from_directory(ASSETS_DIR, filename)


@app.route("/css/<path:filename>")
def serve_css(filename):
    return send_from_directory(CSS_DIR, filename)


@app.route("/js/<path:filename>")
def serve_js(filename):
    return send_from_directory(JS_DIR, filename)


# ── Predictor imports ─────────────────────────────────────────────────────────
from predict import generate_preferred_college_list as mhtcet_predict
from pharmacy import generate_preferred_college_list as pharmacy_predict
from bits import predict_colleges as bitsat_predict


# ══════════════════════════════════════════════════════════════════════════════
#  COLLEGE PREDICTOR APIs
# ══════════════════════════════════════════════════════════════════════════════
@app.route("/api/predict/mhtcet", methods=["POST"])
def api_mhtcet():
    d = request.get_json() or {}
    percentile = float(d.get("percentile", 0))
    category = d.get("category", "OPEN")
    branch = d.get("branch") or None
    cities = [c.strip() for c in d.get("preferred_cities", "").split(",") if c.strip()]
    return jsonify(mhtcet_predict(percentile, category, branch, mhtcet_data, cities))


@app.route("/api/predict/pharmacy", methods=["POST"])
def api_pharmacy():
    d = request.get_json() or {}
    percentile = float(d.get("percentile", 0))
    category = d.get("category", "OPEN")
    branch = d.get("branch") or None
    cities = [c.strip() for c in d.get("preferred_cities", "").split(",") if c.strip()]
    results = pharmacy_predict(percentile, category, branch, pharmacy_data, cities)
    # pharmacy.py now returns list of dicts — extract display string for frontend
    return jsonify([r["display"] if isinstance(r, dict) else r for r in results])


@app.route("/api/predict/bitsat", methods=["POST"])
def api_bitsat():
    d = request.get_json() or {}
    score = int(d.get("score", 0))
    campus = d.get("campus", "")
    return jsonify(bitsat_predict(score, campus, bitsat_data))


@app.route("/api/predict/jee", methods=["POST"])
def api_jee():
    d = request.get_json() or {}
    rank = int(d.get("rank", 0))
    category = d.get("category", "OPEN")
    gender = d.get("gender", "Gender-Neutral")
    branch = d.get("branch", "").strip().lower()
    cities = [c.strip() for c in d.get("preferred_cities", "").split(",") if c.strip()]

    if jee_data.empty:
        return jsonify([])

    df = jee_data.copy()

    # ── Map incoming category to CSV values ──────────────────────────────────
    # CSV uses: GEN, OBC-NCL, SC, ST, GEN-EWS, GEN-PWD
    cat_map = {
        "OPEN": "GEN",
        "GEN": "GEN",
        "GEN-EWS": "GEN-EWS",
        "OBC-NCL": "OBC-NCL",
        "SC": "SC",
        "ST": "ST",
        "GEN-PWD": "GEN-PWD",
    }
    csv_category = cat_map.get(category, "GEN")

    # ── Use latest available year ─────────────────────────────────────────────
    if "year" in df.columns:
        latest_year = df["year"].max()
        df = df[df["year"] == latest_year]

    # ── Filter by category ────────────────────────────────────────────────────
    if "category" in df.columns:
        df = df[df["category"] == csv_category]

    # ── Filter by gender/pool ─────────────────────────────────────────────────
    if gender and "pool" in df.columns:
        df = df[df["pool"] == gender]

    # ── Filter by rank range ──────────────────────────────────────────────────
    if "closing_rank" in df.columns:
        df = df[pd.to_numeric(df["closing_rank"], errors="coerce") >= rank]
    if "opening_rank" in df.columns:
        df = df[pd.to_numeric(df["opening_rank"], errors="coerce") <= rank * 2]

    # ── Filter by branch keyword ──────────────────────────────────────────────
    if branch and "program_name" in df.columns:
        df = df[df["program_name"].str.lower().str.contains(branch, na=False)]

    # ── Filter by institute type (cities field repurposed as institute type) ──
    if cities and "institute_type" in df.columns:
        df = df[df["institute_type"].isin(cities)]

    # ── Rename columns for frontend ───────────────────────────────────────────
    df = df.rename(
        columns={
            "institute_short": "Institute",
            "program_name": "Academic Program Name",
            "category": "Seat Type",
            "pool": "Gender",
            "opening_rank": "Opening Rank",
            "closing_rank": "Closing Rank",
            "institute_type": "Institute Type",
        }
    )

    return jsonify(df.head(50).to_dict(orient="records"))


# ══════════════════════════════════════════════════════════════════════════════
#  ACCOMMODATION APIs
# ══════════════════════════════════════════════════════════════════════════════
@app.route("/api/accommodation", methods=["GET"])
def get_accommodation():
    city = request.args.get("city", "")
    atype = request.args.get("type", "")
    gender = request.args.get("gender", "")
    max_rent = request.args.get("max_rent", type=int)
    q = Accommodation.query
    if city:
        q = q.filter(Accommodation.city.ilike(f"%{city}%"))
    if atype:
        q = q.filter(Accommodation.type.ilike(f"%{atype}%"))
    if gender:
        q = q.filter(Accommodation.gender.ilike(f"%{gender}%"))
    if max_rent:
        q = q.filter(Accommodation.rent <= max_rent)
    return jsonify(
        [
            {
                "id": r.id,
                "title": r.title,
                "type": r.type,
                "city": r.city,
                "area": r.area,
                "rent": r.rent,
                "contact": r.contact,
                "amenities": r.amenities,
                "gender": r.gender,
                "description": r.description,
            }
            for r in q.all()
        ]
    )


@app.route("/api/accommodation", methods=["POST"])
def add_accommodation():
    d = request.get_json() or {}
    rec = Accommodation(
        title=d.get("title", ""),
        type=d.get("type", ""),
        city=d.get("city", ""),
        area=d.get("area", ""),
        rent=d.get("rent", 0),
        contact=d.get("contact", ""),
        amenities=d.get("amenities", ""),
        gender=d.get("gender", ""),
        description=d.get("description", ""),
    )
    db.session.add(rec)
    db.session.commit()
    return jsonify({"id": rec.id, "message": "Added successfully"}), 201


# ══════════════════════════════════════════════════════════════════════════════
#  MESS & TIFFIN APIs
# ══════════════════════════════════════════════════════════════════════════════
@app.route("/api/mess", methods=["GET"])
def get_mess():
    city = request.args.get("city", "")
    mtype = request.args.get("type", "")
    max_cost = request.args.get("max_cost", type=int)
    q = MessTiffin.query
    if city:
        q = q.filter(MessTiffin.city.ilike(f"%{city}%"))
    if mtype:
        q = q.filter(MessTiffin.type.ilike(f"%{mtype}%"))
    if max_cost:
        q = q.filter(MessTiffin.monthly_cost <= max_cost)
    return jsonify(
        [
            {
                "id": r.id,
                "name": r.name,
                "type": r.type,
                "city": r.city,
                "area": r.area,
                "monthly_cost": r.monthly_cost,
                "contact": r.contact,
                "cuisine": r.cuisine,
                "timing": r.timing,
                "description": r.description,
            }
            for r in q.all()
        ]
    )


@app.route("/api/mess", methods=["POST"])
def add_mess():
    d = request.get_json() or {}
    rec = MessTiffin(
        name=d.get("name", ""),
        type=d.get("type", ""),
        city=d.get("city", ""),
        area=d.get("area", ""),
        monthly_cost=d.get("monthly_cost", 0),
        contact=d.get("contact", ""),
        cuisine=d.get("cuisine", ""),
        timing=d.get("timing", ""),
        description=d.get("description", ""),
    )
    db.session.add(rec)
    db.session.commit()
    return jsonify({"id": rec.id, "message": "Added successfully"}), 201


# ══════════════════════════════════════════════════════════════════════════════
#  SCHOLARSHIP APIs
# ══════════════════════════════════════════════════════════════════════════════
@app.route("/api/scholarships", methods=["GET"])
def get_scholarships():
    category = request.args.get("category", "")
    search = request.args.get("search", "")
    q = Scholarship.query
    if category:
        q = q.filter(Scholarship.category.ilike(f"%{category}%"))
    if search:
        q = q.filter(
            db.or_(
                Scholarship.name.ilike(f"%{search}%"),
                Scholarship.provider.ilike(f"%{search}%"),
                Scholarship.description.ilike(f"%{search}%"),
            )
        )
    return jsonify(
        [
            {
                "id": r.id,
                "name": r.name,
                "provider": r.provider,
                "amount": r.amount,
                "eligibility": r.eligibility,
                "deadline": r.deadline,
                "category": r.category,
                "apply_link": r.apply_link,
                "description": r.description,
            }
            for r in q.all()
        ]
    )


@app.route("/api/scholarships", methods=["POST"])
def add_scholarship():
    d = request.get_json() or {}
    rec = Scholarship(
        name=d.get("name", ""),
        provider=d.get("provider", ""),
        amount=d.get("amount", ""),
        eligibility=d.get("eligibility", ""),
        deadline=d.get("deadline", ""),
        category=d.get("category", ""),
        apply_link=d.get("apply_link", ""),
        description=d.get("description", ""),
    )
    db.session.add(rec)
    db.session.commit()
    return jsonify({"id": rec.id, "message": "Scholarship added"}), 201


# ══════════════════════════════════════════════════════════════════════════════
#  RESOURCES APIs
# ══════════════════════════════════════════════════════════════════════════════
@app.route("/api/resources", methods=["GET"])
def get_resources():
    exam = request.args.get("exam", "")
    subject = request.args.get("subject", "")
    rtype = request.args.get("type", "")
    search = request.args.get("search", "")
    year = request.args.get("year", "")
    q = Resource.query
    if exam:
        q = q.filter(Resource.exam.ilike(f"%{exam}%"))
    if subject:
        q = q.filter(Resource.subject.ilike(f"%{subject}%"))
    if rtype:
        q = q.filter(Resource.resource_type.ilike(f"%{rtype}%"))
    if year:
        q = q.filter(Resource.year == year)
    if search:
        q = q.filter(
            db.or_(
                Resource.title.ilike(f"%{search}%"),
                Resource.description.ilike(f"%{search}%"),
                Resource.tags.ilike(f"%{search}%"),
            )
        )
    return jsonify(
        [
            {
                "id": r.id,
                "title": r.title,
                "exam": r.exam,
                "subject": r.subject,
                "resource_type": r.resource_type,
                "year": r.year,
                "description": r.description,
                "file_url": r.file_url,
                "is_free": r.is_free,
                "downloads": r.downloads,
                "tags": r.tags,
            }
            for r in q.order_by(Resource.downloads.desc()).all()
        ]
    )


@app.route("/api/resources/<int:rid>/download", methods=["POST"])
def increment_download(rid):
    r = Resource.query.get_or_404(rid)
    r.downloads += 1
    db.session.commit()
    return jsonify({"downloads": r.downloads})


# ══════════════════════════════════════════════════════════════════════════════
#  AUTH HELPER
# ══════════════════════════════════════════════════════════════════════════════
def get_current_user():
    """Extract user from Bearer token in Authorization header."""
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    token_str = auth[7:]
    token = AuthToken.query.filter_by(token=token_str).first()
    if not token:
        return None
    if token.expires_at < datetime.datetime.utcnow():
        db.session.delete(token)
        db.session.commit()
        return None
    return token.user


# ══════════════════════════════════════════════════════════════════════════════
#  AUTH APIs
# ══════════════════════════════════════════════════════════════════════════════
@app.route("/api/auth/register", methods=["POST"])
def register():
    d = request.get_json() or {}
    full_name = d.get("full_name", "").strip()
    email = d.get("email", "").strip().lower()
    username = d.get("username", "").strip().lower()
    password = d.get("password", "")

    # Validation
    if not all([full_name, email, username, password]):
        return jsonify({"error": "All fields are required."}), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters."}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "An account with this email already exists."}), 409
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "This username is already taken."}), 409

    user = User(full_name=full_name, email=email, username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # Auto-login after register
    token = _create_token(user)
    return (
        jsonify(
            {
                "message": "Account created successfully!",
                "token": token,
                "user": user.to_dict(),
            }
        ),
        201,
    )


@app.route("/api/auth/login", methods=["POST"])
def login():
    d = request.get_json() or {}
    identifier = d.get("identifier", "").strip().lower()  # email or username
    password = d.get("password", "")

    if not identifier or not password:
        return jsonify({"error": "Email/username and password are required."}), 400

    # Find by email or username
    user = User.query.filter(
        (User.email == identifier) | (User.username == identifier)
    ).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email/username or password."}), 401
    if not user.is_active:
        return jsonify({"error": "Your account has been deactivated."}), 403

    token = _create_token(user)
    return jsonify(
        {"message": "Login successful!", "token": token, "user": user.to_dict()}
    )


@app.route("/api/auth/logout", methods=["POST"])
def logout():
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        token = AuthToken.query.filter_by(token=auth[7:]).first()
        if token:
            db.session.delete(token)
            db.session.commit()
    return jsonify({"message": "Logged out successfully."})


@app.route("/api/auth/me", methods=["GET"])
def me():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not authenticated."}), 401
    return jsonify({"user": user.to_dict()})


@app.route("/api/auth/update", methods=["PUT"])
def update_profile():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not authenticated."}), 401
    d = request.get_json() or {}
    full_name = d.get("full_name", "").strip()
    username = d.get("username", "").strip().lower()
    if not full_name or not username:
        return jsonify({"error": "Name and username are required."}), 400
    # Check username uniqueness (excluding self)
    existing = User.query.filter(User.username == username, User.id != user.id).first()
    if existing:
        return jsonify({"error": "Username already taken."}), 409
    user.full_name = full_name
    user.username = username
    db.session.commit()
    return jsonify({"message": "Profile updated.", "user": user.to_dict()})


@app.route("/api/auth/change-password", methods=["PUT"])
def change_password():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not authenticated."}), 401
    d = request.get_json() or {}
    current = d.get("current_password", "")
    new_pw = d.get("new_password", "")
    if not user.check_password(current):
        return jsonify({"error": "Current password is incorrect."}), 401
    if len(new_pw) < 6:
        return jsonify({"error": "New password must be at least 6 characters."}), 400
    user.set_password(new_pw)
    db.session.commit()
    return jsonify({"message": "Password changed successfully."})


@app.route("/api/auth/delete", methods=["DELETE"])
def delete_account():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not authenticated."}), 401
    # Delete all tokens first
    AuthToken.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Account deleted."})


def _create_token(user):
    """Generate a secure token valid for 30 days."""
    token_str = secrets.token_hex(32)
    expires = datetime.datetime.utcnow() + datetime.timedelta(days=30)
    token = AuthToken(user_id=user.id, token=token_str, expires_at=expires)
    db.session.add(token)
    db.session.commit()
    return token_str


# ══════════════════════════════════════════════════════════════════════════════
#  STUDENT PROFILE API
# ══════════════════════════════════════════════════════════════════════════════
@app.route("/api/student", methods=["POST"])
def save_student():
    d = request.get_json() or {}
    if Student.query.filter_by(email=d.get("email", "")).first():
        return jsonify({"message": "Email already registered"}), 409
    s = Student(
        full_name=d.get("full_name", ""),
        dob=d.get("dob", ""),
        gender=d.get("gender", ""),
        email=d.get("email", ""),
        phone=d.get("phone", ""),
        current_address=d.get("current_address", ""),
        permanent_address=d.get("permanent_address", ""),
        hobbies=d.get("hobbies", ""),
        clubs=d.get("clubs", ""),
        volunteer_work=d.get("volunteer_work", ""),
        languages_known=d.get("languages_known", ""),
        platforms=d.get("platforms", ""),
        specializations=d.get("specializations", ""),
        certifications=d.get("certifications", ""),
        career_goals=d.get("career_goals", ""),
        preferred_industries=d.get("preferred_industries", ""),
        internships=d.get("internships", ""),
    )
    db.session.add(s)
    db.session.commit()
    return jsonify({"id": s.id, "message": "Profile saved"}), 201


# ══════════════════════════════════════════════════════════════════════════════
#  SEED DATA
# ══════════════════════════════════════════════════════════════════════════════
def seed_data():
    if Accommodation.query.count() == 0:
        db.session.add_all(
            [
                # Pune
                Accommodation(
                    title="Sunrise PG for Boys",
                    type="PG",
                    city="Pune",
                    area="Kothrud",
                    rent=6000,
                    contact="9876543210",
                    amenities="WiFi, Meals, Laundry, Hot Water",
                    gender="Boys",
                    description="Fully furnished PG near VIT Pune. 3 meals daily, high-speed WiFi, attached bathroom. 5 min walk from college gate.",
                ),
                Accommodation(
                    title="Green Valley Girls Hostel",
                    type="PG",
                    city="Pune",
                    area="Bibwewadi",
                    rent=7500,
                    contact="9876543211",
                    amenities="WiFi, AC, Meals, Security, CCTV",
                    gender="Girls",
                    description="Safe and comfortable girls PG near engineering colleges in Bibwewadi. 24/7 security, biometric entry, AC rooms.",
                ),
                Accommodation(
                    title="Student Flat - 2BHK Warje",
                    type="Flat",
                    city="Pune",
                    area="Warje",
                    rent=12000,
                    contact="9876543212",
                    amenities="WiFi, Parking, 24/7 Water, Modular Kitchen",
                    gender="Co-ed",
                    description="Spacious 2BHK flat ideal for 2-3 students sharing. Fully furnished, near Warje bus stop. Rs.4,000 per head.",
                ),
                Accommodation(
                    title="Shivaji Nagar Boys PG",
                    type="PG",
                    city="Pune",
                    area="Shivaji Nagar",
                    rent=5500,
                    contact="9876543216",
                    amenities="WiFi, Meals, TV Room, Parking",
                    gender="Boys",
                    description="Budget PG near Pune University and FC Road. Homely atmosphere, Maharashtrian meals, monthly rent negotiable.",
                ),
                Accommodation(
                    title="Deccan Girls PG",
                    type="PG",
                    city="Pune",
                    area="Deccan Gymkhana",
                    rent=8500,
                    contact="9876543217",
                    amenities="WiFi, AC, Meals, Gym, Laundry",
                    gender="Girls",
                    description="Premium girls PG in the heart of Pune. Walking distance to Fergusson College and Deccan bus stand.",
                ),
                Accommodation(
                    title="Viman Nagar 1BHK Flat",
                    type="Flat",
                    city="Pune",
                    area="Viman Nagar",
                    rent=9000,
                    contact="9876543218",
                    amenities="WiFi, Parking, Balcony, Modular Kitchen",
                    gender="Co-ed",
                    description="Modern 1BHK flat near IT parks and Pune airport. Ideal for working students or 2 people sharing.",
                ),
                Accommodation(
                    title="Hadapsar Student Hostel",
                    type="Hostel",
                    city="Pune",
                    area="Hadapsar",
                    rent=4500,
                    contact="9876543219",
                    amenities="WiFi, Meals, Locker, Study Room",
                    gender="Boys",
                    description="Affordable hostel near Magarpatta City and IT companies. Shared rooms available. Study room open 24/7.",
                ),
                # Mumbai
                Accommodation(
                    title="Shree Ganesh PG Andheri",
                    type="PG",
                    city="Mumbai",
                    area="Andheri West",
                    rent=9000,
                    contact="9876543213",
                    amenities="WiFi, Meals, Gym, AC",
                    gender="Boys",
                    description="Premium PG near Mumbai University and Andheri station. Gym access, 3 meals, AC rooms available.",
                ),
                Accommodation(
                    title="Dadar Girls PG",
                    type="PG",
                    city="Mumbai",
                    area="Dadar",
                    rent=10000,
                    contact="9876543220",
                    amenities="WiFi, AC, Meals, Security, Laundry",
                    gender="Girls",
                    description="Well-maintained girls PG in central Mumbai. Close to Dadar station, easy access to all colleges.",
                ),
                Accommodation(
                    title="Powai Student Flat 2BHK",
                    type="Flat",
                    city="Mumbai",
                    area="Powai",
                    rent=18000,
                    contact="9876543221",
                    amenities="WiFi, Parking, Gym, Swimming Pool",
                    gender="Co-ed",
                    description="Premium 2BHK flat near IIT Bombay and Hiranandani. Ideal for 2-3 students. Society amenities included.",
                ),
                Accommodation(
                    title="Thane Budget PG",
                    type="PG",
                    city="Mumbai",
                    area="Thane West",
                    rent=6500,
                    contact="9876543222",
                    amenities="WiFi, Meals, Hot Water",
                    gender="Boys",
                    description="Affordable PG near Thane station. Good connectivity to Mumbai colleges via train. Veg meals only.",
                ),
                # Nagpur
                Accommodation(
                    title="Lakeview Flat Dharampeth",
                    type="Flat",
                    city="Nagpur",
                    area="Dharampeth",
                    rent=8000,
                    contact="9876543214",
                    amenities="WiFi, Parking, 24/7 Water",
                    gender="Co-ed",
                    description="Affordable flat near VNIT Nagpur and Dharampeth College. 2BHK, 2 students sharing.",
                ),
                Accommodation(
                    title="VNIT Boys PG",
                    type="PG",
                    city="Nagpur",
                    area="South Ambazari",
                    rent=5000,
                    contact="9876543223",
                    amenities="WiFi, Meals, Study Room",
                    gender="Boys",
                    description="Budget PG walking distance from VNIT Nagpur. Homely meals, quiet study environment.",
                ),
                Accommodation(
                    title="Nagpur Girls Hostel",
                    type="Hostel",
                    city="Nagpur",
                    area="Sitabuldi",
                    rent=4000,
                    contact="9876543224",
                    amenities="Meals, WiFi, CCTV, Warden",
                    gender="Girls",
                    description="Safe girls hostel near Nagpur University. Warden on premises, strict security, affordable rates.",
                ),
                # Nashik
                Accommodation(
                    title="Comfort Girls PG Nashik",
                    type="PG",
                    city="Nashik",
                    area="College Road",
                    rent=5500,
                    contact="9876543215",
                    amenities="Meals, WiFi, CCTV, Hot Water",
                    gender="Girls",
                    description="Budget-friendly girls PG near engineering colleges on College Road, Nashik. Home-cooked meals.",
                ),
                Accommodation(
                    title="Nashik Boys Flat",
                    type="Flat",
                    city="Nashik",
                    area="Gangapur Road",
                    rent=7000,
                    contact="9876543225",
                    amenities="WiFi, Parking, Kitchen",
                    gender="Boys",
                    description="2BHK flat near YCCE and other engineering colleges. 2-3 students sharing. Self-cooking facility.",
                ),
                # Aurangabad
                Accommodation(
                    title="BAMU Area PG",
                    type="PG",
                    city="Aurangabad",
                    area="Cidco",
                    rent=4500,
                    contact="9876543226",
                    amenities="WiFi, Meals, Parking",
                    gender="Boys",
                    description="PG near Dr. Babasaheb Ambedkar Marathwada University. Affordable rates, Maharashtrian meals.",
                ),
                Accommodation(
                    title="Aurangabad Girls PG",
                    type="PG",
                    city="Aurangabad",
                    area="Garkheda",
                    rent=5000,
                    contact="9876543227",
                    amenities="WiFi, Meals, Security, Laundry",
                    gender="Girls",
                    description="Safe girls PG near engineering and medical colleges in Aurangabad. Monthly and daily rates available.",
                ),
            ]
        )
    if MessTiffin.query.count() == 0:
        db.session.add_all(
            [
                # Pune
                MessTiffin(
                    name="Annapurna Mess",
                    type="Mess",
                    city="Pune",
                    area="Kothrud",
                    monthly_cost=2500,
                    contact="9876540001",
                    cuisine="Maharashtrian",
                    timing="7am-10am, 12pm-3pm, 7pm-10pm",
                    description="Home-style Maharashtrian thali with rice, dal, sabzi, chapati, and salad. Monthly subscription available. Veg only.",
                ),
                MessTiffin(
                    name="Tiffin Express",
                    type="Tiffin",
                    city="Pune",
                    area="Bibwewadi",
                    monthly_cost=1800,
                    contact="9876540002",
                    cuisine="North Indian / South Indian",
                    timing="Delivery: 12pm-2pm, 7pm-9pm",
                    description="Daily tiffin delivery to your doorstep. Veg and non-veg options. Lunch + dinner plan available.",
                ),
                MessTiffin(
                    name="VIT Canteen",
                    type="Canteen",
                    city="Pune",
                    area="Bibwewadi",
                    monthly_cost=0,
                    contact="9876540003",
                    cuisine="Multi-cuisine",
                    timing="8am-8pm",
                    description="On-campus canteen at VIT Pune. Affordable meals, snacks, and beverages. Pay per meal, no subscription needed.",
                ),
                MessTiffin(
                    name="Shivaji Nagar Mess",
                    type="Mess",
                    city="Pune",
                    area="Shivaji Nagar",
                    monthly_cost=2800,
                    contact="9876540006",
                    cuisine="Maharashtrian / North Indian",
                    timing="7am-9am, 12pm-2pm, 7pm-9pm",
                    description="Popular student mess near Pune University. Both veg and non-veg thali. Monthly and weekly plans.",
                ),
                MessTiffin(
                    name="Ghar Ka Swad Tiffin",
                    type="Tiffin",
                    city="Pune",
                    area="Kothrud",
                    monthly_cost=2000,
                    contact="9876540007",
                    cuisine="Maharashtrian",
                    timing="Delivery: 12:30pm, 8pm",
                    description="Home-cooked Maharashtrian food delivered fresh daily. Lunch and dinner. Monthly subscription Rs.2,000.",
                ),
                MessTiffin(
                    name="Deccan Mess",
                    type="Mess",
                    city="Pune",
                    area="Deccan Gymkhana",
                    monthly_cost=3000,
                    contact="9876540008",
                    cuisine="Multi-cuisine",
                    timing="7am-10am, 12pm-3pm, 7pm-10pm",
                    description="Premium mess near Fergusson College. Unlimited thali, multiple cuisine options. AC dining hall.",
                ),
                MessTiffin(
                    name="Viman Nagar Tiffin Service",
                    type="Tiffin",
                    city="Pune",
                    area="Viman Nagar",
                    monthly_cost=2200,
                    contact="9876540009",
                    cuisine="North Indian / Gujarati",
                    timing="Delivery: 1pm, 8:30pm",
                    description="Fresh tiffin delivery near IT parks and colleges. Veg only. Monthly plan with 26 days service.",
                ),
                MessTiffin(
                    name="Hadapsar Student Canteen",
                    type="Canteen",
                    city="Pune",
                    area="Hadapsar",
                    monthly_cost=0,
                    contact="9876540010",
                    cuisine="South Indian / North Indian",
                    timing="7am-9pm",
                    description="Affordable canteen near Magarpatta. Idli, dosa, rice meals, and snacks. Student discounts available.",
                ),
                # Mumbai
                MessTiffin(
                    name="Shivaji Mess Andheri",
                    type="Mess",
                    city="Mumbai",
                    area="Andheri West",
                    monthly_cost=3000,
                    contact="9876540004",
                    cuisine="Maharashtrian / Gujarati",
                    timing="7am-9am, 12pm-2pm, 7pm-9pm",
                    description="Popular student mess near Mumbai University. Unlimited thali, both veg and non-veg options.",
                ),
                MessTiffin(
                    name="Dadar Tiffin Center",
                    type="Tiffin",
                    city="Mumbai",
                    area="Dadar",
                    monthly_cost=2500,
                    contact="9876540011",
                    cuisine="Maharashtrian",
                    timing="Delivery: 12pm-1pm, 7pm-8pm",
                    description="Traditional Maharashtrian tiffin delivered in Dadar area. Lunch + dinner. Dabba service available.",
                ),
                MessTiffin(
                    name="Powai Mess",
                    type="Mess",
                    city="Mumbai",
                    area="Powai",
                    monthly_cost=3500,
                    contact="9876540012",
                    cuisine="Multi-cuisine",
                    timing="7am-10am, 12pm-3pm, 7pm-10pm",
                    description="Mess near IIT Bombay and Hiranandani. Variety of cuisines, AC dining. Popular among IIT students.",
                ),
                MessTiffin(
                    name="Thane Tiffin Service",
                    type="Tiffin",
                    city="Mumbai",
                    area="Thane West",
                    monthly_cost=1800,
                    contact="9876540013",
                    cuisine="Maharashtrian / North Indian",
                    timing="Delivery: 12:30pm, 8pm",
                    description="Affordable tiffin delivery in Thane. Home-cooked food, veg only. Monthly plan with Sunday off.",
                ),
                # Nagpur
                MessTiffin(
                    name="Ghar Ka Khana Tiffin",
                    type="Tiffin",
                    city="Nagpur",
                    area="Dharampeth",
                    monthly_cost=1500,
                    contact="9876540005",
                    cuisine="Vidarbha style",
                    timing="Delivery: 1pm, 8pm",
                    description="Authentic Vidarbha-style home-cooked food delivered to students. Veg and non-veg. Most affordable in Nagpur.",
                ),
                MessTiffin(
                    name="VNIT Mess",
                    type="Mess",
                    city="Nagpur",
                    area="South Ambazari",
                    monthly_cost=2200,
                    contact="9876540014",
                    cuisine="Multi-cuisine",
                    timing="7am-9am, 12pm-2pm, 7pm-9pm",
                    description="Mess near VNIT Nagpur. Subsidised rates for students. Veg and non-veg thali. Monthly subscription.",
                ),
                MessTiffin(
                    name="Nagpur Canteen",
                    type="Canteen",
                    city="Nagpur",
                    area="Sitabuldi",
                    monthly_cost=0,
                    contact="9876540015",
                    cuisine="Maharashtrian / South Indian",
                    timing="8am-8pm",
                    description="Central Nagpur canteen near colleges. Affordable meals, snacks, and beverages. No subscription needed.",
                ),
                # Nashik
                MessTiffin(
                    name="Nashik Student Mess",
                    type="Mess",
                    city="Nashik",
                    area="College Road",
                    monthly_cost=2000,
                    contact="9876540016",
                    cuisine="Maharashtrian",
                    timing="7am-9am, 12pm-2pm, 7pm-9pm",
                    description="Budget mess near engineering colleges on College Road. Home-style Maharashtrian food. Veg only.",
                ),
                MessTiffin(
                    name="Nashik Tiffin Delivery",
                    type="Tiffin",
                    city="Nashik",
                    area="Gangapur Road",
                    monthly_cost=1600,
                    contact="9876540017",
                    cuisine="North Indian / Maharashtrian",
                    timing="Delivery: 1pm, 8pm",
                    description="Daily tiffin delivery in Nashik. Lunch and dinner. Veg and non-veg options. Monthly plan.",
                ),
                # Aurangabad
                MessTiffin(
                    name="Aurangabad Student Mess",
                    type="Mess",
                    city="Aurangabad",
                    area="Cidco",
                    monthly_cost=2000,
                    contact="9876540018",
                    cuisine="Maharashtrian",
                    timing="7am-9am, 12pm-2pm, 7pm-9pm",
                    description="Affordable mess near BAMU and engineering colleges. Unlimited Maharashtrian thali. Monthly subscription.",
                ),
            ]
        )
    if Scholarship.query.count() == 0:
        db.session.add_all(
            [
                Scholarship(
                    name="National Merit Scholarship",
                    provider="Government of India",
                    amount="Rs.12,000/year",
                    eligibility="Top 1% in Class 12 board exams",
                    deadline="31 Oct 2025",
                    category="Merit",
                    apply_link="https://scholarships.gov.in",
                    description="Central government scholarship for meritorious students.",
                ),
                Scholarship(
                    name="Post Matric Scholarship for SC/ST",
                    provider="Ministry of Social Justice",
                    amount="Up to Rs.1,20,000/year",
                    eligibility="SC/ST students with family income below Rs.2.5 LPA",
                    deadline="30 Nov 2025",
                    category="SC/ST",
                    apply_link="https://scholarships.gov.in",
                    description="Financial assistance for SC/ST students pursuing higher education.",
                ),
                Scholarship(
                    name="Pragati Scholarship for Girls",
                    provider="AICTE",
                    amount="Rs.50,000/year",
                    eligibility="Girl students in AICTE approved technical institutions, family income below Rs.8 LPA",
                    deadline="31 Dec 2025",
                    category="Girls",
                    apply_link="https://www.aicte-india.org/bureaus/pgd/pragati",
                    description="AICTE scholarship to promote technical education among girl students.",
                ),
                Scholarship(
                    name="Saksham Scholarship",
                    provider="AICTE",
                    amount="Rs.50,000/year",
                    eligibility="Differently abled students in AICTE approved institutions, family income below Rs.8 LPA",
                    deadline="31 Dec 2025",
                    category="Merit",
                    apply_link="https://www.aicte-india.org/bureaus/pgd/saksham",
                    description="AICTE scholarship for differently abled students pursuing technical education.",
                ),
                Scholarship(
                    name="EWS Scholarship Maharashtra",
                    provider="Maharashtra Government",
                    amount="Rs.25,000/year",
                    eligibility="EWS category students, family income below Rs.8 LPA",
                    deadline="15 Jan 2026",
                    category="EWS",
                    apply_link="https://mahadbt.maharashtra.gov.in",
                    description="State scholarship for economically weaker section students in Maharashtra.",
                ),
                Scholarship(
                    name="INSPIRE Scholarship",
                    provider="DST, Government of India",
                    amount="Rs.80,000/year",
                    eligibility="Top 1% in Class 12, pursuing BSc/BE/BTech in natural sciences",
                    deadline="28 Feb 2026",
                    category="Merit",
                    apply_link="https://online-inspire.gov.in",
                    description="Attracts talented students to science and technology.",
                ),
                Scholarship(
                    name="OBC Post Matric Scholarship",
                    provider="Ministry of Social Justice",
                    amount="Up to Rs.57,000/year",
                    eligibility="OBC students, family income below Rs.1 LPA",
                    deadline="30 Nov 2025",
                    category="OBC",
                    apply_link="https://scholarships.gov.in",
                    description="Financial support for OBC students in higher education.",
                ),
                Scholarship(
                    name="Central Sector Scheme of Scholarship",
                    provider="Ministry of Education",
                    amount="Rs.20,000/year (UG)",
                    eligibility="Top 20 percentile in Class 12, family income below Rs.8 LPA",
                    deadline="31 Oct 2025",
                    category="Merit",
                    apply_link="https://scholarships.gov.in",
                    description="Scholarship for students in top 20 percentile of their boards.",
                ),
                Scholarship(
                    name="Minority Post Matric Scholarship",
                    provider="Ministry of Minority Affairs",
                    amount="Up to Rs.30,000/year",
                    eligibility="Minority community students, family income below Rs.2 LPA",
                    deadline="31 Oct 2025",
                    category="Minority",
                    apply_link="https://scholarships.gov.in",
                    description="Financial assistance for students from minority communities.",
                ),
                Scholarship(
                    name="KVPY Fellowship",
                    provider="IISc Bangalore / DST",
                    amount="Rs.5,000-Rs.7,000/month",
                    eligibility="Class 11 to 1st year BSc/BE/BTech with aptitude for research",
                    deadline="15 Sep 2025",
                    category="Merit",
                    apply_link="https://kvpy.iisc.ac.in",
                    description="Fellowship to encourage students with aptitude for research.",
                ),
                Scholarship(
                    name="Reliance Foundation Scholarship",
                    provider="Reliance Foundation",
                    amount="Rs.4,00,000 (one-time)",
                    eligibility="UG students in STEM, family income below Rs.15 LPA, min 60% in Class 12",
                    deadline="15 Feb 2026",
                    category="Merit",
                    apply_link="https://www.reliancefoundation.org/scholarships",
                    description="Scholarship for meritorious students from economically weaker backgrounds.",
                ),
                Scholarship(
                    name="Sports Scholarship - SAI",
                    provider="Sports Authority of India",
                    amount="Rs.10,000-Rs.25,000/month",
                    eligibility="National/International level sportspersons pursuing higher education",
                    deadline="31 Aug 2025",
                    category="Sports",
                    apply_link="https://sportsauthorityofindia.nic.in",
                    description="Financial support for sportspersons to continue education.",
                ),
            ]
        )
    db.session.commit()


def seed_resources():
    if Resource.query.count() > 0:
        return
    db.session.add_all(
        [
            Resource(
                title="MHT-CET 2024 PCM Full Paper with Solutions",
                exam="MHT-CET",
                subject="All",
                resource_type="PYQ",
                year="2024",
                description="Complete MHT-CET 2024 PCM question paper with detailed solutions.",
                file_url="https://mhtcet2024.mahacet.org",
                is_free=True,
                downloads=4821,
                tags="mhtcet,2024,pcm,physics,chemistry,maths,solved",
            ),
            Resource(
                title="MHT-CET 2023 PCM Full Paper with Solutions",
                exam="MHT-CET",
                subject="All",
                resource_type="PYQ",
                year="2023",
                description="Complete MHT-CET 2023 PCM question paper with answer key.",
                file_url="https://mhtcet2023.mahacet.org",
                is_free=True,
                downloads=6340,
                tags="mhtcet,2023,pcm,solved",
            ),
            Resource(
                title="MHT-CET 2022 PCM Full Paper",
                exam="MHT-CET",
                subject="All",
                resource_type="PYQ",
                year="2022",
                description="MHT-CET 2022 PCM question paper with answer key.",
                file_url="https://mhtcet2022.mahacet.org",
                is_free=True,
                downloads=5120,
                tags="mhtcet,2022,pcm",
            ),
            Resource(
                title="MHT-CET Last 10 Years Papers (2014-2024)",
                exam="MHT-CET",
                subject="All",
                resource_type="PYQ",
                year="2014-2024",
                description="Compilation of last 10 years MHT-CET question papers with solutions.",
                file_url="https://mahacet.org",
                is_free=True,
                downloads=9870,
                tags="mhtcet,pyq,10years,compilation",
            ),
            Resource(
                title="JEE Main Jan 2024 - All Shifts with Answer Key",
                exam="JEE",
                subject="All",
                resource_type="PYQ",
                year="2024",
                description="All shifts of JEE Main January 2024 with official answer keys.",
                file_url="https://jeemain.nta.nic.in",
                is_free=True,
                downloads=12450,
                tags="jee,2024,january,all shifts,answer key",
            ),
            Resource(
                title="JEE Main April 2024 - All Shifts",
                exam="JEE",
                subject="All",
                resource_type="PYQ",
                year="2024",
                description="All shifts of JEE Main April 2024 with solutions.",
                file_url="https://jeemain.nta.nic.in",
                is_free=True,
                downloads=10230,
                tags="jee,2024,april",
            ),
            Resource(
                title="JEE Advanced 2024 Paper 1 and 2",
                exam="JEE",
                subject="All",
                resource_type="PYQ",
                year="2024",
                description="JEE Advanced 2024 both papers with detailed solutions.",
                file_url="https://jeeadv.ac.in",
                is_free=True,
                downloads=8760,
                tags="jee advanced,2024,paper1,paper2,iit",
            ),
            Resource(
                title="JEE Main Last 5 Years Papers (2020-2024)",
                exam="JEE",
                subject="All",
                resource_type="PYQ",
                year="2020-2024",
                description="Compilation of JEE Main papers from 2020 to 2024.",
                file_url="https://jeemain.nta.nic.in",
                is_free=True,
                downloads=15600,
                tags="jee,pyq,5years,compilation",
            ),
            Resource(
                title="BITSAT 2024 Sample Paper with Solutions",
                exam="BITSAT",
                subject="All",
                resource_type="PYQ",
                year="2024",
                description="Official BITSAT 2024 sample paper with complete solutions.",
                file_url="https://www.bitsadmission.com",
                is_free=True,
                downloads=5430,
                tags="bitsat,2024,sample",
            ),
            Resource(
                title="BITSAT Previous Years Papers (2019-2024)",
                exam="BITSAT",
                subject="All",
                resource_type="PYQ",
                year="2019-2024",
                description="BITSAT papers from 2019 to 2024 with answer keys.",
                file_url="https://www.bitsadmission.com",
                is_free=True,
                downloads=7890,
                tags="bitsat,pyq,compilation",
            ),
            Resource(
                title="Physics Formula Sheet - JEE and MHT-CET",
                exam="JEE",
                subject="Physics",
                resource_type="Formula Sheet",
                year="",
                description="All important physics formulas: Mechanics, Electrostatics, Optics, Modern Physics.",
                file_url="#",
                is_free=True,
                downloads=18900,
                tags="physics,formula,jee,mhtcet",
            ),
            Resource(
                title="Physics Chapter-wise Notes - Class 11 and 12",
                exam="General",
                subject="Physics",
                resource_type="Notes",
                year="",
                description="Comprehensive chapter-wise physics notes for Class 11 and 12.",
                file_url="#",
                is_free=True,
                downloads=14320,
                tags="physics,notes,class11,class12,ncert",
            ),
            Resource(
                title="Physics Short Tricks and Shortcuts",
                exam="JEE",
                subject="Physics",
                resource_type="Notes",
                year="",
                description="Quick tricks and shortcuts for solving physics problems faster.",
                file_url="#",
                is_free=True,
                downloads=9870,
                tags="physics,tricks,shortcuts,jee,mhtcet",
            ),
            Resource(
                title="Chemistry Formula Sheet - Organic and Inorganic",
                exam="JEE",
                subject="Chemistry",
                resource_type="Formula Sheet",
                year="",
                description="Complete chemistry formula sheet: Organic reactions, Inorganic facts, Physical chemistry.",
                file_url="#",
                is_free=True,
                downloads=16540,
                tags="chemistry,formula,organic,inorganic,physical,jee",
            ),
            Resource(
                title="Organic Chemistry Reaction Mechanisms",
                exam="JEE",
                subject="Chemistry",
                resource_type="Notes",
                year="",
                description="Detailed notes on all important organic chemistry reaction mechanisms.",
                file_url="#",
                is_free=True,
                downloads=11230,
                tags="chemistry,organic,reactions,mechanisms,jee",
            ),
            Resource(
                title="Inorganic Chemistry Quick Revision Notes",
                exam="General",
                subject="Chemistry",
                resource_type="Notes",
                year="",
                description="Quick revision notes for inorganic chemistry for JEE and MHT-CET.",
                file_url="#",
                is_free=True,
                downloads=8760,
                tags="chemistry,inorganic,revision,jee,mhtcet",
            ),
            Resource(
                title="Mathematics Formula Sheet - JEE and MHT-CET",
                exam="JEE",
                subject="Mathematics",
                resource_type="Formula Sheet",
                year="",
                description="All important maths formulas: Calculus, Algebra, Trigonometry, Coordinate Geometry.",
                file_url="#",
                is_free=True,
                downloads=21000,
                tags="maths,formula,calculus,algebra,trigonometry,jee,mhtcet",
            ),
            Resource(
                title="Calculus Notes - Differentiation and Integration",
                exam="JEE",
                subject="Mathematics",
                resource_type="Notes",
                year="",
                description="Comprehensive notes on differential and integral calculus with solved examples.",
                file_url="#",
                is_free=True,
                downloads=13450,
                tags="maths,calculus,differentiation,integration,jee",
            ),
            Resource(
                title="Coordinate Geometry Complete Notes",
                exam="General",
                subject="Mathematics",
                resource_type="Notes",
                year="",
                description="Complete notes on coordinate geometry: straight lines, circles, parabola, ellipse, hyperbola.",
                file_url="#",
                is_free=True,
                downloads=9870,
                tags="maths,coordinate geometry,circles,parabola,jee,mhtcet",
            ),
            Resource(
                title="Biology Quick Revision Notes - NEET and MHT-CET",
                exam="MHT-CET",
                subject="Biology",
                resource_type="Notes",
                year="",
                description="Chapter-wise quick revision notes for Biology covering Botany and Zoology.",
                file_url="#",
                is_free=True,
                downloads=7650,
                tags="biology,neet,mhtcet,botany,zoology,revision",
            ),
            Resource(
                title="Biology Diagrams and Flowcharts",
                exam="General",
                subject="Biology",
                resource_type="Notes",
                year="",
                description="Important biology diagrams and flowcharts for quick revision.",
                file_url="#",
                is_free=True,
                downloads=5430,
                tags="biology,diagrams,flowcharts,neet,mhtcet",
            ),
            Resource(
                title="Physics Video Lectures - JEE by IIT Alumni",
                exam="JEE",
                subject="Physics",
                resource_type="Video",
                year="",
                description="Free YouTube playlist of physics video lectures by IIT alumni.",
                file_url="https://www.youtube.com/results?search_query=jee+physics+lectures",
                is_free=True,
                downloads=0,
                tags="physics,video,lectures,jee,youtube,iit",
            ),
            Resource(
                title="Chemistry Video Lectures - Organic Chemistry",
                exam="JEE",
                subject="Chemistry",
                resource_type="Video",
                year="",
                description="Curated YouTube playlist for organic chemistry video lectures.",
                file_url="https://www.youtube.com/results?search_query=jee+organic+chemistry+lectures",
                is_free=True,
                downloads=0,
                tags="chemistry,organic,video,lectures,jee,youtube",
            ),
            Resource(
                title="Maths Video Lectures - Calculus and Algebra",
                exam="JEE",
                subject="Mathematics",
                resource_type="Video",
                year="",
                description="Free video lectures on calculus and algebra for JEE and MHT-CET.",
                file_url="https://www.youtube.com/results?search_query=jee+maths+calculus+lectures",
                is_free=True,
                downloads=0,
                tags="maths,video,calculus,algebra,jee,youtube",
            ),
            Resource(
                title="MHT-CET Complete Video Course - Free",
                exam="MHT-CET",
                subject="All",
                resource_type="Video",
                year="",
                description="Complete free video course for MHT-CET covering Physics, Chemistry, and Maths.",
                file_url="https://www.youtube.com/results?search_query=mht+cet+complete+course",
                is_free=True,
                downloads=0,
                tags="mhtcet,video,course,free,pcm",
            ),
            Resource(
                title="MHT-CET Full Mock Test - 2025 Pattern",
                exam="MHT-CET",
                subject="All",
                resource_type="Mock Test",
                year="2025",
                description="Full-length mock test based on 2025 MHT-CET pattern with auto-scoring.",
                file_url="/pages/practice.html",
                is_free=True,
                downloads=3210,
                tags="mhtcet,mock test,2025,practice",
            ),
            Resource(
                title="JEE Main Mock Test - 2025 Pattern",
                exam="JEE",
                subject="All",
                resource_type="Mock Test",
                year="2025",
                description="Full-length JEE Main mock test with 90 questions and instant results.",
                file_url="/pages/practice.html",
                is_free=True,
                downloads=5670,
                tags="jee,mock test,2025,practice",
            ),
            Resource(
                title="BITSAT Mock Test - 150 Questions",
                exam="BITSAT",
                subject="All",
                resource_type="Mock Test",
                year="2025",
                description="BITSAT pattern mock test with 150 questions including English and Logical Reasoning.",
                file_url="/pages/practice.html",
                is_free=True,
                downloads=2340,
                tags="bitsat,mock test,2025,practice",
            ),
        ]
    )
    db.session.commit()


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_data()
        seed_resources()
    app.run(debug=True, port=5000)
