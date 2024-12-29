from sqlalchemy import create_engine, text
from database import SQLALCHEMY_DATABASE_URL
import os

def reset_database():
    # Criar engine
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    try:
        # Conectar ao banco de dados
        with engine.connect() as connection:
            # Remover tabela de versões do alembic se existir
            connection.execute(text("DROP TABLE IF EXISTS alembic_version"))
            connection.commit()
            print("Tabela alembic_version removida com sucesso!")
            
            # Remover outras tabelas relacionadas ao projeto
            tables = [
                "translation_revisions",
                "translations",
                "chapters",
                "documents",
                "translator_profiles"
            ]
            
            for table in tables:
                connection.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
                connection.commit()
                print(f"Tabela {table} removida com sucesso!")
                
    except Exception as e:
        print(f"Erro ao resetar o banco de dados: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    print("Iniciando reset do banco de dados...")
    success = reset_database()
    if success:
        print("Banco de dados resetado com sucesso!")
    else:
        print("Falha ao resetar o banco de dados.")
