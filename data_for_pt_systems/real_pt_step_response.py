import numpy as np
import pandas as pd
import os

def generate_real_ptn_response(n, K=1.0, time_end=50, num_points=500):
    """
    Funktion zur Berechnung und Speicherung der Sprungantwort eines PT_n-Systems.
    
    Parameters:
    - n: die Ordnung des Systems (1, 2, 3, ...)
    - K: Verstärkungsfaktor (Standard: 1.0)
    - time_end: Endzeit für die Simulation (Standard: 50)
    - num_points: Anzahl der Zeitpunkte für die Simulation (Standard: 500)
    """
    
    # Definiere Zeitkonstanten T1, T2, ..., Tn
    time_constants = np.linspace(1.0, 1.0 * n, n)

    # Erstelle einen Zeitvektor
    time = np.linspace(0, time_end, num_points)

    # Berechne die Sprungantwort
    response = np.ones_like(time)
    for i in range(n):
        response *= (1 - np.exp(-time / time_constants[i]))

    # Verstärkung
    response *= K

    # Füge Rauschen hinzu
    np.random.seed(42)
    noise = np.random.normal(0, 0.05, len(time))
    response_with_noise = response + noise

    # Step Response (bleibt konstant bei 1)
    step_response = np.ones_like(time)
    step_response[0] = 0

    # DataFrame erzeugen
    df = pd.DataFrame({
        'Time': time,
        'Response': response_with_noise,
        'Step Response': step_response
    })

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = f'real_pt{n}_response.csv'
    file_path = os.path.join(script_dir, file_name)
    df.to_csv(file_path, index=False)



max_ptn_order = 10
# Dateien für PT1 bis PT10 erzeugen
for order in range(1, max_ptn_order+1):
    generate_real_ptn_response(order)
