# downscale-to-png-othophoto
This present code receives a directory with some orthophotos.tif and translate it into orthophotos.png with a downscale of 4096x4096 without lose the original shape.

## Requirements
- You just need to run ```pip install -r requirements.txt``` and the pip will install all necessary requirements to run the source code.
- The main directory must follow this struct:
  ***
       main_directory/
          ---------ortho_tif/
                  ---------orthophoto_1.tif
                  ---------orthophoto_2.tif
                  ---------orthophoto_3.tif
                  ---------orthophoto_4.tif
  ***

## How to use 
To use this code run the cmd:```pyhton compressor.py main_directory/path```.

Segue abaixo uma documentação consolidada em Português explicando como resolver o erro de carregamento do `libvips-42.dll` ao usar **pyvips** no Windows. Você pode incluir este conteúdo no seu README para ajudar outras pessoas que encontrem o mesmo problema.

---

# Resolvendo o Erro de Carregamento de `libvips-42.dll` no Windows

Se você está vendo um erro do tipo:

```
OSError: cannot load library 'libvips-42.dll': error 0x7e
```

ou

```
ModuleNotFoundError: No module named '_libvips'
```

significa que o **pyvips** não está encontrando a biblioteca nativa **libvips** (e suas dependências) no seu sistema Windows.

Abaixo estão as etapas para corrigir o problema:

## 1. Verifique se o Python é 64 bits ou 32 bits

1. Abra o terminal e execute:
   ```powershell
   python -c "import platform; print(platform.architecture())"
   ```
2. Se retornar algo como `('64bit', 'WindowsPE')`, seu Python é 64 bits. Caso apareça `32bit`, você deve baixar a versão de 32 bits do libvips.


## 2. Baixe o Pacote **Completo** do libvips

Os binários (DLLs) necessários para o Windows não estão no repositório principal do libvips, mas sim no repositório [libvips/build-win64-mxe](https://github.com/libvips/build-win64-mxe/releases).

1. Acesse a página de [releases do build-win64-mxe](https://github.com/libvips/build-win64-mxe/releases).  
2. Localize a versão compatível com o seu Python (64 ou 32 bits). Para 64 bits, o arquivo normalmente se chama algo como:
   ```
   vips-dev-w64-all-8.xx.xx.zip
   ```
3. Faça download desse ZIP (por exemplo, `vips-dev-w64-all-8.16.0.zip`).

> **Importante**: Baixe o pacote que contenha `-all-` no nome para garantir que todas as dependências estejam incluídas.


## 3. Extraia os Arquivos

1. Extraia o ZIP em uma pasta, por exemplo:
   ```
   C:\vips
   ```
2. Dentro dessa pasta, você verá várias subpastas, incluindo a **`bin`**.


## 4. Adicione `C:\vips\bin` ao PATH do Windows

Para que o Python encontre os arquivos DLL, é necessário adicionar a pasta `bin` do libvips à variável de ambiente **PATH**:

1. Clique em **Iniciar** → digite “**Variáveis de Ambiente**”.  
2. Selecione “**Editar as variáveis de ambiente do sistema**”.  
3. Na janela “Propriedades do Sistema”, clique em “**Variáveis de Ambiente...**”.  
4. Em “Variáveis do sistema”, localize “**Path**” e clique em **Editar**.  
5. Adicione uma nova entrada apontando para:
   ```
   C:\vips\bin
   ```
6. Salve e feche todas as janelas.

---

## 5. Abra um Novo Terminal

As alterações no PATH só têm efeito em **novas** instâncias do terminal (CMD/PowerShell). Portanto, feche qualquer terminal aberto e abra outro.

## 6. Instale e Teste o pyvips

### Passo a Passo

1. **Entre** no seu ambiente virtual (pipenv, venv etc.).
2. Se ainda não instalou o pyvips, faça:
   ```bash
   pip install pyvips
   ```
3. Verifique a instalação:
   ```bash
   python -c "import pyvips; print(pyvips.version())"
   ```
4. Se tudo estiver correto, aparecerá a versão do libvips (por exemplo, `8.16.0`).

---

## 7. Remova DLLs Duplicadas (se necessário)

Se você **copiou manualmente** algum arquivo `libvips-42.dll` para outras pastas (como `C:\Users\<seu-usuario>\AppData\Local\Programs\Python\Python311\DLLs`), remova-o para evitar conflitos de versão. O Python pode tentar carregar esse DLL solto e ignorar o `bin` oficial do libvips, causando erros.

---

## Solução de Problemas

- **Ainda dá erro 0x7e**  
  Verifique se realmente adicionou `C:\vips\bin` (onde está o `libvips-42.dll` e **outras** DLLs) ao PATH, e não apenas `C:\vips`.  
- **Python 32 bits vs. libvips 64 bits**  
  Se houver incompatibilidade de arquitetura (por exemplo, Python 32 bits e libvips 64 bits), você continuará vendo falhas. Garanta que ambos sejam 64 bits (ou ambos 32 bits).  
- **O pyvips não encontra algumas dependências**  
  O pacote `vips-dev-w64-all` já inclui a maioria das bibliotecas comuns (libjpeg, libtiff, libwebp etc.). Se você precisar de plugins específicos, verifique se estão incluídos ou instale a versão correspondente.

---

### Referências

- [Repositório principal do libvips](https://github.com/libvips/libvips)  
- [Repositório de builds para Windows](https://github.com/libvips/build-win64-mxe/releases)  
- [Documentação do pyvips no PyPI](https://pypi.org/project/pyvips/)  

---

Pronto! Seguindo esses passos, o `pyvips` deve funcionar corretamente no Windows, sem o erro “**cannot load library 'libvips-42.dll'**”.