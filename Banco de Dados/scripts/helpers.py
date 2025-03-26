import psycopg2
from config import DB_CONFIG, SQL_SCRIPTS_DIR, DEMONSTRACOES_DIR, DATA_DIR
from pathlib import Path
import pandas as pd

class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.cur = None

    def connect(self):
        """Estabelece conexão com o banco de dados"""
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cur = self.conn.cursor()
            print("Conexão com o banco de dados estabelecida com sucesso!")
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            raise

    def disconnect(self):
        """Fecha a conexão com o banco de dados"""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
            print("Conexão com o banco de dados encerrada.")

    def execute_sql_file(self, file_path):
        """Executa um arquivo SQL"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                sql = f.read()
                self.cur.execute(sql)
                self.conn.commit()
            print(f"Script {file_path.name} executado com sucesso!")
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao executar o script {file_path.name}: {e}")
            return False

    def generate_load_script(self):
        """Gera o script SQL para carregar todos os arquivos CSV"""
        load_script_path = SQL_SCRIPTS_DIR / "02_load_data.sql"
        
        # Operadoras Ativas
        operadoras_path = DATA_DIR / "operadoras_ativas.csv"
        sql_content = [
            f"-- Carregamento de Operadoras Ativas",
            f"\\copy operadoras_ativas FROM '{operadoras_path}' WITH (FORMAT CSV, DELIMITER ';', HEADER, ENCODING 'UTF8');\n"
        ]
        
        # Demonstrações Contábeis
        sql_content.append("-- Carregamento de Demonstrações Contábeis")
        csv_files = list(DEMONSTRACOES_DIR.glob('*.csv'))
        
        for csv_file in csv_files:
            sql_content.append(
                f"\\copy demonstracoes_contabeis(registro_ans, data, conta_contabil, descricao, valor, tipo_movimento) "
                f"FROM '{csv_file}' WITH (FORMAT CSV, DELIMITER ';', HEADER, ENCODING 'ISO-8859-1');"
            )
        
        # Salvar o script
        with open(load_script_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sql_content))
        
        print(f"Script de carga gerado em: {load_script_path}")
        return load_script_path

    def run_analytical_queries(self):
        """Executa as consultas analíticas e salva os resultados"""
        results = {}
        queries_path = SQL_SCRIPTS_DIR / "03_analytical_queries.sql"
        
        with open(queries_path, 'r', encoding='utf-8') as f:
            sql_queries = f.read().split(';')
        
        for i, query in enumerate(sql_queries, 1):
            query = query.strip()
            if not query:
                continue
                
            try:
                self.cur.execute(query)
                columns = [desc[0] for desc in self.cur.description]
                data = self.cur.fetchall()
                
                # Converter para DataFrame
                df = pd.DataFrame(data, columns=columns)
                results[f"query_{i}"] = df
                
                print(f"\nResultado da Consulta {i}:")
                print(df.to_markdown(index=False))
                
                # Salvar como CSV
                csv_path = DATA_DIR / f"resultado_consulta_{i}.csv"
                df.to_csv(csv_path, index=False, encoding='utf-8')
                print(f"Resultado salvo em: {csv_path}")
                
            except Exception as e:
                print(f"Erro ao executar consulta {i}: {e}")
        
        return results