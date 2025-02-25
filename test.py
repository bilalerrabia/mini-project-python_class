import numpy as np
import matplotlib.pyplot as plt

# --- 1️⃣ Paramètres de Simulation ---
dt = 1  # Intervalle de temps (secondes)
t_end = 2000  # Durée totale de simulation (secondes)
t = np.arange(0, t_end, dt)  # Vecteur temps

# --- 2️⃣ 🔥 Température Extérieure ---
T_ext_base = 25 + 10 * np.sin(2 * np.pi * (t / (t_end / 2)))  # Oscillation jour/nuit
T_ext_noise = 2 * np.random.randn(len(t))  # Variations aléatoires
T_ext = T_ext_base + T_ext_noise  # Température finale

# --- 3️⃣ 💧 Humidité Extérieure ---
humidite_base = 50 + 20 * np.sin(2 * np.pi * (t / (t_end / 2)))  # Variation entre 30% et 70%
humidite_noise = 5 * np.random.randn(len(t))  # Petites variations aléatoires
humidite = np.clip(humidite_base + humidite_noise, 30, 70)  # Limitée entre 30% et 70%

# --- 4️⃣ ❄ Température de l'Habitacle ---
T_habitacle = np.zeros(len(t))
T_habitacle[0] = 40  # Température initiale élevée

# --- 5️⃣ 🔋 Batterie Haute Tension (HV) ---
capacite_batterie = 13.6  # Capacité max en kWh
batterie = np.zeros(len(t))
batterie[0] = capacite_batterie  # Batterie pleine au début
conso_clim_max = 1.5  # Consommation max en kW
P_echauffement = 0.02  # Chauffage naturel
P_max_refroidissement = 0.05  # Puissance max de refroidissement

# --- 6️⃣ 🚗 Vitesse de la Voiture ---
# Calcul de la vitesse à chaque instant (entre 0 et 100 km/h)
vitesse = 50 + 50 * np.sin(2 * np.pi * (t / (t_end / 2)))  # Variation périodique de la vitesse

# --- 7️⃣ 🔄 Simulation ---
puissance_clim = np.zeros(len(t))
energie_consommee_kWh = 0

for i in range(1, len(t)):
    # Calcul de la vitesse actuelle (scalaire)
    vitesse_actuelle = vitesse[i - 1]
    
    # Facteur de vitesse : augmente avec la vitesse (jusqu'à 1.5x à 100 km/h)
    facteur_vitesse = 1 + 0.001 * vitesse_actuelle
    
    # Effet du chauffage naturel
    dT_chaleur = P_echauffement * (T_ext[i - 1] - T_habitacle[i - 1])
    
    # Impact de l'humidité : plus l'humidité est élevée, plus le refroidissement est difficile
    facteur_humidite = 1 + (humidite[i - 1] - 50) / 100  # Influence entre 30% et 70%
    
    # Activation automatique de la climatisation
    if T_habitacle[i - 1] > 26 and batterie[i - 1] > 0.1:
        puissance_clim[i] = 1  # Pleine puissance
    elif T_habitacle[i - 1] < 22 or batterie[i - 1] <= 0.1:
        puissance_clim[i] = 0  # Clim éteinte
    else:
        puissance_clim[i] = 0.5  # Demi puissance
    
    # Refroidissement ajusté par la vitesse et l'humidité
    dT_froid = -puissance_clim[i] * P_max_refroidissement * (T_habitacle[i - 1] - 22) / (facteur_humidite * facteur_vitesse)
    
    # Mise à jour de la température de l'habitacle
    T_habitacle[i] = T_habitacle[i - 1] + dT_chaleur + dT_froid
    
    # Consommation de la batterie
    conso_batterie = puissance_clim[i] * conso_clim_max * (dt / 3600)  # en kWh
    batterie[i] = max(batterie[i - 1] - conso_batterie, 0)
    energie_consommee_kWh += conso_batterie

# --- 8️⃣ 📈 Affichage des Résultats ---
plt.figure(figsize=(12, 12))

# Graphique 1 : Évolution de la température
plt.subplot(4, 1, 1)
plt.plot(t, T_ext, 'r--', label="Température Extérieure")
plt.plot(t, T_habitacle, 'b', label="Température Habitacle")
plt.xlabel('Temps (s)')
plt.ylabel('Température (°C)')
plt.title('Évolution de la Température')
plt.legend()
plt.grid()

# Graphique 2 : Activation de la climatisation
plt.subplot(4, 1, 2)
plt.plot(t, puissance_clim, 'g', label="Puissance Climatisation")
plt.xlabel('Temps (s)')
plt.ylabel('Puissance')
plt.title('Activation de la Climatisation')
plt.legend()
plt.grid()

# Graphique 3 : Énergie restante dans la batterie
plt.subplot(4, 1, 3)
plt.plot(t, batterie, 'm', label="Énergie Batterie (kWh)")
plt.xlabel('Temps (s)')
plt.ylabel('Énergie (kWh)')
plt.title('Évolution de la Batterie HV')
plt.legend()
plt.grid()

# Graphique 4 : Vitesse de la voiture
plt.subplot(4, 1, 4)
plt.plot(t, vitesse, 'c', label="Vitesse (km/h)")
plt.xlabel('Temps (s)')
plt.ylabel('Vitesse (km/h)')
plt.title('Évolution de la Vitesse')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()

# Affichage de l'énergie consommée
print(f"Énergie totale consommée: {energie_consommee_kWh:.2f} kWh")
print(f"Pourcentage d'énergie utilisée: {(energie_consommee_kWh / capacite_batterie) * 100:.2f}% de la batterie")