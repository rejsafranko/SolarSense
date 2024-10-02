import os
import ssl
import time
import json
import keras
import numpy
import cv2
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

from modules import CameraService, ImageProcessor, ModelService

load_dotenv()
MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = os.getenv("MQTT_PORT")
MQTT_TOPIC = os.getenv("MQTT_TOPIC")
ROOT_CA_PATH = os.getenv("ROOT_CA_PATH")
CERT_PATH = os.getenv("CERT_PATH")
KEY_PATH = os.getenv("KEY_PATH")
MODEL_PATH = os.getenv("MODEL_PATH")

payload = {"device_id": "Raspberry Pi Sigma"}


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to AWS IoT: {rc}")
        client.connected_flag = True  # Set flag
    else:
        print(f"Connection failed with status code: {rc}")


def on_publish(**kwargs) -> None:
    print("Message published.")


def publish_mqtt_message(client: mqtt.Client):
    """Publishes an MQTT message to trigger the AWS IoT notification."""
    if client.connected_flag:
        result = client.publish(MQTT_TOPIC, json.dumps(payload), qos=1)
        result.wait_for_publish()
        print(f"Published: {result.is_published()}")
    else:
        print("Client is not connected. Cannot publish.")

if __name__ == "__main__":
    camera_service = CameraService()
    model_service = ModelService(
        model_path=MODEL_PATH, image_processor=ImageProcessor()
    )
    # image = camera_service.image_processor.capture_image()
    # if image is not None:
    # prediction = model_service.run_inference(image)
    prediction = 1
    print(f"Prediction: {'dirty' if 1 else 'clean'}")
    if prediction == 1:
        mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        mqtt_client.tls_set(
            ca_certs=ROOT_CA_PATH,
            certfile=CERT_PATH,
            keyfile=KEY_PATH,
            tls_version=ssl.PROTOCOL_TLSv1_2,
        )

        mqtt_client.on_connect = on_connect
        mqtt_client.on_publish = on_publish
        mqtt_client.connect(MQTT_HOST, int(MQTT_PORT), keepalive=60)
        mqtt_client.loop_start()
        time.sleep(5)
        publish_mqtt_message(mqtt_client)
        time.sleep(20)
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
    else:
        print("Prediction was 0. No MQTT message sent.")
