#!/usr/bin/python
#coding: utf-8

import i3ipc
import sys
import getopt

from gi.repository import Gdk
from operator import itemgetter

# Return a dictionary with the output and its workspaces


def active_workspaces(workspaces):
    active_workspaces = {}
    allmonitors = []

    gdkdsp = Gdk.Display.get_default()
    for i in range(gdkdsp.get_n_monitors()):
        monitor = gdkdsp.get_monitor(i)
        scale = monitor.get_scale_factor()
        geo = monitor.get_geometry()
        allmonitors.append([
            monitor.get_model()] + [n * scale for n in [geo.x, geo.y, geo.width, geo.height]])

    order_monitors = sorted(allmonitors, key=itemgetter(1, 2))

    for monitor in order_monitors:
        list = []
        for w in workspaces:
            if w.output == monitor[0]:
                if w.num in list:
                    pass
                else:
                    list.append(w)

        active_workspaces[monitor[0]] = list

    return active_workspaces

# Swap workspaces between outputs


def swap_outputs(i3, outputs, workspaces, reverse=False, focus=False):

    active = active_workspaces(workspaces)
    keys_list = list(active.keys())

# Selecting the direction of rotation
    if reverse:
        reverse_keys_list = []

        for i in reversed(keys_list):
            reverse_keys_list.append(i)

        keys_list = reverse_keys_list

# Swap outputs
    for r in range(len(keys_list)):
        for w in active[keys_list[r]]:
            i3.command("workspace number " + str(w.num))
            if r < len(keys_list) - 1:
                i3.command("move workspace to output " + keys_list[r+1])
            else:
                i3.command("move workspace to output " + keys_list[0])
            print("number " + str(w.num))

    for w in workspaces:
        if w.visible:
            i3.command("workspace number " + str(w.num))
    for w in workspaces:
        if focus and w.focused:
            i3.command("workspace number " + str(w.num))
            break
    for o in outputs:
        for w in i3.get_workspaces():
            if o.primary and w.visible and focus == False:
                i3.command("workspace number " + str(w.num))
                sys.exit()


def main(argv):

    i3 = i3ipc.Connection()
    workspaces = i3.get_workspaces()
    outputs = i3.get_outputs()

    if len(active_workspaces(workspaces)) == 1:
        sys.exit()

    if len(sys.argv) == 1:
        swap_outputs(i3, outputs, workspaces)

    try:
        opts, args = getopt.getopt(argv, "rf")

    except getopt.GetoptError:
        print("\n[!] Invalid option!!")

    for opt, args in opts:
        if opt in ("-r"):
            swap_outputs(i3, outputs, workspaces, reverse=True)
        elif opt in ("-f"):
            swap_outputs(i3, outputs, workspaces, focus=True)


if __name__ == '__main__':

    main(sys.argv[1:])
