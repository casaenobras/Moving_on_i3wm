# Moving_on_i3wm

Set of Python scripts oriented to multi-monitor configurations for i3wm.  
These scripts can work together if you want.  

It should also work with the Sway window manager, though it hasn't been tested.

# Scripts

## <ins>left_right_workspace</ins>

It is possible that you have the workspaces disordered on several monitors, when you use the keyboard shortcut `Mod+Ctrl+Left` or `Mod+Ctrl+Right`  
by default i3wm goes through the workspaces in numerical order with next / previous, that can cause the focus to change monitor several times  
until you reach the desired workspace even if you are on the same monitor.  
This script avoids this behavior and moves the focus to the left/right workspace regardless of the number assigned to it.  

Read the script README for more information.

## <ins>swap_monitors</ins>

Regardless of the multi-monitor configuration you have, this script will move all workspaces from one monitor to the next successively, causing monitors to swap.

Read the script README for more information.

## <ins>between_screens</ins>

Regardless of the multi-monitor configuration you have, now you can move between monitors quickly.
The focus will shift to the monitor from up/down/left/right with a keyboard shortcut to the visible workspace.  

Read the script README for more information.
