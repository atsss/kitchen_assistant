from classes.mqtt_client import MQTTClient
from loguru import logger

def main():
    try:
        client = MQTTClient()
        client.start()
        client.publish(topic='Test', message='Test')
        client.stop()
    except Exception as err:
        logger.error(f"MQTT error: {err}")
        client.stop()

if __name__ == "__main__":
    main()
