#!/usr/bin/python
#coding: utf-8

import i3ipc
import sys
import getopt
import gi

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
from operator import itemgetter


def unordered_list(i3):
    unordered_list = []
    allmonitors = []

    gdkdsp = Gdk.Display.get_default()
    for i in range(gdkdsp.get_n_monitors()):
        monitor = gdkdsp.get_monitor(i)
        scale = monitor.get_scale_factor()
        geo = monitor.get_geometry()
        allmonitors.append([
            monitor.get_model()] + [n * scale for n in [geo.x, geo.y]])

    order_monitors = sorted(allmonitors, key=itemgetter(1, 2))

    for monitor in order_monitors:
        for w in i3.get_workspaces():
            if w.output == monitor[0]:
                unordered_list.append(w.num)

    return unordered_list


def focused(i3):
    for w in i3.get_workspaces():
        if w.focused:
            focused = w.num

    return focused


def workspace_left(i3, unordered_list, focused):
    if unordered_list.index(focused) == 0:
        new_focused = unordered_list[-1]
    else:
        new_focused = unordered_list[unordered_list.index(focused) - 1]

    i3.command("workspace number" + str(new_focused))


def workspace_right(i3, unordered_list, focused):
    if unordered_list.index(focused) == len(unordered_list) - 1:
        new_focused = unordered_list[0]
    else:
        new_focused = unordered_list[unordered_list.index(focused) + 1]

    i3.command("workspace number " + str(new_focused))


def main(argv):

    i3 = i3ipc.Connection()

    if len(sys.argv) == 1:
        print("[!] Add parameters: '-l' for left o '-r' for right")

    try:
        opts, args = getopt.getopt(argv, "lr")

    except getopt.GetoptError:
        print("\n[!] Invalid option!!")

    for opt, args in opts:
        if opt in ("-l"):
            workspace_left(i3, unordered_list(i3), focused(i3))
        elif opt in ("-r"):
            workspace_right(i3, unordered_list(i3), focused(i3))
        else:
            sys.exit(1)


if __name__ == '__main__':

    main(sys.argv[1:])
