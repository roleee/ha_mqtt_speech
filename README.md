# HA custom component magyar hangvezérléshez

Automate android app beállítása a screenshotok alapján.
A ha_mqtt_speech.py fájlt a HA-n belül a custom_components mappában kell elhelyezni.

<pre>
configuration.yaml:
ha_mqtt_speech:
  topic: # MQTT topik elnevezése
  nickname: # Ha van beállítva, pl. Alexandra, akkor ezt is keresi a HA a szavakkal együtt.
  rules: # Szabályok
    - name:  # Szabály elnevezése
      words: # ezeket a szavakat keresi a HA az MQTT-üzenetben
      platform: # Szolgáltatás első része, amit hívunk egyezés esetén
      service:  # Szolgáltatás második része, amit hívunk egyezés esetén
      service_data: # Entitás
</pre> 

Ha a nick "Alexandra" és a beállított szavak: "bejárat" és "kapcsold fel", akkor bármilyen sorrendben kombinálhatóak az utasítás végrehajtásához:
- Alexandra, kérlek kapcsold fel a bejáratnál a világítást, mert nem látok semmit, olyan sötét van!
- Kapcsold fel a lámpát a bejárat előtt Alexandra, kérlek szépen!
- stb.