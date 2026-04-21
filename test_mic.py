import sounddevice as sd

print("--- Liste des périphériques audio ---")
print(sd.query_devices())
print("\n--- Périphérique par défaut ---")
print(sd.default.device)