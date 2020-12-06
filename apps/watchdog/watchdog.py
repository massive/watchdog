from datetime import datetime

from appdaemon.plugins.hass.hassapi import Hass  # type: ignore
from typing import (
    TypedDict,
    List
)

Sensor = TypedDict('Sensor', {'entity_id': str, 'threshold': int}, total=False)

ALERT_SENSOR_NAME: str = 'binary_sensor.watchdog_alert'

class Watchdog(Hass):

    def initialize(self):
        check_interval: int = self.args['interval'] or 60
        sensors: List[Sensor] = self.args.get("sensors", None)
        threshold: int = self.args['threshold']

        self.log(f"Checking {len(sensors)} configured entities on {check_interval} seconds", level="DEBUG")

        self.run_every(self.run_periodically, "now", check_interval, sensors=sensors, threshold=threshold)
        self.set_state(ALERT_SENSOR_NAME, state="off",
                       attributes={"friendly_name": "Watchdog alert", "device_class": "problem"})

    async def run_periodically(self, kwargs) -> None:
        default_threshold: int = kwargs['threshold']
        sensors: List[Sensor] = kwargs['sensors']

        stale_sensors: List[Sensor] = []

        for sensor in sensors:
            entity_id: str = sensor['entity_id']
            threshold: int = sensor.get('threshold') or default_threshold

            self.log(
                f"Checking entity {entity_id}",
                level="DEBUG"
            )

            last_changed = await self.get_state(entity_id, attribute="last_changed")
            if last_changed is None:
                self.log(f"Could not find entity {entity_id}", level="WARNING")
                continue

            time_diff: float = datetime.now().timestamp() - self.convert_utc(last_changed).timestamp()

            self.log(f"Time difference {time_diff}", level="DEBUG")

            if time_diff > threshold:
                self.log(f"Entity {entity_id} exceeds time threshold {threshold}", level="INFO")
                await self.set_state(f"{entity_id}_age", state=last_changed)
                stale_sensors.append(sensor)

        if len(stale_sensors) > 0:
            alertable_entity_ids = [sensor['entity_id'] for sensor in stale_sensors]
            self.log(f"There are {len(stale_sensors)} stale sensors: {', '.join(alertable_entity_ids)}")
            await self.set_state(ALERT_SENSOR_NAME, state="on", attributes={"entities": alertable_entity_ids})
        else:
            self.log(f"No stale sensors", level="DEBUG")
            await self.set_state(ALERT_SENSOR_NAME, state="off", attributes={"entities": []})
