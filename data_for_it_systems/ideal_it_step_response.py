import numpy as np
import pandas as pd
import os



def generate_ideal_itn_response(n, K=1.0, time_end=50, num_points=500):
    """
    Funktion zur Berechnung und Speicherung der Sprungantwort eines IT_n-Systems.
    
    Parameters:
    - n: die Ordnung des IT_n-Systems (1, 2, 3, ...)
    - K: Verstärkungsfaktor (Standard: 1.0)
    - time_end: Endzeit der Simulation (Standard: 50)
    - num_points: Anzahl der Zeitpunkte (Standard: 500)
    """
    
    # Zeitkonstanten T1 bis Tn (z.B. linear verteilt)
    time_constants = np.linspace(1.0, 1.0 * n, n)

    # Zeitachse
    time = np.linspace(0, time_end, num_points)

    # Sprungantwort berechnen: y(t) = t * Produkt(1 - exp(-t/Ti))
    response = time.copy()
    for T in time_constants:
        response *= (1 - np.exp(-time / T))

    # Step input (bleibt konstant bei 1)
    step_response = np.ones_like(time)

    # DataFrame erstellen
    df = pd.DataFrame({
        'Time': time,
        'Response': response,
        'Step Response': step_response
    })

    # Speicherort im selben Verzeichnis wie dieses Skript
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = f'ideal_it{n}_response.csv'
    file_path = os.path.join(script_dir, file_name)
    df.to_csv(file_path, index=False)



max_itn_order = 10

for order in range(1, max_itn_order + 1):
    generate_ideal_itn_response(order)
