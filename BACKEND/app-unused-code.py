# Default to MySQL; flip to Postgres by changing env or compose.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://appuser:app_pass_123@mysql:3306/appdb"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.current_timestamp())

app = Flask(__name__)
Base.metadata.create_all(bind=engine)


@app.before_request
def _open_session():
    g.db = SessionLocal()

@app.teardown_request
def _close_session(exc):
    db = g.pop("db", None)
    if db is not None:
        if exc:
            db.rollback()
        db.close()

@app.get("/")
def root():
    return jsonify({"status": "ok", "db": DATABASE_URL.split('://',1)[0]})

@app.get("/users/")
def list_users():
    users = g.db.execute(select(User)).scalars().all()
    return jsonify([{"id": u.id, "email": u.email, "full_name": u.full_name} for u in users])

@app.post("/users/")
def create_user():
    data = (request.get_json(silent=True) or {})
    email = (data.get("email") or "").strip()
    full_name = (data.get("full_name") or "").strip()

    if not full_name:
        return jsonify({"detail": "full_name is required"}), 422
    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError as e:
        return jsonify({"detail": f"Invalid email: {e}"}), 422

    u = User(email=email, full_name=full_name)
    g.db.add(u)
    try:
        g.db.commit()
        g.db.refresh(u)
    except IntegrityError:
        g.db.rollback()
        return jsonify({"detail": "Email already exists"}), 409

    return jsonify({"id": u.id, "email": u.email, "full_name": u.full_name}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
