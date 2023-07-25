# enocean_webthing
A web-connected enocean gateway. This project provides a [webthing API](https://iot.mozilla.org/wot/) for an enocean gateway like the [EnOcean USB 300 USB gateway](https://www.enocean.com/de/produkt/usb-300-500u-400j/).

The enocean_webthing package provides a http webthing endpoint that supports enocean devices.

E.g.
```
# webthing has been started on host 192.168.0.23

curl http://192.168.1.198:9090/0/properties

{
   "eep_id":"F6:10:00",
   "enocean_id":"81:00:F0:4E",
   "state":3
}
```
Currently, the following [devices](https://www.enocean-alliance.org/wp-content/uploads/2017/05/EnOcean_Equipment_Profiles_EEP_v2.6.7_public.pdf) are supported.
* Window handle like [HOPPE window handle ConnectHome](https://www.hoppe.com/in-en/window-handles/hoppe-innovations-window-handles/ehandle-connecthome-for-windows/) (EEP ID: F6:10:00).

To install this software, you can use the [PIP](https://realpython.com/what-is-pip/) package manager as shown below.
**PIP approach**
```
sudo pip install enocean_webthing
```

After installation, you can start the Webthing http endpoint in your Python code or from the command line by typing
```
sudo enocean --command listen --port 9090 --path /dev/ttyUSB-enocean --devices 'Office/F6:10:00/81:00:F0:4E, Patiodoor/F6:10:00/01:9A:CC:06'
```
Here, the Webthing API is bound to local port 9090 via the USB gateway /dev/ttyUSB-enocean.
To list the devices to be supported, a comma-separated list with the syntax {device name}/{EEP ID}/{ENOCEAN ID} is used.


As an alternative to the *list* command, you can also use the *register* command to register and start the webthing service as a systemd entity.
This way, the webthing service is started automatically at boot time. Starting the server manually with the *listen* command is no longer necessary.
```
sudo enocean --command register --port 9090 --path /dev/ttyUSB-enocean --devices 'Office/F6:10:00/81:00:F0:4E, Patiodoor/F6:10:00/01:9A:CC:06'
```  