from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import skeletonize
import hashlib

#exibir imagem em cada etapa (apagar dps)
def show_image(img, title=""):
    plt.imshow(img, cmap="gray")
    plt.title(title)
    plt.axis("off")  # Desativar os eixos
    plt.show()

#converter a imagem para escala de cinza
def escala_cinza(image):
    img = Image.open(image)
    img_gray = img.convert("L")
    #show_image(img_gray, "Escala cinza")
    return np.array(img_gray)

#Filtro para melhorar bordas(Gaussian)
def melhora_bordas(img):
    blur_img = cv2.GaussianBlur(img, (3, 3), 0)
    bordas = cv2.Canny(blur_img, threshold1=50, threshold2=150)
    #show_image(bordas, "Borda melhorada")
    return bordas


#Binarização
def binarizacao(bi_img):
    _, bi_img = cv2.threshold(bi_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #show_image(bi_img, "Binarização")
    return bi_img

#Afinamento(Esqueletização)
def afinamento(bi_img):
    #converte para valores binários (0 e 1)
    bi_img = bi_img / 255
    skeleton = skeletonize(bi_img).astype(np.uint8) * 255  #aplica finamento e converte devolta para 255 e 0 
    #show_image(skeleton, "Imagem afinamento")
    return skeleton

#Extração de minúcias
def extracao_minucia(afina_img):
    pontos_minu = ""
    
    #encontrar pontos de terminação e bifurcação
    for i in range(1, afina_img.shape[0] - 1):
        for j in range(1, afina_img.shape[1] - 1):
            if afina_img[i, j] == 255:  #verifica sefaz parte do esqueleto
                vizinhos = afina_img[i-1:i+2, j-1:j+2] // 255 #vizinhança
                #picels vizinhos
                conexao = np.sum(vizinhos) - 1
                
                #verifica ponto de terminação ou bifurcação
                if conexao == 1:  #terminação
                    pontos_minu += f"{i},{j}-T;"
                elif conexao == 3:  #bifurcação
                    pontos_minu += f"{i},{j}-B;"

    #gera a hash
    valor_hash = hashlib.sha256(pontos_minu.encode()).hexdigest()
    return valor_hash
    
def processamento_fingerprint(image):
    #image = "C:\\Users\\GuiJu\\workspace\\APS_BIOMETRIA\\projeto-biometria\\assets\\fingerprints\\biometria2.jpg"
    image_url = str(image)
    image_url.replace("/","\\")
    img_gray = escala_cinza(image_url)
    melhor_bordas = melhora_bordas(img_gray)
    binarizacao_img = binarizacao(melhor_bordas)
    afinamento_img = afinamento(binarizacao_img)
    hash = extracao_minucia(afinamento_img)
    return hash