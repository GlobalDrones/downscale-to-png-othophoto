import os
import sys
from PIL import Image

Image.MAX_IMAGE_PIXELS = None


def calcula_dimensoes(imagem_tif):
    largura, altura = imagem_tif.size


    if largura >= altura:
        fator_escala = 4096 / largura
        nova_largura = 4096
        nova_altura = int(altura * fator_escala)
    else:
        fator_escala = 4096 / altura
        nova_altura = 4096
        nova_largura = int(largura * fator_escala)

    return nova_largura, nova_altura

def salva_imagem_png(tif_path, imagem_final):
    nome_arquivo = os.path.basename(tif_path)
    nome_arquivo_png = os.path.splitext(nome_arquivo)[0] + '.png'
    pasta_saida = os.path.join(os.path.dirname(os.path.dirname(tif_path)), 'ortho_png')
    os.makedirs(pasta_saida, exist_ok=True)
    caminho_saida = os.path.join(pasta_saida, nome_arquivo_png)
    imagem_final.save(caminho_saida, format='PNG')

    print(f'Imagem {nome_arquivo} convertida e salva como {nome_arquivo_png}')

def comprime_imagem(tif_path):
    imagem_tif = Image.open(tif_path)

    nova_largura, nova_altura = calcula_dimensoes(imagem_tif)
    
    imagem_redimensionada = imagem_tif.resize((nova_largura, nova_altura), Image.LANCZOS)

    imagem_final = Image.new('RGBA', (4096, 4096), (0, 0, 0, 0))
    posicao = ((4096 - nova_largura) // 2, (4096 - nova_altura) // 2)
    imagem_final.paste(imagem_redimensionada, posicao)

    salva_imagem_png(tif_path, imagem_final)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Use: python compressor.py path/da/pasta_mae')
        sys.exit(1)

    pasta_mae = sys.argv[1]

    pasta_tif = os.path.join(pasta_mae, 'ortho_tif')
    arquivos_tif = [os.path.join(pasta_tif, arquivo) for arquivo in os.listdir(pasta_tif) if arquivo.endswith('.tif')]

    for arquivo_tif in arquivos_tif:
        try:
            comprime_imagem(arquivo_tif)
        except Exception as e:
            print(f'Erro ao processar {arquivo_tif}: {e}')
