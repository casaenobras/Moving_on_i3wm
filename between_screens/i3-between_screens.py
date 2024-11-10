#!/usr/bin/python
# coding: utf-8

import i3ipc
import sys
import getopt
import gi
import logging

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
from operator import itemgetter


def get_workspaces_list(i3):
    """Gets an ordered list of workspaces with their coordinates."""
    monitors = []
    workspaces_list = []

    # Get monitor information
    gdkdsp = Gdk.Display.get_default()
    for i in range(gdkdsp.get_n_monitors()):
        monitor = gdkdsp.get_monitor(i)
        scale = monitor.get_scale_factor()
        geo = monitor.get_geometry()
        monitors.append([
            monitor.get_model()] + [n * scale for n in [geo.x, geo.y]])

    # Sort monitors by position
    ordered_monitors = sorted(monitors, key=itemgetter(2, 1))

    # Get ordered workspaces
    for monitor in ordered_monitors:
        for workspace in i3.get_workspaces():
            if workspace.output == monitor[0]:
                workspaces_list.append([workspace.num, monitor[1], monitor[2]])
    return workspaces_list


def get_focused_workspace(i3, workspaces_list):
    """Gets the currently focused workspace."""
    focused_num = next((w.num for w in i3.get_workspaces() if w.focused), None)
    return next((w for w in workspaces_list if w[0] == focused_num), None)


def get_visible_workspaces_in_row(i3, workspaces_list, focused_y):
    """Gets visible workspaces in the same row."""
    workspaces_row = [w[0] for w in workspaces_list if w[2] == focused_y]
    return [w for w in workspaces_row if any(ws.num == w and ws.visible for ws in i3.get_workspaces())]


def get_visible_workspaces_in_column(i3, workspaces_list, focused_workspace):
    """Gets visible workspaces in the same column."""
    workspaces_column = [w[0] for w in workspaces_list if w[0] == focused_workspace[0] or focused_workspace[2] != w[2]]
    return [w for w in workspaces_column if any(ws.num == w and ws.visible for ws in i3.get_workspaces())]


def move_to_workspace(i3, workspace_num):
    """Changes to the specified workspace."""
    try:
        i3.command(f"workspace number {workspace_num}")
        logging.info(f"Changed to workspace {workspace_num}")
    except Exception as e:
        logging.error(f"Error changing workspace: {e}")


def workspace_left(i3, workspaces_list, focused):
    """Changes to the workspace on the left."""
    workspaces_row = get_visible_workspaces_in_row(i3, workspaces_list, focused[2])
    current_index = workspaces_row.index(focused[0])
    new_index = -1 if current_index == 0 else current_index - 1
    move_to_workspace(i3, workspaces_row[new_index])


def workspace_right(i3, workspaces_list, focused):
    """Changes to the workspace on the right."""
    workspaces_row = get_visible_workspaces_in_row(i3, workspaces_list, focused[2])
    current_index = workspaces_row.index(focused[0])
    new_index = 0 if current_index == len(workspaces_row) - 1 else current_index + 1
    move_to_workspace(i3, workspaces_row[new_index])


def workspace_up(i3, workspaces_list, focused):
    """Changes to the workspace above."""
    workspaces_column = get_visible_workspaces_in_column(i3, workspaces_list, focused)
    current_index = workspaces_column.index(focused[0])
    new_index = -1 if current_index == 0 else current_index - 1
    move_to_workspace(i3, workspaces_column[new_index])


def workspace_down(i3, workspaces_list, focused):
    """Changes to the workspace below."""
    workspaces_column = get_visible_workspaces_in_column(i3, workspaces_list, focused)
    current_index = workspaces_column.index(focused[0])
    new_index = 0 if current_index == len(workspaces_column) - 1 else current_index + 1
    move_to_workspace(i3, workspaces_column[new_index])


def main(argv):
    i3 = i3ipc.Connection()

    if len(sys.argv) == 1:
        logging.error("Usage: Add '-l' for left, '-r' for right, '-u' for up or '-d' for down")
        sys.exit(1)

    try:
        opts, args = getopt.getopt(argv, "lrud")
        workspaces = get_workspaces_list(i3)
        focused = get_focused_workspace(i3, workspaces)

        if not workspaces or not focused:
            logging.error("Could not get workspaces")
            sys.exit(1)

        for opt, _ in opts:
            if opt == "-l":
                workspace_left(i3, workspaces, focused)
            elif opt == "-r":
                workspace_right(i3, workspaces, focused)
            elif opt == "-u":
                workspace_up(i3, workspaces, focused)
            elif opt == "-d":
                workspace_down(i3, workspaces, focused)

    except getopt.GetoptError:
        logging.error("Invalid option")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])
