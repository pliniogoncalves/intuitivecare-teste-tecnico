from download_data import DataDownloader
from database_manager import setup_database
import argparse

def main():
    parser = argparse.ArgumentParser(description="Teste 3 - Banco de Dados ANS")
    parser.add_argument('--download', action='store_true', help='Baixar dados antes de executar')
    args = parser.parse_args()

    if args.download:
        print("=== INICIANDO DOWNLOAD DOS DADOS ===")
        downloader = DataDownloader()
        downloader.download_latest_operadoras()
        downloader.download_demonstracoes_contabeis(years=2)
    
    print("\n=== CONFIGURANDO BANCO DE DADOS ===")
    setup_database()

if __name__ == "__main__":
    main()