BOTLIB
######

| Welcome to BOTLIB, framework to program bots ! see https://pypi.org/project/botlib/ 


| BOTLIB is placed in the public domain and contain no copyright or LICENSE, this makes BOTLIB truely free (pastable) code you can use how you see fit, 

installation is through pypi:

 > sudo pip3 install botlib --upgrade --force-reinstall

you can also run directly from the tarball, see https://pypi.org/project/botlib/#files

USAGE
=====

BOTLIB has it's own CLI, you can run it by giving the bcmd command on the
prompt, it will return with no response:

:: 

 $ bcmd
 $ 

you can use objr <cmd> to run a command directly:

::

 $ bcmd cmds
 cmd|dne|edt|fnd|flt|krn|log|add|tsk|tdo|udp|upt|ver


BOTLIB also has it's own shell, bsh:

::

  $ bsh
  > cmd

 cmd|dne|edt|fnd|flt|krn|log|add|tsk|tdo|udp|upt|ver

IRC
===

BOTLIB provides the birc as IRC client, configuration is done with the cfg command:

::

 $ bcmd cfg
 channel=#botlib nick=birc port=6667 realname=botlib server=localhost username=botlib

you can use setters to edit fields in a configuration:

::

 $ bcmd cfg server=irc.freenode.net channel=\#botlib nick=birc
 channel=#botib nick=birc port=6667 realname=botlib server=irc.freenode.net username=botlib

RSS
===

BOTLIB provides with the use of feedparser the possibility to server rss
feeds in your channel. adding rss to mods= will load the rss modules and
start it's poller.

::

 $ birc mods=rss

to add an url use the rss command with an url:

::

 $ bcmd rss https://github.com/bthate/objr/commits/master.atom
 ok 1

run the rss command to see what urls are registered:

::

 $ bcmd fnd rss
 0 https://github.com/bthate/objr/commits/master.atom

the ftc (fetch) command can be used to poll the added feeds:

::

 $ bcmd ftc
 fetched 0

UDP
===

BOTLIB also has the possibility to serve as a UDP to IRC relay where you
can send UDP packages to the bot and have txt displayed on the channel.

use the 'budp' command to send text via the bot to the channel on the irc server:

::

 $ tail -f /var/log/syslog | budp

to send the tail output to the IRC channel you can use python3 code to send a UDP packet 
to botlib, it's unencrypted txt send to the bot and display on the joined channels.

to send a udp packet to botlib in python3:

::

 import socket

 def toudp(host=localhost, port=5500, txt=""):
     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     sock.sendto(bytes(txt.strip(), "utf-8"), host, port)

MODULES
=======

BOTLIB use the OLIB library for the new functional object library, it provides
a move all methods to functions and to 

::

 method(obj, *args) instead of obj.method(*arg)

way of programming with objects. If you are use to functional programming you'll like it (or not) ;]

OLIB has the following modules:

::

    ol	 	- object library
    ol.bus	- announce
    ol.csl	- console
    ol.dbs	- databases
    ol.hdl	- handler
    ol.krn	- kernel
    ol.prs 	- parser
    ol.tms	- times
    ol.trm	- terminal
    ol.tsk	- tasks
    ol.utl	- utilities

BOTLIB uses bmod as the namespace to distribute modules for BOTLIB:

::

   bmod.cmd	- command
   bmod.edt	- edit
   bmod.ent	- enter log and todo items
   bmod.fnd	- find typed objects
   bmod.mbx	- mailbox
   bmod.rss	- rich site syndicate
   bmod.udp	- UDP to IRC gateway

BOTLIB has 1 module, the bot.irc module:

::

   bot.irc

this package adds bot.irc to the bot namespace.

you can add you own modules to the bot and bmod packages, they are namespace packages.


SERVICE
=======

if you want to run the BOTLIB 24/7 you can install botd as a service for
the systemd daemon. You can do this by copying the following into
the /etc/systemd/system/botd.service file:

::


 [Unit]
 Description=BOTD - 24/7 channel daemon
 After=network-online.target
 Wants=network-online.target

 [Service]
 User=botlib
 Group=botlib
 ExecStart=/usr/local/bin/botd 

 [Install]
 WantedBy=multi-user.target

create a homedir for objr:

::

 $ mkdir /home/botlib
 $ mkdir /home/botlib/.bot
 $ mkdir /home/botlib/.bot/bmod

add the botlib user to the system:

::

 $ groupadd botlib
 $ chown -R botlib:botlib /home/botlib
 $ useradd botlib -d /home/botlib
 $ passwd botlib

configure botd to connect to irc:

::

 $ sudo -u botlib bcmd cfg server=irc.freenode.net channel=#botlib nick=birc

copy modules over to botlib's work directory:

::

 $ cp -Ra bmod/*.py /home/botlib.bot/bmod

make sure permissions are set properly:

::

 $ chown -R botlib:botlib /home/botlib
 $ chown -R botlib:botlib /home/botlib/.bot
 $ chmod -R 700 /home/botlib/.bot/bmod/
 $ chmod -R 400 /home/botlib/.bot/bmod/*.py

add the botd service with:

::

 $ sudo systemctl enable botd
 $ sudo systemctl daemon-reload

then restart the botd service.

::

 $ sudo service botd stop
 $ sudo service botd start

if you don't want botd to startup at boot, remove the service file:

::

 $ sudo rm /etc/systemd/system/botd.service

CONTACT
=======

contact me on IRC/freenode/#dunkbots or email me at bthate@dds.nl

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net
