'''

mini_dlna_browser - a dlna/upnp browser with a basic GUI implemented in Python

Copyright (C) 2021  Ian Eperson - ian.eperson@dedf.co.uk

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or 
(at your option) any later version.

Created on 23 Feb 2021

'''

from tkinter import Tk, Label, Button, Frame, Canvas, Scrollbar

from Upnp import *

class Application(Frame):
    
    def stdButton(self, grow, gcolumn, btext, action):
        but = Button(self.scrollableframe, height=0, width=0, borderwidth=0, anchor="w", font=(0, 9, 'roman'))
        but["text"] = btext
        but.bind("<1>", action)
        but.grid(row = grow, column = gcolumn, sticky = "w")
        self.displayed.append (but)
    
    def createItems(self, ditem):
        self.history.append(ditem) # add this item to the history
        for x in self.displayed: # remove the existing entries
            x.destroy()       
        self.canvas.yview_moveto(0) # reset the scroll
        
        grow = 0 # start at the top 
        self.stdButton(0, 0, "Exit", quit)
        if len(self.history) > 1:
            def GoToParent(event, self=self):
                self.history.pop() # pop the current folder
                return self.createItems(self.history.pop()) # and the parent - creatItems will push it back again
            self.stdButton(0, 2, "Parent container", GoToParent)
               
        for sitem in Upnp().Search(ditem): # get the children for this container
            grow = grow + 1 # on the next line
            if (sitem[0] == 'container'):
                def OpenContainer(event, self=self, x=sitem[1]): # set a local callback function so we can add an exra parameter
                    return self.createItems(x) # create a new display for the selected container
                self.stdButton(grow, 0, "Open", OpenContainer)
                
            def PlayItem(event, self=self, x=sitem[1]): # set a local callback function so we can add an exra parameter
                return Upnp().FindandPlay(x) 
            self.stdButton(grow, 1, "Play", PlayItem)

            text = Label(self.scrollableframe, height=0, width=0, anchor="w", font=(0, 9, 'italic')) # changing the slant increases default font size?
            text["text"] = sitem[2]
            text.grid(row = grow, column = 2, sticky = "w")
            self.displayed.append (text)
               
    def __init__(self, master=None):
        super().__init__(master)
        master.resizable(False, False)
        self.pack(side="left", fill="none")

        self.canvas = Canvas(self)
        scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollableframe = Frame(self.canvas)
        def scroller(event, self=self):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.scrollableframe.bind( "<Configure>", scroller)
        self.canvas.create_window((0, 0), window=self.scrollableframe, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both")
        scrollbar.pack(side="right", fill="y")

        self.displayed = [] # the items currently displayed (so we can remove them)
        self.history = [] # the container history (so we can go back up the tree)
        
        self.createItems("0") # start at the root

# the standard Tk startup/mainloop
root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
