from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

# Carregamento do CSV com tratamento robusto
try:
    df = pd.read_csv('operadoras_ativas.csv', encoding='utf-8', sep=';')
except Exception as e:
    print(f"Erro ao ler com UTF-8: {e}")
    try:
        df = pd.read_csv('operadoras_ativas.csv', encoding='latin-1', sep=';')
    except Exception as e:
        print(f"Erro ao ler com Latin-1: {e}")
        df = pd.DataFrame()

# Converter colunas problemáticas para string
if not df.empty:
    df = df.replace({np.nan: None, pd.NA: None})
    for col in ['DDD', 'Telefone', 'Fax']:
        if col in df.columns:
            df[col] = df[col].astype(str)

@app.route('/search', methods=['GET'])
def search():
    try:
        if df.empty:
            return jsonify({"error": "Dados não carregados"}), 500

        query = request.args.get('q', '').lower().strip()
        if not query:
            return jsonify({"error": "Parâmetro 'q' ausente"}), 400

        # Busca segura
        mask = (
            df['Razao_Social'].str.lower().str.contains(query, na=False) |
            df['Nome_Fantasia'].str.lower().str.contains(query, na=False) |
            df['CNPJ'].astype(str).str.contains(query, na=False)
        )
        
        results = df[mask].head(20)
        return jsonify(results.to_dict(orient='records'))

    except Exception as e:
        print(f"Erro na busca: {str(e)}")
        return jsonify({"error": "Erro interno no servidor"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)