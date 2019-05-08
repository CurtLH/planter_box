# planter_box

```
$ sudo vim /etc/postgresql/10/main/postgresql.conf
```

Add the following
```
listen_addresses = '*'
```

```
$ sudo vim /etc/postgresql/10/main/ph_hba.conf
```

Add the following

```
host	all	all	192.168.0.102/0	md5
```

Start the sensors on reboot

```
$ sudo crontab -e
```

Add the following:

```
@reboot /home/pi/planter-box/launch.sh
```
