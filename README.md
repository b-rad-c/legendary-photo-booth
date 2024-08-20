# Legendary Photobooth

A photobooth app for the raspberry pi, used in the Legends of the Hidden Playa burning man maze!

See `USER_GUIDE.txt` for printable instructions.

## Requirements
* raspberry pi (tested with model 4)
* rasperry pi camera
* raspberry pi os - port of debian bookworm
* python 3

NOTE: the raspberry pi os contains libraries necessary for this to work, no additional deps are required. A vanilla install of debian bookworm has not been tested and likely does not work out of the box.

## Setup

Copy the software onto the raspberry pi and setup a cron job to launch it at boot. Note that the `DISPLAY` variable is required to display the window.

Open cron:	`crontab -e`
Add the following line:

    @reboot export DISPLAY=:0; /usr/bin/python3 <path>/photo_booth.py &> /tmp/photo.log
    
## dev notess

I originally tried the pibooth photo app but it doesn't work with the current OS,
and the old version of the OS didn't have the libraries, etc, etc...

Instead, I decided to make a super simple app barely more than a hello world application that would be simple to maintain.

I tried several hello worlds i found online and in the included docs before settling on one with the right features.
* can respond to keyboard input to trigger photo capture
* can display live preview, take pics, and cycle back any forth
* can be triggered on startup and have keyboard focus
    --> the actual implementation should not require a keyboard or mouse 
        however the capture button uses the keyboard protocol 
        which is why we need to capture keyboard. We need to boot directly 
        into our app ready to capture photos w/o user input
            
It's crucial for performance to get the async timing correct
* event loop in section 8 of included picamera2 manual
* `signal_function`
* `picam2.wait(job)`

## Useful links
https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/8
https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf
https://github.com/raspberrypi/picamera2/blob/main/apps/app_capture2.py
https://www.raspberrypi.com/documentation/computers/camera_software.html
