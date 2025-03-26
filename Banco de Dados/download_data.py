import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
from config import DATA_DIR, DEMONSTRACOES_DIR, URLS
import pandas as pd
import re
from urllib.parse import urljoin
from pathlib import Path

class DataDownloader:
    @staticmethod
    def download_latest_operadoras():
        """Download do arquivo CSV de operadoras ativas (3.2)"""
        print("\n=== BAIXANDO DADOS DE OPERADORAS ATIVAS (CSV) ===")
        response = requests.get(URLS['operadoras'])
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontrar o link do CSV
        csv_link = None
        for a in soup.find_all('a'):
            href = a.get('href', '')
            if href.endswith('.csv'):
                csv_link = href
                break
        
        if not csv_link:
            raise Exception("Nenhum arquivo CSV encontrado para operadoras ativas")
        
        file_url = urljoin(URLS['operadoras'], csv_link)
        save_path = DATA_DIR / "operadoras_ativas.csv"
        
        print(f"Baixando arquivo: {csv_link}")
        print(f"URL: {file_url}")
        
        try:
            response = requests.get(file_url, stream=True)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            # Verificar e corrigir encoding
            try:
                df = pd.read_csv(save_path, sep=';', encoding='iso-8859-1')
                df.to_csv(save_path, sep=';', encoding='utf-8', index=False)
                print("Arquivo convertido para UTF-8")
            except Exception as e:
                print(f"Aviso: Não foi possível converter encoding - {e}")
            
            print(f"\nArquivo salvo em: {save_path}")
            return True
            
        except Exception as e:
            print(f"\nErro ao baixar o arquivo: {e}")
            if save_path.exists():
                os.remove(save_path)
            return False

    @staticmethod
    def download_demonstracoes_contabeis(years=2):
        """Download dos arquivos ZIP de demonstrações contábeis (3.1)"""
        print("\n=== BAIXANDO DEMONSTRAÇÕES CONTÁBEIS (ZIP) ===")
        response = requests.get(URLS['demonstracoes'])
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontrar links de diretórios dos anos
        year_links = []
        for a in soup.find_all('a'):
            href = a.get('href', '')
            if re.match(r'^20\d{2}/$', href):  # Pastas de ano (2023/, 2024/, etc.)
                full_url = urljoin(URLS['demonstracoes'], href)
                year_links.append((href.strip('/'), full_url))
        
        # Ordenar anos decrescente e pegar os mais recentes
        year_links.sort(reverse=True)
        selected_years = year_links[:years]
        
        if not selected_years:
            raise Exception("Nenhum ano encontrado no diretório de demonstrações")
        
        print(f"Anos selecionados: {[y[0] for y in selected_years]}")
        
        total_files = 0
        for year, year_url in selected_years:
            print(f"\nProcessando ano: {year}")
            
            # Obter lista de arquivos ZIP deste ano
            response = requests.get(year_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            zip_files = []
            for a in soup.find_all('a'):
                href = a.get('href', '')
                if href.endswith('.zip'):
                    full_url = urljoin(year_url, href)
                    zip_files.append((href, full_url))
            
            if not zip_files:
                print(f"Aviso: Nenhum arquivo ZIP encontrado para o ano {year}")
                continue
            
            # Criar subdiretório para o ano
            year_dir = DEMONSTRACOES_DIR / year
            os.makedirs(year_dir, exist_ok=True)
            
            # Baixar cada arquivo ZIP
            downloaded = 0
            for zip_file, file_url in tqdm(zip_files, desc=f"Baixando {year}"):
                save_path = year_dir / zip_file
                
                if save_path.exists():
                    tqdm.write(f"Arquivo já existe: {zip_file} - Pulando")
                    continue
                
                try:
                    response = requests.get(file_url, stream=True)
                    response.raise_for_status()
                    
                    with open(save_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    downloaded += 1
                except Exception as e:
                    tqdm.write(f"Erro ao baixar {zip_file}: {e}")
                    if save_path.exists():
                        os.remove(save_path)
            
            total_files += downloaded
            print(f"Download concluído para {downloaded}/{len(zip_files)} arquivos do ano {year}")
        
        print(f"\nTotal de arquivos baixados: {total_files}")
        print(f"Arquivos salvos em: {DEMONSTRACOES_DIR}")
        return total_files > 0

if __name__ == "__main__":
    downloader = DataDownloader()
    
    print("=== INÍCIO DO PROCESSO DE DOWNLOAD ===")
    
    # Baixar operadoras ativas (CSV)
    success_operadoras = downloader.download_latest_operadoras()
    
    # Baixar demonstrações contábeis (ZIP)
    success_demonstracoes = downloader.download_demonstracoes_contabeis(years=2)
    
    # Resumo final
    print("\n=== RESUMO FINAL ===")
    print(f"Operadoras ativas (CSV): {'Sucesso' if success_operadoras else 'Falha'}")
    print(f"Demonstrações contábeis (ZIP): {'Sucesso' if success_demonstracoes else 'Falha'}")
    
    if not (success_operadoras and success_demonstracoes):
        print("\nAVISO: Alguns downloads falharam. Verifique as mensagens de erro acima.")