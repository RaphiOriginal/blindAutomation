[![Build Status](https://travis-ci.org/RaphiOriginal/blindAutomation.svg?branch=master)](https://travis-ci.org/RaphiOriginal/blindAutomation)

# blindAutomation 🚀
Scripts to control blinds depending on the sun azimuth or weather without sensors!

This python code is meant to run on a raspberrypi. It searches for [Shellys](https://shelly.cloud) in the local Network and maps them with the configured Shellyids (see settings.yaml.template).
This application is build for [Shelly 2.5](https://shelly.cloud/products/shelly-25-smart-home-automation-relay/) in roller mode to control your blinds. It calculates the Sundata with [pvlib](https://pvlib-python.readthedocs.io/en/stable/).
It is necessary to have the shellys calibrated for it opening and close times to get it working correctly, otherwise it might just stops in the middle of the window or does not move at all.

For the Weather data is an account and api key from [OpenWeather](https://openweathermap.org) necessary. A Free Subscription is enough to get it working!
The API key must be configured as environment variable `OPEN_WEATHER_API_KEY` on the run environment.

## Configuration settings.yaml 🎛
copy and rename [settings.yaml.template](https://github.com/RaphiOriginal/blindAutomation/blob/reorganisation/data/settings.yaml.template) to settings.yaml and update the properties.

### Main information
There are some main information necessary like location data and timezone.
#### Location
For proper calculation the application needs your location as precise as possible:
* `coordinates:`
  * `lat:` Latitude of the building
  * `long:` Longitude of the building
  * `alt:` Altitude of the location
##### Example
```
coordinates:
  lat: 47.3916
  long: 8.0512
  alt: 365
```
#### API
* `api:` Defines which api should be used to calculate sundata. I recommend pvlib which will run on your device.
  * Possible values are `pvlib` or `mock`, where mock is only for testing purposes where sunrise is 30 seconds after api call and all degrees are 30 seconds apart from each other.
##### Example
```
api: pvlib
```
#### Timezone
* `timezone:` define which timezone you're to match correct times e.g. for the `TIME`trigger.
  * Check possible values on [Wikipedia](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) in the 'TZ database name' column.
##### Example
```
timezone: 'Europe/Zurich'
```
#### Main information example
```
coordinates:
  lat: 47.3916
  long: 8.0512
  alt: 365
api: pvlib
timezone: 'Europe/Zurich'
```
### Building data
To be able to get all the times correct for example for the `SUNIN` and `SUNOUT` trigger, are some data of the building needes.
#### Walls
Of course has every building some walls where possible shutters to be configured are. That's why we need some data for each wall with shutter you'd like to manage.
* `walls:` holds list of walls that you want to controll
#### Wall
Holds data like when the sun will enter and leafe the wall. On an open field without other buildings or trees at a straight wall, that should be a range about 180° between those properties. Of course with other buildings making shadow, it can be less.
* `wall:` holds the actual data for a wall
  * Properties are `name`, `in`, `out`, `blinds`
  * `name:` To give the wall a name for better management and log output.
  * `in:` Azimuth when the sun would enter the wall.
    * Value must be between `0`° and `360`°.
  * `out:` Azimuth when the sun would leave the wall.
    * Value must be between `0`° and `360`°.
  * `blinds:` List of blind` that are build into the wall.
#### Blind
The `blind` property holds the actual date about the blind and it's device that controls the blind.
* `name:` Name of the blind some thing like 'Kitchen'
* `in:` (optional) Overrides the wall azimuth for sun income trigger
    * Value must be between `0`° and `360`°.
* `out:` (optional) Overrides the wall azimuth for sun outgoing trigger
    * Value must be between `0`° and `360`°.
* `device-id:` ID of the device
  * string
* `device-typ:` Defines which device controlls the blind
  * Possible values are `SHELLY`
* `tilt-time:` (optional) Overrides the time in seconds the blind needs to tilt from 90° to 0°
  * If not set the default value is 1.2 seconds
* `triggers:` List that holds the trigger
  * List of `trigger` for example `SUNRISE` or `SUNOUT`
* `events:` List that holds the event
  * List of `event` for example `CLOUDY` or `WIND`
#### Example
For an example of those properties or more please take a look at [settings.yaml.template](https://github.com/RaphiOriginal/blindAutomation/blob/master/settings.yaml.template).
### Tasks
Tasks defines the actual work that is possible to do. Following tasks are available:
* `OPEN` Opens the blinds
* `CLOSE` Closes the blinds
* `TILT` Will tilt the blinds
You can define how much the blind should tilt by passing a degree value between `0`° and `90`°, where `0`° means fully tilt and `90`° means closed.
Example:
```
task: 
  TILT: 45
```
This will tilt the task for 45°.

with:
```
task: TILT
```
the default degree of `0`° will be applied.
### Triggers
Triggers are either a list of strings where each trigger just uses its default values, or trigger objects. String and objects triggers can be mixed in the list.
Available triggers are:
* `SUNRISE` Will open the blind at sunrise
* `SUNSET` Will close the blind at sunset
* `SUNIN` Will tilt the blind when sun passes configured wall or device azimuth
* `SUNOUT` Will open the blind when sun passes configured wall or device azimuth
* `TIME` Will trigger the configured task when configured time is passed
* `AZIMUTH` Will trigger the configured task when defined azimuth is passed by the sun
* `ELEVATION` Will trigger the configured task when defined elevation is passed by the sun
* `POSITION` Will trigger the configured task when defined azimuth and defined elevation is passed by the sun

How triggers are represented in the settings.yaml file:
```
- TRIGGER
    task: (optional) overrides default task (This is not optional for TIME, AZIMUTH, ELEVATION and POSITION)
    at: (optional) list of days or range or placeholders to define at which days the trigger should be applied. Default is every day!`
    offset: (optional) time in minutes to define the offset of the actual trigger time. Can be positive or negative.
    time: (only and mandatory for TIME) define the time the trigger should be applyied
    azimuth: (AZIMUTH and POSITION trigger only, mandatory) defines which azimuth should be triggered
    elevation: (ELEVATION and POSITION trigger only, mandatory) defines which elevation should be triggered
    direction: (ELEVATION nd POSITION trigger only, mandatory) defines if trigger should by apply when passing the elevation value on sunrise or sunset
```
##### SUNRISE
* Default task: `OPEN`
* Triggers at sunrise
* Optional fields:
  * `task:`
  * `at:`
  * `offset:`
##### SUNSET
* Default task: `CLOSE`
* Triggers at sunset
* Optional fields:
  * `task:`
  * `at:`
  * `offset:`
##### SUNIN
* Default task: `TILT`
* Triggers when sun passes azimuth defined on the wall or device
* Optional fields:
  * `task:`
  * `at:`
  * `offset:`
##### SUNOUT
* Default task: `OPEN`
* Triggers when sun passes azimuth defined on the wall or device
* Optional
  * `task:`
  * `at:`
  * `offset:`
##### TIME
* Triggers when configured time reached
* Mandatory
  * `task:`
  * `time:` in 'HH:MM:SS' format
* Optional
  * `at:`
  * `offset:`
##### AZIMUTH
* Default task: `CLOSE`
* Triggers when sun passes configured azimuth
* Mandatory
  * `azimuth:`
* Optional
  * `task:`
  * `at:`
  * `offset:`
##### ELEVATION
* Default task: `CLOSE`
* Triggers when sun passes configured elevation
* Mandatory
  * `elevation:`
  * `direction:`
* Optional
  * `task:`
  * `at:`
  * `offset:`
##### POSITION
* Default task: `CLOSE`
* Triggers when sun passes configured azimuth and elevation in the configured direction
* Mandatory
  * `azimuth:`
  * `elevation:`
  * `direction:`
* Optional
  * `task:`
  * `at:`
  * `offset:`
#### Trigger Properties
* `task:` Task string or `TILT` object
  * Possible values are `OPEN`, `CLOSE` or `TILT` where `TILT` can have a value between `0`° and `90`°.
* `at:` List of days of week
  * List Possible values are `MO`, `TU`, `WE`, `TH`, `FR`, `SA`, `SU`, `WEEKEND`, `WORKINGDAY` or a range between days e.g. `MO-TH`. The different styles can be mixed, so you can have days and ranges in the list.
* `offset:` Integer
  * Integer in minutes that defines the offset when the task has to be done based on the calculated trigger time. Can be a positive or negative value.
* `time:`
  * Time when task has to be triggeret in the format of 'HH:MM:SS'.
* `azimuth:` Integer
  * Defines an azimuth degree between `0`° and `360`° for a trigger.
* `elevation:` Integer
  * Defines an elevation degree between `-90`° and `90`° for a trigger.
* `direction:` Defines the direction the sun passes an elevation to trigger a task.
  * Possible values are `RISE` or `SET`.
    * `RISE`: will trigger when sun passes elevation degree on sunrise
    * `SET`: will trigger when sun passes elevation degree on sunset
#### Examples
```
...
triggers:
  - SUNRISE
  - SUNSET:
      offset: 20
  - TIME:
      task: TILT
      at:
        - WORKINGDAY
      time: '07:30:00'
  - SUNIN
  - SUNOUT
  - ELEVATION:
      task:
        TILT: 45
      elevation: 16
      direction: SET
...
```
### Events
Events are basically triggers too. But they can't be calculated becaus we can't see when they happens in advance.
Similar to triggers are events also in a list as string or object representation.
The weather is checked every three minutes and will therefore activate or deactivate the events depending on the weather status.
####Weather based events
Following weather based events are available:
* `CLOUDY` Will open the blinds on a cloudy day ☁️
* `RAIN` Will open the blinds on a rainy day 🌧
* `CLEAR` Will close the blinds when the sky is clear ☀️
* `STORM` Will open the blinds when there is a storm ongoing ⛈
* `DRIZZLE` Will open the blinds when there is drizzle
* `SNOW` Will open the blinds when it's snowing 🌨
* `WIND` Will open the blinds when it's windy 🌬
* `SPECIAL` Will open the blinds when there is a special weather event like a tornado 🌪 or fog 🌫

How events are represented in the settings.yaml file:
```
events:
  - EVENT:
      night: (optional) deactivates or activates events running at night
      task: (optional) overrides the default task
      intensity: (optional, except CLOUDY and WIND) overrides the default intensity of an weather event
      coverage: (optional, CLOUDY only) percentage of how much the sky is covered in clouds ☁️ to open the blind
      events: (optional, SPECIAL only) defines on which special event the blind should open
      speed: (optional, WIND only) define a wind speed when blind should open
      direction: (optional, WIND only) define a range in degree in which direction the wind should blow to open the blind
        from: degree starting the wind direction range
        to: degree stopping the wind direction range
      at: (optional) list of days or range or placeholders to define at which days the trigger should be applied. Default is every day!`
```

##### CLOUDY
* Default task: `OPEN`
* Triggers when cloud coverage passes specified percentage
* Default percentage: `100`%
* Optional fields:
  * `night:`
  * `task:`
  * `coverage:`
  * `at:`
##### CLEAR
* Default task: `OPEN`
* Triggers when the sky is clear
* Optional fields:
  * `night:`
  * `task:`
  * `at:`
##### RAIN
* Default task: `OPEN`
* Triggers when its raining
* Available intensities are: `MODERATE`, `VERY_HEAVY`, `EXTREME`, `FREEZING`, `LIGHT_SHOWER`, `HEAVY_SHOWER`, `RAGGED_SHOWER`, `SHOWER`, `HEAVY`, `LIGHT`
* Default set intensities are: `MODERATE`, `HEAVY`, `VERY_HEAVY`, `EXTREME`, `SHOWER`, `HEAVY_SHOWER`, `RAGGED_SHOWER`
* Optional fields:
  * `night:`
  * `task:`
  * `intensity:`
  * `at:`
##### STORM
* Default task: `OPEN`
* Triggers when there is a storm
* Available intensities are: `LIGHT_RAIN`, `RAIN`, `HEAVY_RAIN`, `LIGHT`, `NORMAL`, `HEAVY`, `RAGGED`, `LIGHT_DRIZZLE`, `DRIZZLE`, `HEAVY_DRIZZLE`
* Default set intensities are: `LIGHT_RAIN`, `RAIN`, `HEAVY_RAIN`, `LIGHT`, `NORMAL`, `HEAVY`, `RAGGED`, `LIGHT_DRIZZLE`, `DRIZZLE`, `HEAVY_DRIZZLE`
* Optional fields:
  * `night:`
  * `task:`
  * `intensity:`
  * `at:`
##### DRIZZLE
* Default task: `OPEN`
* Triggers when there is drizzle
* Available intensities are: `LIGHT_RAIN`, `RAIN`, `LIGHT`, `NORMAL`, `HEAVY`, `HEAVY_RAIN`, `SHOWER_RAIN`, `HEAVY_SHOWER_RAIN`, `SHOWER`
* Default set intensities are: `HEAVY_RAIN`, `SHOWER_RAIN`, `HEAVY_SHOWER_RAIN`, `SHOWER`
* Optional fields:
  * `night:`
  * `task:`
  * `intensity:`
  * `at:`
##### SNOW
* Default task: `OPEN`
* Triggers when it is snowing
* Available intensities are: `LIGHT_RAIN`, `RAIN`, `LIGHT`, `NORMAL`, `HEAVY`, `SHOWER`, `LIGHT_SHOWER`, `HEAVY_SHOWER`, `SLEET`, `LIGHT_SHOWER_SLEET`, `SHOWER_SLEET`
* Default set intensities are: `LIGHT_RAIN`, `RAIN`, `LIGHT`, `NORMAL`, `HEAVY`, `SHOWER`, `LIGHT_SHOWER`, `HEAVY_SHOWER`, `SLEET`, `LIGHT_SHOWER_SLEET`, `SHOWER_SLEET`
* Optional fields:
  * `night:`
  * `task:`
  * `intensity:`
  * `at:`
##### SPECIAL
* Default task: `OPEN`
* Triggers when there appears one of the defined events
* Available events are: `MIST`, `SMOKE`, `HAZE`, `WHIRLS`, `FOG`, `SAND`, `DUST`, `ASH`, `SQUALL`, `TORNADO`
* Default set events are: `MIST`, `SMOKE`, `HAZE`, `WHIRLS`, `FOG`, `SAND`, `DUST`, `ASH`, `SQUALL`, `TORNADO`
* Optional fields:
  * `night:`
  * `task:`
  * `events:`
  * `at:`
##### WIND
* Default task: `OPEN`
* Triggers when the wind hits a certain speed and if configured a specific direction
* Default speed: `120` meters per second
* Default direction: There is per default no direction set
* Optional fields:
  * `night:`
  * `task:`
  * `direction:`
  * `at:`
#### Event properties
* `night:` Property to turn on or off the night mode.
  * Possible values are `True` or `False`. Default for all events is `True`.
* `task:` Task string or `TILT` object
  * Possible values are `OPEN`, `CLOSE` or `TILT` where `TILT` can have a value between `0`° and `90`°.
* `intensity:` List of intensity strings to override the default intensity list.
  * For possible values check the event detail descriptions.
* `coverage:` Percentage of cloud coverage to define at which coverage the task should get triggered.
  * Possible value is between `0`% and `100`%.
* `events:` Property to limit the events when the special event task should be triggered.
  * Available events are: `MIST`, `SMOKE`, `HAZE`, `WHIRLS`, `FOG`, `SAND`, `DUST`, `ASH`, `SQUALL`, `TORNADO`
* `speed:` Property in meters per second for wind speed.
  * Value has to be higher than `0.0`
* `direction:` Property to define a specific direction range where the wind blows to, to trigger the task.
  * `from:` Value between `0`° and `360`°.
  * `to:` Value between `0`° and `360`°.
  * the `from` property also can be lower than the `to` property then the range goes from `to`° over `0`° to `from`°.
* `at:` List of days of week
  * List Possible values are `MO`, `TU`, `WE`, `TH`, `FR`, `SA`, `SU`, `WEEKEND`, `WORKINGDAY` or a range between days e.g. `MO-TH`. The different styles can be mixed, so you can have days and ranges in the list.
#### Examples
```
...
events:
  - CLOUDY
  - RAIN
  - SNOW:
      intensity:
        - SLEET
        - LIGHT_SHOWER_SLEET
        - SHOWER_SLEET
  - SPECIAL:
      task: CLOSE
      events:
        - TORNADO
        - MIST
        - FOG
  - WIND:
      night: False
      task:
        TILT: 60
      speed: 80
      direction:
        from: 180.4
        to: 200
      at:
        - WEEKEND
...
```
## Running and Installation 🏃🏗
##### Balena.io
After you downloaded the project and prepared your settings file, the easiest way to do it is by deploying it with [balena](https://www.balena.io/os)
Follow getting started and after all the preparation is done and your RaspberryPi 4 is reachable over the network, simpli go to the project root folder in the terminal and use following command:
```
$balena push yourDevice.local
```
the app will fetch sundata for the actual date and if this results in no tasks, it will do it for the following date. after the work is done, it will exit and the container will restart it self and we fetch again tasks for the next day 💪
I recommend to use balena cloud for better device management even outside of your local network.


Made with ❤️ in 🇨🇭
