from database import Base, engine
from models import Document, Chapter, Translation, TranslatorProfile, TranslationRevision

# Criar todas as tabelas
def create_tables():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Banco de dados recriado com sucesso!")

if __name__ == "__main__":
    create_tables()
