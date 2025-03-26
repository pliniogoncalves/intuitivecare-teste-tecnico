import pandas as pd
import tabula
import zipfile
import os
from pathlib import Path
import PyPDF2
import warnings

# Configuração de caminhos
BASE_DIR = Path(__file__).parent.parent
WEB_SCRAPING_DIR = BASE_DIR / "Web Scraping" / "anexos"
TRANSFORMACAO_DIR = BASE_DIR / "Transformação de Dados"

def extract_pdf_tables(pdf_path):
    try:
        print(f"Extraindo tabelas de: {pdf_path}...")
        
        # Tentativa 1: Leitura com parâmetros otimizados
        tables = tabula.read_pdf(
            str(pdf_path),
            pages='all',
            multiple_tables=True,
            lattice=True,
            stream=True,  # Alternar entre lattice e stream
            pandas_options={'header': None},
            area=[0, 0, 100, 100],  # Área total da página
            guess=False,
            silent=True
        )
        
        # Se não extraiu tabelas, tentar método alternativo
        if not tables:
            warnings.warn("Primeira tentativa falhou. Tentando método alternativo...")
            tables = tabula.read_pdf(
                str(pdf_path),
                pages='all',
                multiple_tables=True,
                stream=False,  # Tentar com lattice
                lattice=True,
                pandas_options={'header': None}
            )
        
        # Verificar se extraiu alguma tabela
        if not tables:
            raise ValueError("Nenhuma tabela foi detectada no PDF. Verifique o formato do arquivo.")
            
        return pd.concat(tables, ignore_index=True)
        
    except Exception as e:
        print(f"\n Erro na extração: {e}")
        
        # Verificação básica do PDF
        try:
            with open(pdf_path, "rb") as f:
                pdf = PyPDF2.PdfReader(f)
                print(f"O PDF possui {len(pdf.pages)} páginas.")
                if len(pdf.pages) == 0:
                    print("O PDF está vazio!")
        except Exception as pdf_error:
            print(f"Erro ao verificar PDF: {pdf_error}")
        
        raise

def process_and_save_table(df, output_csv):
    """
    Processa o DataFrame extraído e salva como CSV.
    """
    try:
        df_cleaned = df.dropna(how='all')
        
        # Salvar o DataFrame processado como CSV
        df_cleaned.to_csv(output_csv, index=False, encoding='utf-8')
        print(f" Dados processados e salvos em: {output_csv}")
    except Exception as e:
        raise RuntimeError(f"Erro ao processar e salvar a tabela: {e}")

def create_zip(file_path, zip_name):
    """
    Compacta o arquivo CSV em um arquivo ZIP.
    """
    try:
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file_path, arcname=os.path.basename(file_path))
        print(f" Arquivo ZIP criado em: {zip_name}")
    except Exception as e:
        raise RuntimeError(f"Erro ao criar o arquivo ZIP: {e}")

def main():
    try:
        # Caminhos dos arquivos
        pdf_path = WEB_SCRAPING_DIR / "Anexo_I.pdf"
        output_csv = TRANSFORMACAO_DIR / "Rol_de_Procedimentos.csv"
        zip_name = TRANSFORMACAO_DIR / "Teste_PlinioGoncalves.zip"
        
        # Verificações iniciais
        if not pdf_path.exists():
            raise FileNotFoundError(f"Arquivo PDF não encontrado: {pdf_path}")

        print("\n=== INÍCIO DO PROCESSAMENTO ===")
        
        # Etapa 1: Extração
        print("\nETAPA 1: Extração de tabelas do PDF")
        df_raw = extract_pdf_tables(pdf_path)
        print(f" Extraídas {len(df_raw)} linhas da tabela")
        
        # Etapa 2: Processamento
        print("\nETAPA 2: Processamento dos dados")
        process_and_save_table(df_raw, output_csv)
        print(f" CSV gerado em: {output_csv}")
        
        # Etapa 3: Compactação
        print("\nETAPA 3: Criação do arquivo ZIP")
        create_zip(output_csv, zip_name)
        print(f" ZIP criado em: {zip_name}")
        
        print("\n=== PROCESSO CONCLUÍDO COM SUCESSO ===")
        
    except Exception as e:
        print(f"\n ERRO: {e}")
        print("\nSugestões para resolver:")
        print("1. Verifique se o PDF contém tabelas (abra manualmente)")
        print("2. Tente outro método de extração (camelot, pdfplumber)")
        print("3. Verifique se o PDF não está corrompido")
        print("4. Considere converter o PDF para Excel primeiro")
        return 1
    
    return 0

if __name__ == "__main__":
    main()