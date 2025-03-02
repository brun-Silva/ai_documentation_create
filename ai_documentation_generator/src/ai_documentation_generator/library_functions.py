import os


def listar_arquivos(diretorio, pastas_ignorar=None):
    if pastas_ignorar is None:
        pastas_ignorar = []

    lista_arquivos = []

    for raiz, diretorios, arquivos in os.walk(diretorio, topdown=True):
        # Remove pastas ignoradas da lista de diretórios a serem percorridos
        diretorios[:] = [d for d in diretorios if d not in pastas_ignorar]

        for arquivo in arquivos:
            caminho_completo = os.path.join(raiz, arquivo)
            lista_arquivos.append(caminho_completo)
    all_files = ""

    for i in lista_arquivos:
        all_files += f"\n{str(i)}"  # Adiciona cada caminho em uma nova linha

    print("ALL FILES")
    print(all_files)
    return [all_files,lista_arquivos]


import os


def extrair_conteudo_arquivo(caminho, extensoes_ignorar=None, encoding='utf-8'):
    """
    Extrai conteúdo de um arquivo se sua extensão não estiver na lista de ignorados

    Args:
        caminho (str): Caminho completo do arquivo
        extensoes_ignorar (list): Lista de extensões para ignorar (ex: ['.db', '.tmp'])
        encoding (str): Codificação para leitura do arquivo (padrão: utf-8)

    Returns:
        str: Conteúdo do arquivo ou None se for ignorado/não texto
    """
    if extensoes_ignorar is None:
        extensoes_ignorar = []

    # Verifica se é arquivo e extensão permitida
    if not os.path.isfile(caminho):
        return None

    # Extrai extensão e normaliza para comparação
    extensao = os.path.splitext(caminho)[1].lower()
    if extensao in [ext.lower() for ext in extensoes_ignorar]:
        return None

    try:
        with open(caminho, 'r', encoding=encoding, errors='ignore') as arquivo:
            return arquivo.read()
    except UnicodeDecodeError:
        # Arquivos binários serão ignorados
        return None
    except Exception as e:
        print(f"Erro ao ler {caminho}: {str(e)}")
        return None



def append_to_resume(text, filename="RESUME.txt"):
    with open(filename, "a", encoding="utf-8") as file:
        file.write(text + "\n___________________________________________________________________________________")
