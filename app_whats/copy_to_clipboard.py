from io import BytesIO
import win32clipboard
from PIL import Image
import os
import fitz


def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

def copiar_imagem_redimensionada(caminho_imagem, nova_largura):

  try:
    # Abre a imagem
    imagem = Image.open(caminho_imagem)

    # Calcula a nova altura, mantendo a proporção
    largura_original, altura_original = imagem.size
    nova_altura = int(altura_original * nova_largura / largura_original)

    # Redimensiona a imagem
    imagem_redimensionada = imagem.resize((nova_largura, nova_altura))

    # Converte para formato compatível com o clipboard (BMP)
    output = BytesIO()
    imagem_redimensionada.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]  # Remove o cabeçalho do arquivo BMP
    output.close()

    # Copia a imagem redimensionada para o clipboard
    send_to_clipboard(win32clipboard.CF_DIB, data)

  except Exception as e:
    print(f"Erro ao copiar a imagem: {e}")


def pdf_to_png(pdf_file_path):

    pdffile = pdf_file_path
    doc = fitz.open(pdffile)
    zoom = 4
    mat = fitz.Matrix(zoom, zoom)
    count = 0
    # Count variable is to get the number of pages in the pdf
    for p in doc:
        count += 1
    for i in range(count):
        val = os.path.join('auxiliar',f"modelo_{i+1}.png")
        page = doc.load_page(i)
        pix = page.get_pixmap(matrix=mat)
        pix.save(val)
    doc.close()





def main_copiar_imagem():
    
    pdf_file_path = r'auxiliar\Modelo Comunicado.pdf'
    pdf_to_png(pdf_file_path)
    
    caminho_imagem = r'auxiliar\modelo_1.png'
    nova_largura = 1500
    copiar_imagem_redimensionada(caminho_imagem, nova_largura)


