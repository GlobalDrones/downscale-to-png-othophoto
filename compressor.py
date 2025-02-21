import os
import sys
import pyvips

def calcula_dimensoes(width, height, image_size):
    if width >= height:
        scale = image_size / width
        new_width = image_size
        new_height = int(height * scale)
    else:
        scale = image_size / height
        new_height = image_size
        new_width = int(width * scale)
    return new_width, new_height, scale

def salva_imagem_png(tif_path, final_image):
    nome_arquivo = os.path.basename(tif_path)
    nome_arquivo_png = os.path.splitext(nome_arquivo)[0] + '.png'
    pasta_saida = os.path.join(os.path.dirname(os.path.dirname(tif_path)), 'ortho_png')
    os.makedirs(pasta_saida, exist_ok=True)
    caminho_saida = os.path.join(pasta_saida, nome_arquivo_png)
    
    try:
        final_image.write_to_file(caminho_saida)
        print(f'Imagem {nome_arquivo} convertida e salva como {nome_arquivo_png}')
    except Exception as e:
        print(f'Erro ao salvar a imagem {nome_arquivo} como PNG: {e}')

def comprime_imagem(tif_path, image_size):
    try:
        # Abre a imagem TIF com acesso sequencial para evitar carregar tudo na RAM
        image = pyvips.Image.new_from_file(tif_path, access='sequential')
    except Exception as e:
        print(f'Erro ao abrir a imagem {tif_path}: {e}')
        return

    width = image.width
    height = image.height
    new_width, new_height, scale = calcula_dimensoes(width, height, image_size)
    
    try:
        resized = image.resize(scale)
    except Exception as e:
        print(f'Erro ao redimensionar a imagem {tif_path}: {e}')
        return

    # Garante que a imagem tenha 4 bandas (RGBA)
    if resized.bands == 3:
        resized = resized.bandjoin(255)
    
    try:
        final_image = pyvips.Image.black(3072, 3072, bands=4)
        
        left = (image_size - new_width) // 2
        top = (image_size - new_height) // 2
        
        final_image = final_image.insert(resized, left, top)
    except Exception as e:
        print(f'Erro ao compor a imagem final para {tif_path}: {e}')
        return

    salva_imagem_png(tif_path, final_image)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Uso: python compressor.py <image_size> <path/da/pasta_mae>')
        sys.exit(1)

    image_size = int(sys.argv[1])
    if image_size%2 != 0:
        print('Warning: o tamanho da imagem deve ser multiplo de 2.')
    pasta_mae = sys.argv[2]


    if not os.path.isdir(pasta_mae):
        print(f'Erro: a pasta {pasta_mae} não existe.')
        sys.exit(1)

    pasta_tif = os.path.join(pasta_mae, 'ortho_tif')
    if not os.path.isdir(pasta_tif):
        print(f'Erro: a pasta {pasta_tif} não existe.')
        sys.exit(1)

    arquivos_tif = [os.path.join(pasta_tif, arquivo) for arquivo in os.listdir(pasta_tif) if arquivo.lower().endswith('.tif')]

    if not arquivos_tif:
        print('Nenhum arquivo TIF encontrado para processar.')
        sys.exit(0)

    for arquivo_tif in arquivos_tif:
        try:
            comprime_imagem(arquivo_tif, image_size)
        except Exception as e:
            print(f'Erro ao processar {arquivo_tif}: {e}')
