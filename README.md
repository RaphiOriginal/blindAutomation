# blindAutomation 🚀
Scripts to control blinds depending on the sun azimuth

This python code is meant to run on a raspberrypi. It searches for [Shellys](https://shelly.cloud) in the configured Networkmask and maps them with the configured Shellyids (see settings.yaml.template).
This application is build for [Shelly 2.5](https://shelly.cloud/products/shelly-25-smart-home-automation-relay/) in roller mode to controll your blinds. It collects the Sundata from [Meteomatics](https://www.meteomatics.com/)
It is necessary to have the shellys calibrated for it runtimes to get it working correctly, otherwise it might just stops in the middle of the window.

## Configuration settings.yaml 🎛
copy and rename [settings.yaml.template](https://github.com/RaphiOriginal/blindAutomation/blob/master/settings.yaml.template) to settings.yaml and update the properties:
* meteomatics: Meteomatics api credentials
  * username: from Meteomatics
  * password: from Meteomatics
  * coordinates: coordinates of wall (i recommend to pick a corner of two walls) I did mine with the help of [SunCalc](https://www.suncalc.org/#/46.0162,8.4421,3/2020.07.27/19:54/1/1)
    * lat: Latitude
    * long: Longitude
* api: Which api you want to use (meteomatics is recommended here)
* networkmask: where to to search for shellys
* walls:
  * wall:
    * name: where the wall is (can be any name, e.g. 'south' or 'green wall'')
    * in: When the sun azimuth starts to hit the wall
    * out: When the sun azimuth stops to hit the wall
* shellys: list of shellys
  * shelly:
    * name: How you'd like to name the shelly to recognise it in text outputs
    * id: Shellyid (can be found in the shelly app in settings) usualy last 6 characters of macadress
    * direction: At which wall is the shelly located (must match with a name from walls)
    * triggers: List of triggers you'd like to apply for the shelly
      * SUNRISE: Will open the blinds on sunrise
        * task: (optional) default is OPEN
      * SUNSET: Will close the blinds on sunset
        * task: (optional) default is CLOSE
      * SUNIN: Will tilt the blinds when the azimuth of the sun passes the azimuth defined for the related wall
        * task: (optional) default is TILT
      * SUNOUT: Will open the blinds when the azimuth of the sun passes the azimuth defined for the related wall
        * task: (optional) default is OPEN
      * TIME: Add a Task (OPEN, CLOSE, TILT) you want at a given time, will be run at this time daily
        * task: (mandatory) Can be OPEN, CLOSE or TILT. Tilt will close the blind completle and then open for around 2%
        * time: (mandatory) Time when the task should be triggered in the HH:MM:SS format

## Meteomatics ☀️
You have to get access to the meteomatics api and update your logins in the settings.yaml

## Running and Installation 🏃🏗
##### Balena.io
After you downloaded the project and prepared your settings file, the easiest way to do it is by deploying it with [balena](https://www.balena.io/os)
Follow getting started and after all the preparation is done and your RaspberryPi 4 is reachable over the network, simpli go to the project root folder in the terminal and use following command:
```
balena push yourDevice.local
```
after that, the application fetches all new sundata every 03:00 of your local timezone
after powerloss, the container will start itself again and we're back on track.
Further customization are possible in the Dockerfile
##### Manual Installation
If you want to install the application without Docker you can install it also manually for the same functionality. Only how you will bring the code on the device is then your own business.
I recommend to run this scripts with cronjob. It will collect all task for a full day, and after the day is over, it will finish and needs to be started again.
Due to the nature of the Meteomatics API i recommend to time your Fetch for your day after midnight utc if possible (e.g. 03:00 for MEZ) but before the first Task should be applied.

you can edit crontab with e.g. nano:
`$ crontab -e`

Add cronjobs:
```
0 3 * * * ~/blindAutomation/app.py
```

It is also recommended to start the script after a reboot to get the magic ongoing e.g. after a power outage.
To achieve this, we use systemd.

you can start configure your service with:
`sudo systemctl edit --force --full blindAutomation.service`

and entering following configurations into the file:

```
[Unit]
Description=Blind Automation Service
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi
ExecStart=/home/pi/blindAutomation/app.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
WantedBy=network-online.service
```

after that a simple `sudo systemctl enable blindAutomation.service` will start the app after every reboot

## Logging 🖨

if you like to log the app output, you can adding following to your cronjob:

```
0 3 * * * ~/blindAutomation/app.py >> /output-daily.log 2>&1
```
the output of the reboot job (which is only a fallback anyway) will be logged automaticly and can be found with `sudo journalctl -b -u blindAutomation`.
But those logs will disappear after a reboot

Made with ❤️ in 🇨🇭
