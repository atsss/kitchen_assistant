import threading
import typing as ty

from loguru import logger
import socket
import json

import paho.mqtt.client as paho
from paho import mqtt

MQTT_BROKER_URL = ''
MQTT_BROKER_PORT = ''
DEVICE_MQTT_BROKER_USERNAME = ''
DEVICE_MQTT_BROKER_PASSWORD = ''

class MQTTClient(object):
    def __init__(self,
                 address: str = MQTT_BROKER_URL,
                 port: int = MQTT_BROKER_PORT,
                 username: str = DEVICE_MQTT_BROKER_USERNAME,
                 password: str = DEVICE_MQTT_BROKER_PASSWORD,
                 device_uuid: str = DEVICE_UUID
                 ) -> None:

        # Connection
        self._address = address
        self._port = port
        self._username = username
        self._password = password

        # Client
        self._client: ty.Optional['mqtt.Client'] = None
        self._client_id: str = device_uuid
        self._connected: bool = False

        # Notifications
        self._configuration_changed: 'threading.Condition' = threading.Condition()

    def _connect(self) -> ty.Tuple[bool, ty.Dict]:
        try:
            if self._client is None:
                self._client = paho.Client(client_id=self._client_id, protocol=paho.MQTTv5, clean_session=False)
                self._client.username_pw_set(self._username, self._password)
                self._client.on_connect = self._on_connect
                self._client.on_disconnect = self._on_disconnect
                self._client.on_subscribe = self._on_subscribe
                self._client.on_message = self._on_message
                rc = self._client.connect(self._address, self._port, keepalive=60)
            else:
                self._client.reconnect()
            return True, {}
        except (ConnectionRefusedError, socket.gaierror) as err:
            logger.warning(f"Can't connect device to message broker: {err}")
            return False, {'msg': err}
        except Exception as err:
            logger.error(f"Error connecting device to message broker: {err}")
            return False, {'msg': err}

    def _disconnect(self) -> None:
        if self._client is not None:
            self._client.disconnect()

    def _on_connect(self, client, userdata, flags, rc, properties=None):
        # This will be called once the client connects
        if rc == 0:
            logger.success(f"Device message client connected with result code '{str(rc)}'")
            # Subscribe here!
            # TODO: Do we need to subscribe every time we connect?
            client.subscribe(self.TOPIC_CONFIGURE, qos=1)
            self._connected = True
        else:
            logger.warning(f"Device message client tried to connect with result code '{str(rc)}'")

    def _on_disconnect(self, client, userdata, rc, properties=None):
        self._connected = False

    def _on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        logger.debug(f"Device subscribed: mid:{str(mid)}, QoS:{'.'.join([str(s1) for s1 in granted_qos])}")

    def _on_message(self, client, userdata, msg):
        try:
            # Assume payload is json
            data = json.loads(msg.payload)
            logger.success(f"Message received [{msg.topic}]: {data}")

        except json.decoder.JSONDecodeError:
            data = msg.payload.decode("utf-8")
            logger.warning(f"Message received [{msg.topic}] in unexpected format (not json) : {data}")
        except Exception as err:
            logger.error(f"Error receiving message [{msg.topic}]: {err}")

    def start(self) -> None:
        succ, resp = self._connect()
        if succ and self._client is not None:
            self._client.loop_start()
            logger.debug(f"Started App MQTT Client")
        else:
            logger.error(f"Can't start MQTT client")

    def stop(self) -> None:
        if self._client is not None:
            self._client.disconnect()
            self._client.stop_loop()
            logger.debug(f"Stopped App MQTT Client")

    def publish(self, message: str, topic: str) -> None:
        logger.debug(f"Will publish {message[:20]} to {topic}")
        self._client.publish(topic, payload="hot", qos=0)
        logger.debug(f"Published {message[:20]} to {topic}")
