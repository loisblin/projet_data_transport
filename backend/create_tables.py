from backend.database import engine
from backend.models import Base


# Supprime toutes les tables
Base.metadata.drop_all(bind=engine)

# Recréé toutes les tables à partir des modèles
Base.metadata.create_all(bind=engine)

print("Base update !")