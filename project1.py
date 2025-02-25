import numpy as np
import matplotlib.pyplot as plt

# Paramètres de Simulation
dt = 1  # Intervalle de temps (s)
t_end = 2000  # Durée totale de simulation (s)
t = np.arange(0, t_end, dt)

# Données réelles de la Toyota C-HR
battery_capacity_kWh = 13.8  # Capacité batterie hybride (kWh)
energy_consumption_kW = 5  # Consommation du climatiseur en kW (valeur estimée)

# Simulation de la température extérieure
T_ext_base = 25 + 10 * np.sin(2 * np.pi * (t / (t_end / 2)))  # Oscillation jour/nuit
T_ext_noise = 2 * np.random.randn(len(t))  # Variations aléatoires
T_ext = T_ext_base + T_ext_noise  # Température finale

# Température initiale de l’habitacle
T_habitacle = np.zeros(len(t))
T_habitacle[0] = 40  # Habitacle chaud au départ

# Modèle de Climatisation
P_echauffement = 0.02  # Chauffage naturel (°C/s)
mode = "Normal"  # Mode de climatisation sélectionné
vitesse = 50  # Vitesse du véhicule en km/h

# Définition des modes de climatisation
modes = {
    "Eco": 0.03,
    "Normal": 0.05,
    "Max": 0.08
}
P_max_refroidissement = modes[mode]

# Effet de la vitesse sur le refroidissement (ventilation naturelle)
P_ventilation = 0.001 * vitesse  # Plus la voiture roule vite, plus l'effet de ventilation est grand

# Effet du rayonnement solaire
I_solar = np.maximum(0, np.sin(2 * np.pi * (t / (t_end / 2))))  # Intensité du soleil (0 à 1)
P_solaire = 0.03 * I_solar  # Effet du soleil sur l’habitacle

# Simulation de la température de l’habitacle
puissance_clim = np.zeros(len(t))
energie_consommée_kWh = 0

for i in range(1, len(t)):
    # Réchauffement dû à la température extérieure
    dT_chaleur = P_echauffement * (T_ext[i - 1] - T_habitacle[i - 1])
    
    # Activation automatique de la climatisation
    if T_habitacle[i - 1] > 26:
        puissance_clim[i] = 1  # Climatisation activée
    elif T_habitacle[i - 1] < 22:
        puissance_clim[i] = 0  # Clim éteinte
    else:
        puissance_clim[i] = 0.5  # Clim à moitié
    
    # Refroidissement du à la climatisation
    dT_froid = -puissance_clim[i] * P_max_refroidissement * (T_habitacle[i - 1] - 22)
    
    # Mise à jour de la température de l’habitacle
    T_habitacle[i] = T_habitacle[i - 1] + dT_chaleur + dT_froid - P_ventilation + P_solaire[i]
    
    # Calcul de l’énergie consommée
    energie_consommée_kWh += puissance_clim[i] * energy_consumption_kW * (dt / 3600)  # kWh

# Calcul de l'énergie gaspillée en pourcentage
efficiency = (energie_consommée_kWh / battery_capacity_kWh) * 100

# Affichage des Résultats
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(t, T_ext, 'r--', label="Température Extérieure")
plt.plot(t, T_habitacle, 'b', label="Température Habitacle")
plt.xlabel("Temps (s)")
plt.ylabel("Température (°C)")
plt.title("Évolution de la Température")
plt.legend()
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(t, puissance_clim, 'g', label="Puissance Climatisation")
plt.xlabel("Temps (s)")
plt.ylabel("Puissance")
plt.title("Activation de la Climatisation")
plt.legend()
plt.grid()

plt.show()

print(f"Énergie totale consommée: {energie_consommée_kWh:.2f} kWh")
print(f"Pourcentage d’énergie gaspillée: {efficiency:.2f}% de la batterie")
