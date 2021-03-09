This is a simple DLNA/UPNP browser providing a user interface to a remote minidlna server.

It was inspired by Javier López's simple-dlna-browser (https://github.com/javier-lopez/learn/blob/master/sh/tools/simple-dlna-browser) which a is triumph of shell scripting.  Thanks to Javier for the headers and SOAP action scripts. 

It adopts Javier's approach but uses Python to add a minimal graphical user interface via Tkinter.

The video/music player is mplayer which is invoked from the Python script by a system call.

The browser works with minidlna - it hasn't (yet) been tested with any other DLNA/UPnP-AV servers


To run the browser you are going to need Python3 - with Tkinter and Python's regular expression handler (re), its HTTP library (requests) and, to run the player, the system library (os).

You will need to change the URL to match the location of your minidlna server.

To keep everything a simple as possible there is a lot of reliance on Tkinter’s default settings, this does leave plenty of scope for customization.

The container search is limited to 1000 responses, the item search to 100.  Modifying the values in the respective headers will have a significant effect on the speed of operation.

Parsing the returned data does depend on the a$b$c$d... format for the item/container identifiers.  (With a,b, c,d... being integer values at the different levels of the object tree.)

Adapting the code to earlier Pythons should be straightforward.

