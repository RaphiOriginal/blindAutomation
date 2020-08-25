[![Build Status](https://travis-ci.org/RaphiOriginal/blindAutomation.svg?branch=master)](https://travis-ci.org/RaphiOriginal/blindAutomation)

# blindAutomation 🚀
Scripts to control blinds depending on the sun azimuth or weather without sensors!

This python code is meant to run on a raspberrypi. It searches for [Shellys](https://shelly.cloud) in the local Network and maps them with the configured Shellyids (see settings.yaml.template).
This application is build for [Shelly 2.5](https://shelly.cloud/products/shelly-25-smart-home-automation-relay/) in roller mode to control your blinds. It calculates the Sundata with [pvlib](https://pvlib-python.readthedocs.io/en/stable/).
It is necessary to have the shellys calibrated for it opening and close times to get it working correctly, otherwise it might just stops in the middle of the window or does not move at all.

For the Weather data is an account and api key from [OpenWeather](https://openweathermap.org) necessary. A Free Subscription is enough to get it working!
The API key must be configured as environment variable `OPEN_WEATHER_API_KEY` on the run environment.

## Configuration settings.yaml 🎛
copy and rename [settings.yaml.template](https://github.com/RaphiOriginal/blindAutomation/blob/master/settings.yaml.template) to settings.yaml and update the properties.

Basics:
```
pvlib:
  coordinates:
    lat: #Latitude
    long: #Longitude
    alt: #Altitude
api: #Which api you want to use (pvlib is recommended here)
timezone: #A time zone name (IANA)
walls: #List of walls with blinds of your home
  - wall: #Represents one side of your house with possible multiple blinds
      name: #where the wall is (can be any name, e.g. 'south' or 'green wall'')
      in: #When the sun azimuth starts to hit the wall
      out: #When the sun azimuth stops to hit the wall
      blinds: #list of blinds you'd like to manage for this wall
        - blind:
            name: #Name of blind to identify them more easy
            in: #(optional) Overrides the wall values for this blind
            out: #(optional) Overrides the wall values for this blind
            device-id: #deviceid (can be found in the shelly app in settings) usualy last 6 characters of macadress
            device-typ: SHELLY #Fix set to Shelly since no other controllers supported yet
            tilt_time: #(optional) overrides the defaulttime the blind needs to fully tilt
            triggers: #List of triggers you'd like to apply for the device`
            events: #List of events sou'd like to apply for the device
```
###Tasks
Tasks defines the actual work that is possible to do. Following tasks are available:
* `OPEN` Opens the blinds
* `CLOSE` Closes the blinds
* `TILT` Will tilt the blinds
You can define how much the blind should tilt by passing a degree value between 0 and 90, where 0 means fully tilt and 90 means closed.
Example:
```
task: 
  TILT: 45
```
This will tilt the task for 45°. with:
```
task: TILT
```
the default degree of `0` will be applied.
###Triggers
Triggers are either a list of strings where each trigger just uses its default values.
Available triggers are:
* `SUNRISE` Will open the blind at sunrise
* `SUNSET` Will close the blind at sunset
* `SININ` Will tilt the blind when sun passes configured wall or device azimuth
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
#####SUNRISE
* Default task: `OPEN`
* Triggers at sunrise
* Optional fields:
  * `task:`
  * `at:`
  * `offset:`
#####SUNSET
* Default task: `CLOSE`
* Triggers at sunset
* Optional fields:
  * `task:`
  * `at:`
  * `offset:`
#####SUNIN
* Default task: `TILT`
* Triggers when sun passes azimuth defined on the wall or device
* Optional fields:
  * `task:`
  * `at:`
  * `offset:`
#####SUNOUT
* Default task: `OPEN`
* Triggers when sun passes azimuth defined on the wall or device
* Optional
  * `task:`
  * `at:`
  * `offset:`
#####TIME
* Triggers when configured time reached
* Mandatory
  * `task:`
  * `time:` in 'HH:MM:SS' format
* Optional
  * `at:`
  * `offset:`
#####AZIMUTH
* Default task: `CLOSE`
* Triggers when sun passes configured azimuth
* Mandatory
  * `azimuth:`
* Optional
  * `task:`
  * `at:`
  * `offset:`
#####ELEVATION
* Default task: `CLOSE`
* Triggers when sun passes configured elevation
* Mandatory
  * `elevation:`
  * `direction:`
* Optional
  * `task:`
  * `at:`
  * `offset:`
#####POSITION
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
####Trigger Properties
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
####Examples
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
###Events

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
