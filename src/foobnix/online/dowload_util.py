'''
Created on Jun 10, 2010

@author: ivan
'''
from foobnix.util.configuration import FConfiguration
from foobnix.util import LOG
import os
import urllib
import thread
from foobnix.online.song_resource import update_song_path


def dowload_song_thread(song):
    thread.start_new_thread(download_song, (song,))
    
def save_song_thread(song):
    thread.start_new_thread(save_song, (song,))

def save_as_song_thread(song, path):
    thread.start_new_thread(save_as_song, (song,path,))
    

def save_song(song):    
    update_song_path(song)
    file = get_file_store_path(song)
    LOG.debug("Download song start", file)
    if not os.path.exists(file + ".tmp"):
        LOG.debug("Song PATH", song.path)
        urllib.urlretrieve(song.path, file + ".tmp")
        os.rename(file + ".tmp", file)        
        LOG.debug("Download song finished", file)
    else:
        LOG.debug("Found file already dowloaded", file)


def save_as_song(song, path):
    update_song_path(song)
    file = path +  "/" + song.name + ".mp3"
    LOG.debug("Store song path", file)
    if not os.path.exists(file + ".tmp"):
        urllib.urlretrieve(song.path, file + ".tmp")
        os.rename(file + ".tmp", file)        
        LOG.debug("Download song finished", file)
    else:
        LOG.debug("Found file already dowloaded", file)

"""Dowload song proccess"""
def download_song(song):
    if not FConfiguration().is_save_online:
        LOG.debug("Saving (Caching) not enable")
        return None    
    save_song(song)
    pass

"""Determine file place"""
def get_file_store_path(song):
        dir = FConfiguration().onlineMusicPath
        if song.getArtist():
            dir = dir + "/" + song.getArtist()
        make_dirs(dir)
        song = dir + "/" + song.name + ".mp3"
        return song
    
def make_dirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)
            