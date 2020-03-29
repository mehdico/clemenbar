# !/usr/bin/python3
# coding=utf-8

import rumps
import threading
from clementineremote import ClementineRemote

clementine = ClementineRemote(host="127.0.0.1", port=5500, auth_code=None, reconnect=True)


class ClemenbarApp(rumps.App):
    def __init__(self):
        super(ClemenbarApp, self).__init__("Clemenbar", "Title")
        tail(self)

    @rumps.clicked("Play/Pause")
    def playPause(self, _):
        clementine.playpause()
        self.title = getTitle()

    @rumps.clicked("Next")
    def next(self, _):
        clementine.next()

    @rumps.clicked("Prev")
    def prev(self, _):
        clementine.previous()

def getTitle():
    defaultTitle = "Clemenbar"
    if clementine is None:
        return defaultTitle
    state = clementine.state
    if state is not None and state == "Paused":
        return defaultTitle

    currentTrack = clementine.current_track
    if currentTrack is None:
        return defaultTitle
    if "title" in currentTrack.keys() and currentTrack["title"] is not None:
        if "track_artist" in currentTrack.keys() and currentTrack["track_artist"] is not None:
            return currentTrack["title"] + ' - ' + currentTrack["track_artist"]
        else:
            return currentTrack["title"]
    if "filename" in currentTrack.keys() and currentTrack["filename"] is not None:
        return currentTrack["filename"]

    return defaultTitle


def tail(self):
    threading.Timer(3, tail, [self, ]).start()
    self.title = getTitle()


ClemenbarApp().run()
