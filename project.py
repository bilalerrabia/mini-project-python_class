import numpy as np
import matplotlib.pyplot as plt

# --- 1️⃣ Paramètres de Simulation ---
dt = 1  # Intervalle de temps (s)
t_end = 2000  # Durée totale de simulation (s)
t = np.arange(0, t_end, dt)

# --- 2️⃣ 🔥 Température Extérieure ---
T_ext_base = 25 + 10 * np.sin(2 * np.pi * (t / (t_end / 2)))  # Oscillation jour/nuit
T_ext_noise = 2 * np.random.randn(len(t))  # Variations aléatoires
T_ext = T_ext_base + T_ext_noise  # Température finale

# --- 3️⃣ 💧 Humidité Extérieure ---
humidite_base = 50 + 20 * np.sin(2 * np.pi * (t / (t_end / 2)))  # Humidité varie entre 30% et 70%
humidite_noise = 5 * np.random.randn(len(t))  # Petites variations aléatoires
humidite = np.clip(humidite_base + humidite_noise, 30, 70)  # Limité entre 30% et 70%

# --- 4️⃣ ❄ Température de l'Habitacle ---
T_habitacle = np.zeros(len(t))
T_habitacle[0] = 40  # Température initiale élevée

# --- 5️⃣ 🔋 Batterie Haute Tension (HV) ---
capacite_batterie = 13.6  # Capacité max en kWh
batterie = np.zeros(len(t))
batterie[0] = capacite_batterie  # Batterie pleine au début

# --- 6️⃣ Modes de Climatisation ---
mode_clim = "Normal"  # Choix entre "Eco", "Normal", "Max"

mode_factors = {
    "Eco": 0.5,
    "Normal": 1.0,
    "Max": 1.5
}

conso_clim_max = 1.5  # Consommation max en kW
P_echauffement = 0.02  # Chauffage naturel
P_max_refroidissement = 0.05 * mode_factors[mode_clim]  # Puissance max de refroidissement selon mode

# --- 7️⃣ Simulation ---
puissance_clim = np.zeros(len(t))
energie_consommee_kWh = 0

for i in range(1, len(t)):
    dT_chaleur = P_echauffement * (T_ext[i - 1] - T_habitacle[i - 1])
    facteur_humidite = 1 + (humidite[i] - 50) / 100
    
    erreur_temperature = T_habitacle[i - 1] - 22  # Écart par rapport à la température cible
    
    if erreur_temperature > 4 and batterie[i - 1] > 1.5:
        puissance_clim[i] = min(1, erreur_temperature / 10)  # Modulation progressive
    elif erreur_temperature < 2 or batterie[i - 1] <= 1.5:
        puissance_clim[i] = 0  # Clim éteinte
    
    dT_froid = -puissance_clim[i] * P_max_refroidissement * erreur_temperature / facteur_humidite
    
    T_habitacle[i] = T_habitacle[i - 1] + dT_chaleur + dT_froid
    
    conso_batterie = puissance_clim[i] * conso_clim_max * (dt / 3600)
    batterie[i] = max(batterie[i - 1] - conso_batterie, 0)
    energie_consommee_kWh += conso_batterie

# --- 8️⃣ Affichage des Résultats ---
plt.figure(figsize=(12, 10))

plt.subplot(3, 1, 1)
plt.plot(t, T_ext, 'r--', label="Température Extérieure")
plt.plot(t, T_habitacle, 'b', label="Température Habitacle")
plt.xlabel('Temps (s)')
plt.ylabel('Température (°C)')
plt.title('Évolution de la Température')
plt.legend()
plt.grid()

plt.subplot(3, 1, 2)
plt.plot(t, puissance_clim, 'g', label="Puissance Climatisation")
plt.xlabel('Temps (s)')
plt.ylabel('Puissance')
plt.title('Activation de la Climatisation')
plt.legend()
plt.grid()

plt.subplot(3, 1, 3)
plt.plot(t, batterie, 'm', label="Énergie Batterie (kWh)")
plt.xlabel('Temps (s)')
plt.ylabel('Énergie (kWh)')
plt.title('Évolution de la Batterie HV')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()

print(f"Mode de climatisation: {mode_clim}")
print(f"Énergie totale consommée: {energie_consommee_kWh:.2f} kWh")
print(f"Pourcentage d'énergie utilisée: {(energie_consommee_kWh / capacite_batterie) * 100:.2f}% de la batterie")
