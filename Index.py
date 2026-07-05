import os
import urllib.request
import urllib.parse
import re

def clonar_e_vincular():
    # Pasta oficial: /sdcard/Download/clones
    pasta_raiz = "/sdcard/Download/clones"
    os.makedirs(pasta_raiz, exist_ok=True)
    
    url = input("🔗 Cole a URL: ").strip()
    if not url.startswith("http"): url = "https://" + url
    
    # Cria uma subpasta para o site específico (ex: /clones/www_site_com)
    nome_site = urllib.parse.urlparse(url).netloc.replace(".", "_")
    caminho_final = os.path.join(pasta_raiz, nome_site)
    os.makedirs(caminho_final, exist_ok=True)
    
    print(f"\n📂 Salvando em: {caminho_final}")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    
    # 1. Baixa o HTML
    with urllib.request.urlopen(req) as r:
        html = r.read().decode('utf-8', errors='ignore')
    
    # 2. Acha todos os links de arquivos (src e href)
    # Procura por: src="link" ou href="link" onde o link termina com extensão de arquivo
    padrao = r'(?:src|href)=["\'](.*?\.(?:png|jpg|jpeg|gif|css|js|svg|ico|mp4|mp3))["\']'
    recursos = re.findall(padrao, html)
    
    print(f"🔍 Encontrados {len(set(recursos))} recursos. Baixando...")
    
    # 3. Baixa os recursos e substitui no HTML
    for link in set(recursos):
        try:
            full_url = urllib.parse.urljoin(url, link)
            nome_arq = os.path.basename(urllib.parse.urlparse(link).path)
            if not nome_arq: nome_arq = "arquivo"
            
            # Baixa o arquivo
            urllib.request.urlretrieve(full_url, os.path.join(caminho_final, nome_arq))
            
            # Substitui o caminho no HTML pelo nome do arquivo local
            # Assim o HTML sabe que o arquivo está ali na mesma pasta
            html = html.replace(link, nome_arq)
            print(f"✅ Baixado e vinculado: {nome_arq}")
        except:
            print(f"⚠️ Erro ao baixar: {link}")

    # 4. Salva o HTML corrigido
    with open(os.path.join(caminho_final, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
        
    print(f"\n✅ CONCLUÍDO!")
    print(f"Pasta: {caminho_final}")
    print("Vá em 'Gerenciador de Arquivos' > 'Download' > 'clones' > '" + nome_site + "'")

if __name__ == "__main__":
    clonar_e_vincular()
          
