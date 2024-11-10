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


def get_ordered_workspaces(i3):
    """Gets an ordered list of workspace numbers based on monitor position."""
    workspace_list = []
    monitors = []

    # Get monitor information
    gdkdsp = Gdk.Display.get_default()
    for i in range(gdkdsp.get_n_monitors()):
        monitor = gdkdsp.get_monitor(i)
        scale = monitor.get_scale_factor()
        geo = monitor.get_geometry()
        monitors.append([monitor.get_model()] + [n * scale for n in [geo.x, geo.y]])

    # Sort monitors by position
    ordered_monitors = sorted(monitors, key=itemgetter(1, 2))

    # Get workspaces in order
    for monitor in ordered_monitors:
        for workspace in i3.get_workspaces():
            if workspace.output == monitor[0]:
                workspace_list.append(workspace.num)

    return workspace_list


def get_focused_workspace(i3):
    """Gets the number of the currently focused workspace."""
    return next((w.num for w in i3.get_workspaces() if w.focused), None)


def move_to_workspace(i3, workspace_num):
    """Changes to the specified workspace."""
    try:
        i3.command(f"workspace number {workspace_num}")
        logging.info(f"Changed to workspace {workspace_num}")
    except Exception as e:
        logging.error(f"Error changing workspace: {e}")


def workspace_left(i3, workspace_list, current):
    """Changes to the workspace on the left."""
    current_index = workspace_list.index(current)
    new_index = -1 if current_index == 0 else current_index - 1
    move_to_workspace(i3, workspace_list[new_index])


def workspace_right(i3, workspace_list, current):
    """Changes to the workspace on the right."""
    current_index = workspace_list.index(current)
    new_index = 0 if current_index == len(workspace_list) - 1 else current_index + 1
    move_to_workspace(i3, workspace_list[new_index])


def main(argv):
    i3 = i3ipc.Connection()

    if len(sys.argv) == 1:
        logging.error("Usage: Add '-l' for left or '-r' for right")
        sys.exit(1)

    try:
        opts, args = getopt.getopt(argv, "lr")
        workspace_list = get_ordered_workspaces(i3)
        current_workspace = get_focused_workspace(i3)

        if not workspace_list or current_workspace is None:
            logging.error("Could not get workspaces")
            sys.exit(1)

        for opt, _ in opts:
            if opt == "-l":
                workspace_left(i3, workspace_list, current_workspace)
            elif opt == "-r":
                workspace_right(i3, workspace_list, current_workspace)

    except getopt.GetoptError:
        logging.error("Invalid option")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
