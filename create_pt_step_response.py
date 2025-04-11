import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Parameter für das PT2-System
K = 0.5  # Verstärkungsfaktor
T1 = 5.0  # Zeitkonstante 1
T2 = 10.0  # Zeitkonstante 2

# Parameter für das PT3-System
T3 = 15.0  # Zeitkonstante 3

# Parameter für das PT4-System
T4 = 20.0  # Zeitkonstante 4

# Erstellen eines Zeitvektors
time = np.linspace(0, 10, 500)

# PT1-System (Sprungantwort)
response_pt1 = K * (1 - np.exp(-time / T1))

# PT2-System (Sprungantwort)
response_pt2 = K * (1 - np.exp(-time / T1)) * (1 - np.exp(-time / T2))

# PT3-System (Sprungantwort)
response_pt3 = K * (1 - np.exp(-time / T1)) * (1 - np.exp(-time / T2)) * (1 - np.exp(-time / T3))

# PT4-System (Sprungantwort)
response_pt4 = K * (1 - np.exp(-time / T1)) * (1 - np.exp(-time / T2)) * (1 - np.exp(-time / T3)) * (1 - np.exp(-time / T4))

# Hinzufügen von Rauschen zu allen Antworten
np.random.seed(42)  # für Reproduzierbarkeit
noise = np.random.normal(0, 0.05, len(time))  # Rauschen mit geringer Amplitude

response_pt1_with_noise = response_pt1 + noise
response_pt2_with_noise = response_pt2 + noise
response_pt3_with_noise = response_pt3 + noise
response_pt4_with_noise = response_pt4 + noise

# Step Response bleibt konstant bei 1
step_response = np.ones_like(time)

# Erstellen von DataFrames
df_pt1 = pd.DataFrame({
    'Time': time,
    'Response': response_pt1_with_noise,
    'Step Response': step_response
})
df_pt2 = pd.DataFrame({
    'Time': time,
    'Response': response_pt2_with_noise,
    'Step Response': step_response
})

df_pt3 = pd.DataFrame({
    'Time': time,
    'Response': response_pt3_with_noise,
    'Step Response': step_response
})

df_pt4 = pd.DataFrame({
    'Time': time,
    'Response': response_pt4_with_noise,
    'Step Response': step_response
})

# Speichern der Daten als CSV
df_pt1.to_csv('real_pt1_response.csv', index=False)
df_pt2.to_csv('real_pt2_response.csv', index=False)
df_pt3.to_csv('real_pt3_response.csv', index=False)
df_pt4.to_csv('real_pt4_response.csv', index=False)
