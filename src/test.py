import os
import time
from classes.mqtt_client import MQTTClient
from loguru import logger

def main():
    try:
        image_path = os.path.join(os.path.dirname(__file__), 'assets', 'esp32s3_sample.jpg')
        with open(image_path, "rb") as image_file:
            byte_array = bytearray(image_file.read())
        logger.debug(len(byte_array))

        unacked_publish = set()
        client = MQTTClient(userdate=unacked_publish)
        client.start()

        msg_info = client.publish(topic='Test', message=byte_array)
        unacked_publish.add(msg_info.mid)

        # Wait for all message to be published
        while len(unacked_publish):
            time.sleep(0.1)

        # Due to race-condition described above, the following way to wait for all publish is safer
        msg_info.wait_for_publish()
        logger.debug(len(byte_array))

        client.stop()
    except Exception as err:
        logger.error(f"MQTT error: {err}")
        client.stop()

if __name__ == "__main__":
    main()
