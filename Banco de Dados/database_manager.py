from scripts.helpers import DatabaseManager
from config import SQL_SCRIPTS_DIR
import time

def setup_database():
    db = DatabaseManager()
    try:
        db.connect()
        
        # 1. Criar tabelas
        print("\n=== CRIANDO TABELAS ===")
        db.execute_sql_file(SQL_SCRIPTS_DIR / "01_create_tables.sql")
        
        # 2. Gerar e executar script de carga
        print("\n=== CARREGANDO DADOS ===")
        load_script = db.generate_load_script()
        db.execute_sql_file(load_script)
        
        # 3. Executar consultas analíticas
        print("\n=== EXECUTANDO CONSULTAS ANALÍTICAS ===")
        db.run_analytical_queries()
        
    except Exception as e:
        print(f"Erro durante a execução: {e}")
    finally:
        db.disconnect()

if __name__ == "__main__":
    start_time = time.time()
    setup_database()
    print(f"\nProcesso concluído em {time.time() - start_time:.2f} segundos")