import os
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile

# 1.1. Acessar o site e extrair links dos Anexos I e II
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Dicionário para armazenar os links dos Anexos I e II
anexos = {
    "Anexo I": None,  # Guardará ('Anexo_I.pdf', url)
    "Anexo II": None  # Guardará ('Anexo_II.pdf', url)
}

# Verificar cada link para ambos os Anexos
for link in soup.find_all('a'):
    link_text = link.text.strip()
    href = link.get('href', '')
    
    # Se for Anexo I e ainda não foi capturado
    if 'Anexo I' in link_text and anexos["Anexo I"] is None:
        anexos["Anexo I"] = ('Anexo_I.pdf', href)
    
    # Se for Anexo II e ainda não foi capturado
    if 'Anexo II' in link_text and anexos["Anexo II"] is None:
        anexos["Anexo II"] = ('Anexo_II.pdf', href)

# 1.2. Download dos PDFs
os.makedirs('anexos', exist_ok=True)
for nome_arquivo, dados in anexos.items():
    if dados is not None:
        nome, url_pdf = dados
        try:
            pdf_response = requests.get(url_pdf)
            with open(f'anexos/{nome}', 'wb') as f:
                f.write(pdf_response.content)
            print(f"Download concluído: {nome}")
        except Exception as e:
            print(f"Erro ao baixar {nome}: {e}")
    else:
        print(f"Atenção: {nome_arquivo} não encontrado no site!")

# 1.3. Compactar os arquivos em um ZIP
arquivos_baixados = [dados for dados in anexos.values() if dados is not None]
if arquivos_baixados:
    with ZipFile('Anexos_ANS.zip', 'w') as zipf:
        for nome, _ in arquivos_baixados:
            zipf.write(f'anexos/{nome}', arcname=nome)
    print("Compactação concluída: Anexos_ANS.zip")
else:
    print("Nenhum Anexo foi baixado. Verifique o site.")