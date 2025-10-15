from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
# Es esencial para usar sesiones (para guardar el puntaje y la pregunta)
app.secret_key = 'tu_clave_secreta_aqui'

# --- Lógica del Juego ---
def generar_pregunta(nivel):
    """Genera una pregunta de suma basada en el nivel."""
    if nivel == 'basico':
        limite = 10
    elif nivel == 'intermedio':
        limite = 50
    else: # dificil
        limite = 100

    num1 = random.randint(1, limite)
    num2 = random.randint(1, limite)
    operacion = "+" # En este ejemplo, solo usaremos la suma.
    
    pregunta_str = f"{num1} {operacion} {num2}"
    respuesta_correcta = num1 + num2
    
    return pregunta_str, respuesta_correcta, nivel

# --- Rutas Web ---

@app.route('/')
def inicio():
    """Página de inicio: muestra el menú principal y el puntaje."""
    # Inicializar el puntaje si no existe en la sesión
    if 'puntaje' not in session:
        session['puntaje'] = 0
    return render_template('inicio.html', puntaje=session['puntaje'])

@app.route('/nivel/<string:nivel>')
def jugar(nivel):
    """Muestra una pregunta según el nivel seleccionado."""
    
    # 1. Generar la pregunta y guardar la respuesta correcta en la sesión
    pregunta_str, respuesta_correcta, nivel_actual = generar_pregunta(nivel)
    
    session['respuesta_correcta'] = respuesta_correcta
    session['nivel_actual'] = nivel_actual
    
    return render_template('jugar.html', pregunta=pregunta_str, nivel=nivel_actual)

@app.route('/verificar', methods=['POST'])
def verificar():
    """Verifica la respuesta del niño y actualiza el puntaje."""
    
    # Obtener la respuesta del formulario (frontend)
    respuesta_nino = request.form.get('respuesta')
    
    # Obtener la respuesta correcta de la sesión
    respuesta_correcta = session.get('respuesta_correcta')
    nivel_actual = session.get('nivel_actual')
    
    mensaje = ""
    es_correcto = False

    try:
        if int(respuesta_nino) == respuesta_correcta:
            session['puntaje'] += 1
            mensaje = "¡Correcto! 🎉"
            es_correcto = True
        else:
            mensaje = f"¡Incorrecto! La respuesta era {respuesta_correcta} 🙁"
    except (ValueError, TypeError):
        mensaje = "Por favor, introduce un número válido."

    # Redirigir a una página de resultado que luego te envíe al inicio o a una nueva pregunta
    return render_template('resultado.html', mensaje=mensaje, es_correcto=es_correcto, nivel=nivel_actual)

# --- Ejecutar la aplicación ---
if __name__ == '__main__':
    # Para ejecutar en Pydroid 3, el host debe ser '0.0.0.0'
    app.run(host='0.0.0.0', port=5000, debug=True)
