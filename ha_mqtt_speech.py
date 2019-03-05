#ha_mqtt_speech:
#  topic: xSpeech
#  nickname: 
#  rules:
#    - name: entrance-light-up
#      words:
#        - bejárat
#        - kapcsold fel
#      platform: switch
#      service: turn_on
#      service_data: {"entity_id": "switch.bejarat_vilagitas"}
#      answer_topic: xiaomi/speak
#      answer: A bejárat előtt felkapcsoltam a világítást.
#    - name: entrance-light-up-2
#      words:
#        - bejárat
#        - sötét
#      platform: switch
#      service: turn_on
#      service_data: {"entity_id": "switch.bejarat_vilagitas"}
#      answer_topic: xiaomi/speak
#      answer: A bejárat előtt felkapcsoltam a világítást.
#    - name: entrance-light-down
#      words:
#        - bejárat
#        - kapcsold le
#      platform: switch
#      service: turn_off
#      service_data: {"entity_id": "switch.bejarat_vilagitas"}
#      answer_topic: xiaomi/speak
#      answer: A bejárat előtt lekapcsoltam a világítást.

import logging
import homeassistant.loader as loader

# The domain of your component. Should be equal to the name of your component.
DOMAIN = 'ha_mqtt_speech'

# List of component names (string) your component depends upon.
DEPENDENCIES = ['mqtt']
LOGGER = logging.getLogger(__name__)

CONF_TOPIC = 'topic'
CONF_RULES = 'rules'
CONF_NICKNAME = 'nickname'
DEFAULT_TOPIC = 'xSpeech'
DEFAULT_NICKNAME = ''

def setup(hass, config):
    LOGGER.info(DOMAIN + ' component is ready!')
    """Set up the Hello MQTT component."""
    mqtt = hass.components.mqtt
    topic = config[DOMAIN].get(CONF_TOPIC, DEFAULT_TOPIC)
    rules = config[DOMAIN].get(CONF_RULES, [])
    nickname = config[DOMAIN].get(CONF_NICKNAME, DEFAULT_NICKNAME)
    entity_id = 'ha_mqtt_speech.last_message'
    LOGGER.info(DOMAIN + ' rules: ')
    LOGGER.info(rules)
    
    # Listener to be called when we receive a message.
    def message_received(topic, payload, qos):
        """Handle new MQTT messages."""
        LOGGER.info(DOMAIN + ' message_received received data: ' + payload)
        for rule in rules:
            LOGGER.info(DOMAIN + ' rule name: ' + rule['name'])
            ok = False
            for word in rule['words']:
                if word.lower() in payload.lower():
                    ok = True
                else:
                    ok = False
                    break
            
            if ok and nickname is not None and len(nickname.strip()) > 0:
                if nickname.strip().lower() in payload.lower():
                    ok = True
                else:
                    ok = False
            
            if ok:
                LOGGER.info(DOMAIN + ' rule matched: ' + rule['name'])
                if rule['answer_topic'] is not None and len(rule['answer_topic']) > 0 and rule['answer'] is not None and len(rule['answer']) > 0:
                    LOGGER.info(DOMAIN + ' answer_topic: ' + rule['answer_topic'] + ', answer: ' + rule['answer'])
                    mqtt.publish(rule['answer_topic'], rule['answer'])
                else:
                    LOGGER.info(DOMAIN + ' answer_topic: ' + rule['answer_topic'] + ', answer: ' + rule['answer'] + '!')
                hass.services.call(rule['platform'], rule['service'], rule['service_data'], False)
                break
            else:
                LOGGER.info(DOMAIN + ' rule not matched: ' + rule['name'])

    # Subscribe our listener to a topic.
    mqtt.subscribe(topic, message_received)
    LOGGER.info(DOMAIN + ' subscribed topic: ' +topic)
    LOGGER.info(DOMAIN + ' nickname: ' +str(nickname))
    return True
