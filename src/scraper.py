# =============================================================================
# scraper.py
# Responsável por realizar a requisição HTTP ao site Vagas.com.br
# e retornar o conteúdo HTML bruto da página de resultados.
# =============================================================================

import requests

# Headers para simular um navegador real.
# Sem isso, o site pode bloquear a requisição por identificar que é um bot.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def buscar_pagina(termo: str, pagina: int = 1) -> str:
    """
    Faz a requisição HTTP e retorna o HTML da página de resultados.

    Args:
        termo (str): Termo de busca (ex: 'python', 'data-analyst')
        pagina (int): Número da página de resultados (padrão: 1)

    Returns:
        str: Conteúdo HTML da página
    """

    # Monta a URL de busca com o termo e o número da página
    url = f"https://www.vagas.com.br/vagas-de-{termo}?pagina={pagina}"

    print(f"[scraper] Buscando: {url}")

    # Realiza a requisição com timeout de 10 segundos
    resposta = requests.get(url, headers=HEADERS, timeout=10)

    # Lança um erro automaticamente se o status não for 200 (OK)
    resposta.raise_for_status()

    print(f"[scraper] Status: {resposta.status_code} — OK!")

    return resposta.text


# -----------------------------------------------------------------------------
# Teste rápido: rode este arquivo diretamente para ver se está funcionando
# python src/scraper.py
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    html = buscar_pagina("python")
    print(f"[scraper] HTML recebido: {len(html)} caracteres")