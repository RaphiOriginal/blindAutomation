# blindAutomation
Scripts to control blinds depending on the sun azimuth

This python code is meant to run on a raspberrypi. It searches for [Shellys](https://shelly.cloud) in the configured Networkmask and maps them with the configured Shellyids (see settings.yaml.template).
This application is build for [Shelly 2.5](https://shelly.cloud/products/shelly-25-smart-home-automation-relay/) in roller mode to controll your blinds. It collects the Sundata from [Meteomatics](https://www.meteomatics.com/)
It is necessary to have the shellys calibrated for it runtimes to get it working correctly, otherwise it might just stops in the middle of the window.

## Configuration settings.yaml
copy and rename settings.yaml.template to settings.yaml and update the properties:
* meteomatics: Meteomatics api credentials
  * username
  * password
  * coordinates of wall (i recommend to pick a corner of two walls) I did mine with the help of [SunCalc](https://www.suncalc.org/#/46.0162,8.4421,3/2020.07.27/19:54/1/1)
    * lat: Latitude
    * long: Longitude
* api which you want to use
* networkmask where to to search for shellys
* walls
  * direction where the wall is (can be any name)
  * in: When the sun azimuth starts to hit the wall
  * out: When the sun azimuth stops to hit the wall
* list of shellys
  * How you'd like to name the shelly to recognise it in text outputs
  * Shellyid (can be found in the shelly app in settings) usualy last 6 characters of macadress
  * direction: At which wall is the shelly located (must match with a name from walls)
  * triggers: You can add those triggers you'd like to be handled for each shelly
    * SUNRISE: Will open the blinds on sunrise
    * SUNSET: Will close the blinds on sunset
    * SUNIN: Will tilt the blinds when the azimuth of the sun passes the azimuth defined for the related wall
    * SUNOUT: Will open the blinds when the azimuth of the sun passes the azimuth defined for the related wall
    * TIME: Add a Task (OPEN, CLOSE, TILT) you want at a given time, will be run at this time daily
      * task: Can be OPEN, CLOSE or TILT. Tilt will close the blind completle and then open for around 2%
      * time: Time when the task should be triggered in the HH:MM:SS format

## Meteomatics
You have to get access to the meteomatics api and update your logins in the settings.yaml

## Run
I recommend to run this scripts with cronjob. It will collect all task for a full day, and after the day is over, it will finish and needs to be started again.
Due to the nature of the Meteomatics API i recommend to time your Fetch for your day after midnight utc if possible (e.g. 03:00 for MEZ) but before the first Task should be applied.
I also recommend to start the script on startup, to keep the blinds going after power loss.

you can edit crontab with e.g. nano:
`$ nano /etc/crontab`

Add cronjobs:
```
0 3     * * *   root    python3 ~/blindAutomation/app.py
@reboot         root    python3 ~/blindAutomation/app.py &
