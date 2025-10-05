from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import json

app = Flask(__name__)
CORS(app)

class AnalizadorEstadistico:
    def __init__(self):
        self.datos = None
    
    def cargar_datos(self, datos_lista):
        """Carga datos desde una lista"""
        self.datos = pd.DataFrame(datos_lista, columns=['Valores'])
        return {"mensaje": "Datos cargados exitosamente", "cantidad": len(datos_lista)}
    
    def medidas_tendencia_central(self):
        """Calcula medidas de tendencia central"""
        if self.datos is None:
            return {"error": "No hay datos cargados"}
        
        valores = self.datos['Valores']
        
        resultado = {
            "media": float(np.mean(valores)),
            "mediana": float(np.median(valores)),
            "moda": float(stats.mode(valores).mode[0]),
            "conteo_moda": int(stats.mode(valores).count[0])
        }
        return resultado
    
    def medidas_dispersion(self):
        """Calcula medidas de dispersión"""
        if self.datos is None:
            return {"error": "No hay datos cargados"}
        
        valores = self.datos['Valores']
        
        resultado = {
            "varianza": float(np.var(valores, ddof=1)),
            "desviacion_estandar": float(np.std(valores, ddof=1)),
            "rango": float(np.max(valores) - np.min(valores)),
            "rango_intercuartil": float(np.percentile(valores, 75) - np.percentile(valores, 25)),
            "minimo": float(np.min(valores)),
            "maximo": float(np.max(valores))
        }
        return resultado
    
    def generar_grafico(self, tipo_grafico):
        """Genera diferentes tipos de gráficos"""
        if self.datos is None:
            return {"error": "No hay datos cargados"}
        
        valores = self.datos['Valores']
        plt.figure(figsize=(10, 6))
        
        if tipo_grafico == 'histograma':
            plt.hist(valores, bins='auto', alpha=0.7, color='skyblue', edgecolor='black')
            plt.title('Histograma')
            plt.xlabel('Valores')
            plt.ylabel('Frecuencia')
        
        elif tipo_grafico == 'boxplot':
            plt.boxplot(valores)
            plt.title('Diagrama de Caja')
            plt.ylabel('Valores')
        
        elif tipo_grafico == 'dispersion':
            plt.scatter(range(len(valores)), valores, alpha=0.7)
            plt.title('Gráfico de Dispersión')
            plt.xlabel('Índice')
            plt.ylabel('Valores')
        
        elif tipo_grafico == 'violin':
            sns.violinplot(y=valores)
            plt.title('Diagrama de Violín')
        
        elif tipo_grafico == 'qq':
            stats.probplot(valores, dist="norm", plot=plt)
            plt.title('Gráfico Q-Q')
        
        plt.grid(alpha=0.75)
        
        # Convertir gráfico a base64
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        plt.close()
        
        return base64.b64encode(img.getvalue()).decode()

# Instancia global del analizador
analizador = AnalizadorEstadistico()

@app.route('/api/cargar-datos', methods=['POST'])
def cargar_datos():
    try:
        datos = request.json.get('datos', [])
        if not datos:
            return jsonify({"error": "No se proporcionaron datos"}), 400
        
        resultado = analizador.cargar_datos(datos)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tendencia-central', methods=['GET'])
def tendencia_central():
    try:
        resultado = analizador.medidas_tendencia_central()
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/dispersion', methods=['GET'])
def dispersion():
    try:
        resultado = analizador.medidas_dispersion()
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/grafico/<tipo>', methods=['GET'])
def generar_grafico(tipo):
    try:
        tipos_permitidos = ['histograma', 'boxplot', 'dispersion', 'violin', 'qq']
        if tipo not in tipos_permitidos:
            return jsonify({"error": "Tipo de gráfico no válido"}), 400
        
        imagen_base64 = analizador.generar_grafico(tipo)
        return jsonify({"imagen": f"data:image/png;base64,{imagen_base64}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/estadisticas-completas', methods=['GET'])
def estadisticas_completas():
    try:
        tendencia = analizador.medidas_tendencia_central()
        dispersion = analizador.medidas_dispersion()
        
        if 'error' in tendencia or 'error' in dispersion:
            return jsonify({"error": "No hay datos cargados"}), 400
        
        resultado = {**tendencia, **dispersion}
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)