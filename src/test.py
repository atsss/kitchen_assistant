import os
from classes.mqtt_client import MQTTClient
from loguru import logger

def main():
    try:
        image_path = os.path.join(os.path.dirname(__file__), 'assets', 'esp32s3_sample.jpg')
        with open(image_path, "rb") as image_file:
            byte_array = bytearray(image_file.read())
        logger.debug(len(byte_array))

        client = MQTTClient()
        client.start()
        client.publish(topic='Test', message=byte_array)
        client.stop()
    except Exception as err:
        logger.error(f"MQTT error: {err}")
        client.stop()

if __name__ == "__main__":
    main()
