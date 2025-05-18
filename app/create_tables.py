from app.db.session import engine, Base
from app.models import alarma  # importa el modelo de la alarma

Base.metadata.create_all(bind=engine)