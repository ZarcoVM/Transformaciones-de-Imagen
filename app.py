from flask import Flask, render_template, request, send_file
from PIL import Image
import numpy as np
import io

app = Flask(__name__)

# Cargar la imagen predeterminada
def cargar_imagen_predeterminada():
    return Image.open('static/lambo.jpg')

# Función para redimensionar la imagen
def redimensionar_imagen(image, tamaño=(800, 600)):
    return image.resize(tamaño, Image.ANTIALIAS)

# Función para aplicar transformación usando matriz de cizallado
def aplicar_cizallado(image):
    matriz_cizallado = [1, 0.5, 0,
                        0.5, 1, 0]
    return aplicar_transformacion_matriz(image, matriz_cizallado)

# Función para aplicar transformación usando matriz de traslación
def aplicar_traslacion(image):
    matriz_traslacion = [1, 0, 50,
                          0, 1, 50]
    return aplicar_transformacion_matriz(image, matriz_traslacion)

# Función para aplicar transformación usando matriz de rotación
def aplicar_rotacion(image):
    angulo = np.radians(45)
    matriz_rotacion = [np.cos(angulo), -np.sin(angulo), 0,
                       np.sin(angulo), np.cos(angulo), 0]
    return aplicar_transformacion_matriz(image, matriz_rotacion)

# Función para aplicar transformación usando matriz de escalamiento
def aplicar_escalamiento(image):
    matriz_escalamiento = [1.5, 0, 0,
                           0, 1.5, 0]
    return aplicar_transformacion_matriz(image, matriz_escalamiento)

# Función para aplicar la transformación usando la matriz dada
def aplicar_transformacion_matriz(image, matriz):
    ancho, alto = image.size
    imagen_transformada = image.transform((ancho, alto), Image.AFFINE, data=matriz, resample=Image.BICUBIC)
    return imagen_transformada

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transformar', methods=['POST'])
def transformar():
    transformacion = request.form.get('transformacion')

    # Cargar la imagen predeterminada
    image = cargar_imagen_predeterminada()

    # Redimensionar la imagen
    image = redimensionar_imagen(image, tamaño=(400, 300))

    # Aplicar la transformación seleccionada
    if transformacion == 'cizallado':
        image = aplicar_cizallado(image)
    elif transformacion == 'traslacion':
        image = aplicar_traslacion(image)
    elif transformacion == 'rotacion':
        image = aplicar_rotacion(image)
    elif transformacion == 'escalamiento':
        image = aplicar_escalamiento(image)

    # Guardar la imagen transformada en un buffer
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
