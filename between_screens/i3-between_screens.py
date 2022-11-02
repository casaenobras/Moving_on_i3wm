#!/usr/bin/python
#coding: utf-8

import i3ipc
import sys
import getopt

from gi.repository import Gdk
from operator import itemgetter


def workspaces_list(i3):
    allmonitors = []
    workspaces_list = []

    gdkdsp = Gdk.Display.get_default()
    for i in range(gdkdsp.get_n_monitors()):
        monitor = gdkdsp.get_monitor(i)
        scale = monitor.get_scale_factor()
        geo = monitor.get_geometry()
        allmonitors.append([
            monitor.get_model()] + [n * scale for n in [geo.x, geo.y]])

    order_monitors = sorted(allmonitors, key=itemgetter(2, 1))

    for monitor in order_monitors:
        for w in i3.get_workspaces():
            if w.output == monitor[0]:
                workspaces_list.append([w.num, monitor[1], monitor[2]])
    return workspaces_list


def focused(i3, workspaces_list):

    for w in i3.get_workspaces():
        if w.focused:
            focus = w.num
            break

    for w in workspaces_list:
        if w[0] == focus:
            focused = w

    return focused


def workspace_left(i3, workspaces_list, focused):

    workspaces_row = []

    for i in workspaces_list:
        if i[2] == focused[2]:
            workspaces_row.append(i[0])

    for w in i3.get_workspaces():
        if w.visible == False and w.num in workspaces_row:
            workspaces_row.remove(w.num)

    if workspaces_row.index(focused[0]) == 0:
        new_focused = workspaces_row[-1]
    else:
        new_focused = workspaces_row[workspaces_row.index(focused[0]) - 1]

    i3.command("workspace number" + str(new_focused))


def workspace_right(i3, workspaces_list, focused):

    workspaces_row = []

    for i in workspaces_list:
        if i[2] == focused[2]:
            workspaces_row.append(i[0])

    for w in i3.get_workspaces():
        if w.visible == False and w.num in workspaces_row:
            workspaces_row.remove(w.num)

    if workspaces_row.index(focused[0]) == len(workspaces_row) - 1:
        new_focused = workspaces_row[0]
    else:
        new_focused = workspaces_row[workspaces_row.index(focused[0]) + 1]

    i3.command("workspace number" + str(new_focused))


def workspace_up(i3, workspaces_list, focused):

    workspaces_column = []

    for w in workspaces_list:
        if w[0] == focused[0]:
            workspaces_column.append(w[0])
        elif focused[2] != w[2]:
            workspaces_column.append(w[0])

    for w in i3.get_workspaces():
        if w.visible == False and w.num in workspaces_column:
            workspaces_column.remove(w.num)

    if workspaces_column.index(focused[0]) == 0:
        new_focused = workspaces_column[-1]
    else:
        new_focused = workspaces_column[workspaces_column.index(
            focused[0]) - 1]

    i3.command("workspace number" + str(new_focused))


def workspace_down(i3, workspaces_list, focused):

    workspaces_column = []

    for w in workspaces_list:
        if w[0] == focused[0]:
            workspaces_column.append(w[0])
        elif focused[2] != w[2]:
            workspaces_column.append(w[0])

    for w in i3.get_workspaces():
        if w.visible == False and w.num in workspaces_column:
            workspaces_column.remove(w.num)

    if workspaces_column.index(focused[0]) == len(workspaces_column) - 1:
        new_focused = workspaces_column[0]
    else:
        new_focused = workspaces_column[workspaces_column.index(
            focused[0]) + 1]

    i3.command("workspace number" + str(new_focused))


def main(argv):

    i3 = i3ipc.Connection()

    if len(sys.argv) == 1:
        print(
            "[!] Add parameters: '-l' for left, '-r' for right, '-u' for up or '-d' for down")

    try:
        opts, args = getopt.getopt(argv, "lrud")

    except getopt.GetoptError:
        print("\n[!] Invalid option!!")

    for opt, args in opts:
        if opt in ("-l"):
            workspace_left(i3, workspaces_list(
                i3), focused(i3, workspaces_list(i3)))
        elif opt in ("-r"):
            workspace_right(i3, workspaces_list(
                i3), focused(i3, workspaces_list(i3)))
        elif opt in ("-u"):
            workspace_up(i3, workspaces_list(
                i3), focused(i3, workspaces_list(i3)))
        elif opt in ("-d"):
            workspace_down(i3, workspaces_list(
                i3), focused(i3, workspaces_list(i3)))
        else:
            sys.exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])
