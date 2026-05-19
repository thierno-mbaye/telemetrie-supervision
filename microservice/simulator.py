import paho.mqtt.client as mqtt
import json
import time
import random
import math

BROKER = "mosquitto"
PORT = 1883

CAPTEURS = [
    {"device_id": "capteur-01", "location": "salle-serveurs"},
    {"device_id": "capteur-02", "location": "datacenter"},
    {"device_id": "capteur-03", "location": "atelier-iot"},
]

def simuler_temperature(t, base=22.0):
    """Simule une température avec variation sinusoïdale + bruit"""
    return round(base + 5 * math.sin(t / 30) + random.uniform(-1, 1), 2)

def simuler_pression(t, base=1013.0):
    """Simule une pression atmosphérique"""
    return round(base + 2 * math.sin(t / 60) + random.uniform(-0.5, 0.5), 2)

def simuler_vibration():
    """Simule une vibration avec pics occasionnels"""
    if random.random() < 0.05:  # 5% de chance de pic
        return round(random.uniform(8.0, 15.0), 2)
    return round(random.uniform(0.1, 2.0), 2)

def simuler_batterie(device_id, batteries):
    """Simule une décharge progressive de batterie"""
    if device_id not in batteries:
        batteries[device_id] = random.uniform(60, 100)
    batteries[device_id] = max(0, batteries[device_id] - random.uniform(0.01, 0.05))
    return round(batteries[device_id], 2)

def main():
    client = mqtt.Client()
    
    print("Connexion au broker MQTT...")
    while True:
        try:
            client.connect(BROKER, PORT, 60)
            print("Connecté à Mosquitto !")
            break
        except Exception as e:
            print(f"Erreur connexion: {e}, retry dans 5s...")
            time.sleep(5)

    batteries = {}
    t = 0

    print("Démarrage simulation capteurs IoT...")
    while True:
        for capteur in CAPTEURS:
            payload = {
                "device_id": capteur["device_id"],
                "location": capteur["location"],
                "temperature": simuler_temperature(t),
                "pression": simuler_pression(t),
                "vibration": simuler_vibration(),
                "battery": simuler_batterie(capteur["device_id"], batteries),
                "timestamp": time.time()
            }

            topic = f"sensors/{capteur['device_id']}/telemetry"
            client.publish(topic, json.dumps(payload))
            print(f"[{capteur['device_id']}] {payload}")

        t += 1
        time.sleep(10)

if __name__ == "__main__":
    main()
