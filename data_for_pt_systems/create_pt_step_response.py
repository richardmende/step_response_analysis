import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def generate_ptn_response(n, K=1.0, time_end=50, num_points=500):
    """
    Funktion zur Berechnung und Speicherung der Sprungantwort eines PT_n-Systems.
    
    Parameters:
    - n: die Ordnung des Systems (2, 3, 4, ...)
    - K: Verstärkungsfaktor (Standard: 1.0)
    - time_end: Endzeit für die Simulation (Standard: 10)
    - num_points: Anzahl der Zeitpunkte für die Simulation (Standard: 500)
    """
    
    # Definiere Zeitkonstanten T1, T2, ..., Tn
    time_constants = np.linspace(1.0, 1.0 * n, n)  # Einfaches Beispiel für Zeitkonstanten: 1, 2, ..., n

    # Erstelle einen Zeitvektor
    time = np.linspace(0, time_end, num_points)

    # Berechne die Sprungantwort für ein PT_n-System
    response = np.ones_like(time)
    
    for i in range(n):
        response *= (1 - np.exp(-time / time_constants[i]))

    # Füge Rauschen hinzu
    np.random.seed(42)  # für Reproduzierbarkeit
    noise = np.random.normal(0, 0.05, len(time))  # Rauschen mit geringer Amplitude
    response_with_noise = response + noise

    # Step Response bleibt konstant bei 1
    step_response = np.ones_like(time)

    # Erstelle DataFrame
    df = pd.DataFrame({
        'Time': time,
        'Response': response_with_noise,
        'Step Response': step_response
    })

    # Speichern der CSV-Datei
    file_name = f'real_pt{n}_response.csv'
    df.to_csv(file_name, index=False)



generate_ptn_response(1)
generate_ptn_response(2)
generate_ptn_response(3)
generate_ptn_response(4)
generate_ptn_response(5)
generate_ptn_response(6)
generate_ptn_response(7)
generate_ptn_response(8)
generate_ptn_response(9)
generate_ptn_response(10)
