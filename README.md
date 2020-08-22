[![Build Status](https://travis-ci.org/RaphiOriginal/blindAutomation.svg?branch=master)](https://travis-ci.org/RaphiOriginal/blindAutomation)

# blindAutomation 🚀
Scripts to control blinds depending on the sun azimuth

This python code is meant to run on a raspberrypi. It searches for [Shellys](https://shelly.cloud) in the local Network and maps them with the configured Shellyids (see settings.yaml.template).
This application is build for [Shelly 2.5](https://shelly.cloud/products/shelly-25-smart-home-automation-relay/) in roller mode to controll your blinds. It calculates the Sundata with [pvlib](https://pvlib-python.readthedocs.io/en/stable/)
It is necessary to have the shellys calibrated for it runtimes to get it working correctly, otherwise it might just stops in the middle of the window.

## Configuration settings.yaml 🎛
copy and rename [settings.yaml.template](https://github.com/RaphiOriginal/blindAutomation/blob/master/settings.yaml.template) to settings.yaml and update the properties:
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
            device-id: #Shellyid (can be found in the shelly app in settings) usualy last 6 characters of macadress
            device-typ: SHELLY #Fix set to Shelly since no other controllers supported yet
            tilt_time: #(optional) overrides the defaulttime the blind needs to fully tilt
            triggers: #List of triggers you'd like to apply for the shelly
              SUNRISE: #Will open the blinds on sunrise
                task: #(optional) default is OPEN
                on: #(optional List) defines on which weekdays the trigger applies. Options are: MO, TU, WE, TH, FR, SA, SU, or ranges e.g. MO-WE or WORKINGDAY or WEEKEND. You can Mix all of them in the list
                offset: #(optional) default is 0 can be positiv or negativ
              SUNSET: #Will close the blinds on sunset
                task: #(optional) default is CLOSE
                on: #(optional List) defines on which weekdays the trigger applies. Options are: MO, TU, WE, TH, FR, SA, SU, or ranges e.g. MO-WE or WORKINGDAY or WEEKEND. You can Mix all of them in the list
                offset: #(optional) default is 0 can be positiv or negativ
              SUNIN: #Will tilt the blinds when the azimuth of the sun passes the azimuth defined for the related wall
                task: #(optional) default is TILT
                on: #(optional List) defines on which weekdays the trigger applies. Options are: MO, TU, WE, TH, FR, SA, SU, or ranges e.g. MO-WE or WORKINGDAY or WEEKEND. You can Mix all of them in the list
                offset: #(optional) default is 0 can be positiv or negativ
              SUNOUT: #Will open the blinds when the azimuth of the sun passes the azimuth defined for the related wall
                task: #(optional) default is OPEN
                on: #(optional List) defines on which weekdays the trigger applies. Options are: MO, TU, WE, TH, FR, SA, SU, or ranges e.g. MO-WE or WORKINGDAY or WEEKEND. You can Mix all of them in the list
                offset: #(optional) default is 0 can be positiv or negativ
              TIME: #Add a Task (OPEN, CLOSE, TILT) you want at a given time, will be run at this time daily
                task: #(mandatory) Can be OPEN, CLOSE or TILT. Tilt will close the blind completle and then open for around 2%
                on: #(optional List) defines on which weekdays the trigger applies. Options are: MO, TU, WE, TH, FR, SA, SU, or ranges e.g. MO-WE or WORKINGDAY or WEEKEND. You can Mix all of them in the list
                time: #(mandatory) Time when the task should be triggered in the HH:MM:SS format
                offset: #(optional) default is 0 can be positiv or negativ (even if this would be ridiculous 😏)
              AZIMUTH:
                azimuth: #(mandatory) defines azimuth to be passed to trigger task
                task: #(optional) default is CLOSE
                on: #(optional List) defines on which weekdays the trigger applies. Options are: MO, TU, WE, TH, FR, SA, SU, or ranges e.g. MO-WE or WORKINGDAY or WEEKEND. You can Mix all of them in the list
                offset: #(optional) default is 0 can be positiv or negativ
              ELEVATION:
                elevation: #(mandatory) defines elevation to be passed to trigger task
                direction: #(mandatory) choose between (RISE and SET) to define elevation when sun rises or when sun sets
                task: #(optional) default is CLOSE
                on: #(optional List) defines on which weekdays the trigger applies. Options are: MO, TU, WE, TH, FR, SA, SU, or ranges e.g. MO-WE or WORKINGDAY or WEEKEND. You can Mix all of them in the list
                offset: #(optional) default is 0 can be positiv or negativ
              POSITION: #will be triggered when azimuth and elevation has been passed (will take the later event)
                azimuth: #(mandatory) defines elevation to be passed to trigger task
                elevation: #(mandatory) defines elevation to be passed to trigger task
                direction: #(mandatory) choose between (RISE and SET) to define elevation when sun rises or when sun sets
                task: #(optional) default is CLOSE
                on: #(optional List) defines on which weekdays the trigger applies. Options are: MO, TU, WE, TH, FR, SA, SU, or ranges e.g. MO-WE or WORKINGDAY or WEEKEND. You can Mix all of them in the list
                offset: #(optional) default is 0 can be positiv or negativ
```

## Running and Installation 🏃🏗
##### Balena.io
After you downloaded the project and prepared your settings file, the easiest way to do it is by deploying it with [balena](https://www.balena.io/os)
Follow getting started and after all the preparation is done and your RaspberryPi 4 is reachable over the network, simpli go to the project root folder in the terminal and use following command:
```
balena push yourDevice.local
```
the app will fetch sundata for the actual date and if this results in no tasks, it will do it for the following date. after the work is done, it will exit and the container will restart it self and we fetch again tasks for the next day 💪
I recommend to use balena cloud for better device management even outside of your local network.


Made with ❤️ in 🇨🇭
