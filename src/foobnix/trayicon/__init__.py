'''
Created on Mar 13, 2010

@author: ivan
'''

import gtk
import os.path
from foobnix.base import BaseController
from foobnix.base import SIGNAL_RUN_FIRST, TYPE_NONE


class TrayIcon(BaseController):
    """
    A class that represents tray icon and a widget that pops up when the icon is right-clicked.
    """
    
    __gsignals__ = {
        'exit'  : (SIGNAL_RUN_FIRST, TYPE_NONE, ()),
        'toggle_window_visibility' : (SIGNAL_RUN_FIRST, TYPE_NONE, ()),

        'play'  : (SIGNAL_RUN_FIRST, TYPE_NONE, ()),
        'pause' : (SIGNAL_RUN_FIRST, TYPE_NONE, ()),
        'next'  : (SIGNAL_RUN_FIRST, TYPE_NONE, ()),
        'prev'  : (SIGNAL_RUN_FIRST, TYPE_NONE, ()),
        
        'volume_up'   : (SIGNAL_RUN_FIRST, TYPE_NONE, ()),
        'volume_down' : (SIGNAL_RUN_FIRST, TYPE_NONE, ())
    }
    
    def __init__(self, gx_tray_icon):
        BaseController.__init__(self)
        
        self.popup = gx_tray_icon.get_widget("popUpWindow")
        self.text1 = gx_tray_icon.get_widget("text1")
        self.text2 = gx_tray_icon.get_widget("text2")
         
        self.icon = gtk.StatusIcon()
        self.icon.set_tooltip("Foobnix music playerEngine")
        # TODO: move the path to config
        icon_path = "/usr/local/share/pixmaps/foobnix.png"
        if os.path.exists(icon_path):
            self.icon.set_from_file(icon_path)
        else:
            self.icon.set_from_stock("gtk-media-play")
        
        self.icon.connect("activate",   lambda *a: self.emit('toggle_window_visibility'))
        self.icon.connect("popup-menu", lambda *a: self.popup.show())
        try:
            self.icon.connect("scroll-event", self.on_mouse_wheel_scrolled)
        except:
            pass

        popup_signals = {
                "on_close_clicked" : lambda *a: self.emit('exit'),
                "on_play_clicked"  : lambda *a: self.emit('play'),
                "on_pause_clicked" : lambda *a: self.emit('pause'),
                "on_next_clicked"  : lambda *a: self.emit('next'),
                "on_prev_clicked"  : lambda *s: self.emit('prev'),
                "on_cancel_clicked": lambda *a: self.popup.hide()
        }
        gx_tray_icon.signal_autoconnect(popup_signals)

        
    def setText1(self, text):
        self.text1.set_text(text)
    
    def setText2(self, text):
        self.text2.set_text(text)

    def on_mouse_wheel_scrolled(self, w, event):
        if event.direction == gtk.gdk.SCROLL_UP:    #@UndefinedVariable
            self.emit('volume_up')
        else:
            self.emit('volume_down')
        # TODO: move next line to player_controller 
        # self.playerWidgets.volume.set_value(volume * 100)
