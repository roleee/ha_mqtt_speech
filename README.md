# HA custom component magyar hangvezérléshez

Android appok:

Automate: https://play.google.com/store/apps/details?id=com.llamalab.automate

MQTT Client: https://play.google.com/store/apps/details?id=in.dc297.mqttclpro

Google szövegfelolvasó: https://play.google.com/store/apps/details?id=com.google.android.tts

Automate beállítása a screenshotok alapján.
A ha_mqtt_speech.py fájlt a HA-n belül a custom_components mappában kell elhelyezni.

configuration.yaml:
<pre>
ha_mqtt_speech:
  topic: # MQTT topik elnevezése
  nickname: # Ha van beállítva, pl. Alexandra, akkor ezt is keresi a HA a szavakkal együtt.
  rules: # Szabályok
    - name:  # Szabály elnevezése
      words: # ezeket a szavakat keresi a HA az MQTT-üzenetben
      platform: # Szolgáltatás első része, amit hívunk egyezés esetén
      service:  # Szolgáltatás második része, amit hívunk egyezés esetén
      service_data: # Entitás
      answer_topic: # MQTT-topik, ahova küld egy üzenetet, ha végzett az utasítással
      answer: # MQTT-üzenet, amit felolvas az Automate
</pre> 

Példa:
<pre>
ha_mqtt_speech:
  topic: xSpeech
  nickname: Alexandra
  rules:
    - name: entrance-light-up
      words:
        - bejárat
        - kapcsold fel
      platform: switch
      service: turn_on
      service_data: {"entity_id": "switch.bejarat_vilagitas"}
      answer_topic: xiaomi/speak
      answer: A bejárat előtt felkapcsoltam a világítást.
</pre>

Ha a nick "Alexandra" és a beállított szavak: "bejárat" és "kapcsold fel", akkor bármilyen sorrendben kombinálhatóak az utasítás végrehajtásához:
- Alexandra, kérlek kapcsold fel a bejáratnál a világítást, mert nem látok semmit, olyan sötét van!
- Kapcsold fel a lámpát a bejárat előtt Alexandra, kérlek szépen!
- stb.

Hibakereséshez praktikus a configuration.yaml-ba:
<pre>
logger:
  default: warning
  logs:
    custom_components: info
</pre>
