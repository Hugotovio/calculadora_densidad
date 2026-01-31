from flask import Flask, request, jsonify
from flask_cors import CORS   # 👈 AÑADIDO

app = Flask(__name__)
CORS(app)   # 👈 AÑADIDO (habilita CORS para todo)

# Tabla 1: factores de conversión (°F → factor)
factores = {
    70: 0.917, 71: 1.01, 72: 1.102, 73: 1.195, 74: 1.288,
    75: 1.38, 76: 1.473, 77: 1.567, 78: 1.66, 79: 1.753,
    80: 1.847, 81: 1.94, 82: 2.034, 83: 2.128, 84: 2.222,
    85: 2.316, 86: 2.411, 87: 2.505, 88: 2.599, 89: 2.694,
    90: 2.789, 91: 2.884, 92: 2.979, 93: 3.074, 94: 3.169,
    95: 3.265, 96: 3.36, 97: 3.456, 98: 3.552, 99: 3.648,
    100: 3.748,
}

# Tabla 2: API observado → densidad (kg/gal)
tabla_api = {
    40.0: 3.12, 40.1: 3.118, 40.2: 3.117, 40.3: 3.115, 40.4: 3.113,
    40.5: 3.111, 40.6: 3.109, 40.7: 3.107, 40.8: 3.106, 40.9: 3.104,
    41.0: 3.102, 41.1: 3.1, 41.2: 3.098, 41.3: 3.097, 41.4: 3.095,
    41.5: 3.093, 41.6: 3.091, 41.7: 3.09, 41.8: 3.088, 41.9: 3.086,
    42.0: 3.084, 42.1: 3.082, 42.2: 3.081, 42.3: 3.079, 42.4: 3.077,
    42.5: 3.075, 42.6: 3.074, 42.7: 3.072, 42.8: 3.07, 42.9: 3.068,
    43.0: 3.067, 43.1: 3.065, 43.2: 3.063, 43.3: 3.061, 43.4: 3.06,
    43.5: 3.058, 43.6: 3.056, 43.7: 3.054, 43.8: 3.053, 43.9: 3.051,
    44.0: 3.049, 44.1: 3.047, 44.2: 3.046, 44.3: 3.044, 44.4: 3.042,
    44.5: 3.04, 44.6: 3.039, 44.7: 3.037, 44.8: 3.035, 44.9: 3.033,
    45.0: 3.032, 45.1: 3.03, 45.2: 3.028, 45.3: 3.027, 45.4: 3.025,
    45.5: 3.023, 45.6: 3.022, 45.7: 3.02, 45.8: 3.018, 45.9: 3.016,
    46.0: 3.015, 46.1: 3.013, 46.2: 3.011, 46.3: 3.01, 46.4: 3.008,
    46.5: 3.006, 46.6: 3.005, 46.7: 3.003, 46.8: 3.001, 46.9: 2.999,
    47.0: 2.998, 47.1: 2.996, 47.2: 2.994, 47.3: 2.993, 47.4: 2.991,
    47.5: 2.989, 47.6: 2.988, 47.7: 2.986, 47.8: 2.984, 47.9: 2.983,
    48.0: 2.981, 48.1: 2.979, 48.2: 2.978, 48.3: 2.976, 48.4: 2.974,
    48.5: 2.973, 48.6: 2.971, 48.7: 2.97, 48.8: 2.968, 48.9: 2.966,
    49.0: 2.965, 49.1: 2.963, 49.2: 2.961, 49.3: 2.96, 49.4: 2.958,
    49.5: 2.956, 49.6: 2.955, 49.7: 2.953, 49.8: 2.952, 49.9: 2.95,
    50.0: 2.948, 50.1: 2.947, 50.2: 2.945, 50.3: 2.943, 50.4: 2.942,
    50.5: 2.94, 50.6: 2.939, 50.7: 2.937, 50.8: 2.935, 50.9: 2.934,
    51.0: 2.932,
}

def truncar_1_decimal(valor: float) -> float:
    return int(valor * 10) / 10

@app.route("/calcular-densidad", methods=["POST"])
def calcular_densidad():
    data = request.get_json()

    if not data or "temperatura" not in data or "api60" not in data:
        return jsonify({"error": "Debe enviar temperatura y api60"}), 400

    try:
        temperatura = float(str(data["temperatura"]).replace(",", "."))
        api60 = float(str(data["api60"]).replace(",", "."))
    except ValueError:
        return jsonify({"error": "Valores numéricos inválidos"}), 400

    factor = factores.get(round(temperatura))
    if not factor:
        return jsonify({"error": "Temperatura fuera de rango (70–100 °F)"}), 400

    api_observado = truncar_1_decimal(api60 + factor)
    densidad = tabla_api.get(api_observado)

    if not densidad:
        return jsonify({"error": f"No existe densidad para API {api_observado}"}), 404

    return jsonify({
        "temperatura_F": temperatura,
        "api_60F": api60,
        "factor_conversion": factor,
        "api_observado": api_observado,
        "densidad_kg_gal": densidad
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)