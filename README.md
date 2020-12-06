# Watchdog

_A HACS AppDaemon addon for getting notified on stale sensors [HACS](https://github.com/custom-components/hacs)._

## Installation

This app is best installed using [HACS](https://github.com/custom-components/hacs), so that you can easily track and download updates.

Alternatively, you can download the `watchdog` directory from inside the `apps` directory here to your local `apps` directory, then add the configuration to enable the `watchdog` module.

## App configuration

```yaml
watchdog:
  module: 'watchdog'
  class: 'Watchdog'
  interval: 60
  threshold: 3600
  sensors:
    - entity_id: sensor.bedroom_sensor_temperature
    - entity_id: sensor.fridge_sensor_temperature
      threshold: 7200
```

## Options

key | optional | type | default | description
-- | -- | -- | -- | --
`module` | False | string | | The module name of the app.
`class` | False | string | | The name of the Class.
`interval` | True | integer | 60 | Default checking interval in seconds
`sensors` | False | list of entities |  | The list of entities to check for staleness

## Sensors
key | optional | type | default | description
-- | -- | -- | -- | --
`entity_id` | False | string | | Entity id
`threshold` | True | integer | default threshold | Staleness threshold for the given entity
