"""
Requests humidty and temperature data from a DHT22 sensor and inserts it into BigQuery.
"""

import os
import time
from datetime import datetime

import Adafruit_DHT
from google.cloud import bigquery


def _dht_data(sensor, sensor_id, sensor_pin):
    """
    Returns a tuple (humidity, temperature) from sensor.
    """
    dht_data = {}
    dht_data["sensor_id"] = sensor_id
    dht_data["requested_at"] = datetime.now()
    dht_data["humidity"], dht_data["temperature"] = Adafruit_DHT.read_retry(
        sensor, sensor_pin
    )
    return dht_data


def _gbq_setup(project_id, dataset_id, table_id):
    """
    Creates a BigQuery client.
    """
    client = bigquery.Client()
    dataset = bigquery.dataset.DatasetReference.from_string(
        f"{project_id}.{dataset_id}"
    )
    table = client.get_table(dataset.table(table_id))
    return client, table


def _gbq_insert(dht_data, client, table):
    """
    Inserts dht data into BigQuery.
    """
    errors = client.insert_rows(table, [dht_data])
    if errors:
        raise RuntimeError(errors)


def main():
    """
    Requests humidty and temperature data from a DHT22 sensor and inserts it into BigQuery.
    """
    sensor_id = int(os.environ.get("DHT_SENSOR_ID", 1))
    sensor_pin = int(os.environ["DHT_SENSOR_PIN"])
    gbq_insert = bool(os.environ.get("DHT_GBQ_INSERT", False))

    sensor = Adafruit_DHT.DHT22
    dht_data = _dht_data(sensor, sensor_id, sensor_pin)
    print(dht_data)

    if gbq_insert:
        print("Inserting into BigQuery.")
        project_id = os.environ["DHT_GBQ_PROJECT_ID"]
        dataset_id = os.environ["DHT_GBQ_DATASET_ID"]
        table_id = os.environ["DHT_GBQ_TABLE_ID"]
        _gbq_insert(dht_data, *_gbq_setup(project_id, dataset_id, table_id))
