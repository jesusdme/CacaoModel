from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

# Cargar el modelo desde el archivo .pkl
rf_model = joblib.load("cacao_rf_model.pkl")

# Crear la instancia de FastAPI
app = FastAPI()

# Definir el modelo de datos para la solicitud
class PredictionRequest(BaseModel):
    Area_Sembrada: float
    Area_Cosechada: float
    Produccion: float

@app.post("/predict")
def predict(request: PredictionRequest):
    # Extraer los datos de la solicitud
    input_data = pd.DataFrame([[request.Area_Sembrada, request.Area_Cosechada, request.Produccion]], 
                              columns=['Area_Sembrada', 'Area_Cosechada', 'Produccion'])

    # Realizar la predicción
    try:
        prediction = rf_model.predict(input_data)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"Rendimiento_Predicho": prediction}

# Endpoint de prueba para la raíz
@app.get("/")
def read_root():
    return {"message": "Hello World!"}

# Si ejecutas el archivo directamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
