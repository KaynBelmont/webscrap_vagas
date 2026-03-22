# =============================================================================
# parser.py
# Responsável por extrair os dados das vagas a partir do HTML bruto.
# Utiliza BeautifulSoup para navegar e coletar as informações de cada vaga.
# =============================================================================

from bs4 import BeautifulSoup


def extrair_vagas(html: str) -> list[dict]:
    """
    Recebe o HTML da página e retorna uma lista de dicionários,
    onde cada dicionário representa uma vaga com seus dados.

    Args:
        html (str): Conteúdo HTML bruto da página

    Returns:
        list[dict]: Lista de vagas extraídas
    """

    # Inicializa o BeautifulSoup com o parser lxml (mais rápido)
    soup = BeautifulSoup(html, "lxml")

    # Encontra todos os cards de vaga na página
    # Cada vaga fica dentro de um <li> com a classe "vaga"
    cards = soup.find_all("li", class_="vaga")

    print(f"[parser] {len(cards)} vagas encontradas na página")

    vagas = []

    for card in cards:

        # --- Título ---
        # O atributo 'title' da tag <a> já traz o texto limpo, sem a tag <mark>
        titulo_tag = card.find("a", class_="link-detalhes-vaga")
        titulo = titulo_tag["title"].strip() if titulo_tag else "N/A"

        # --- Empresa ---
        empresa_tag = card.find("span", class_="emprVaga")
        empresa = empresa_tag.get_text(strip=True) if empresa_tag else "N/A"

        # --- Localidade ---
        local_tag = card.find("span", class_="vaga-local")
        local = local_tag.get_text(separator=" ", strip=True) if local_tag else "N/A"
        # Remove o ícone invisível que vem junto com o texto
        local = " ".join(local.split()[1:]) if local and local != "N/A" else "N/A"

        # --- Nível ---
        nivel_tag = card.find("span", class_="nivelVaga")
        nivel = nivel_tag.get_text(strip=True) if nivel_tag else "N/A"

        # --- Link da vaga ---
        link = "https://www.vagas.com.br" + titulo_tag["href"] if titulo_tag else "N/A"

        # Monta o dicionário com os dados da vaga
        vagas.append({
            "titulo":  titulo,
            "empresa": empresa,
            "local":   local,
            "nivel":   nivel,
            "link":    link,
        })

    return vagas


# -----------------------------------------------------------------------------
# Teste rápido: integra com o scraper para ver os dados extraídos
# python src/parser.py
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    from scraper import buscar_pagina

    html = buscar_pagina("python")
    vagas = extrair_vagas(html)

    # Exibe as 3 primeiras vagas para conferir
    for i, vaga in enumerate(vagas[:3], start=1):
        print(f"\n--- Vaga {i} ---")
        for chave, valor in vaga.items():
            print(f"  {chave}: {valor}")