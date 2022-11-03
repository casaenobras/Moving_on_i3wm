# i3-between_screens

This Python3 script is ideal for multi-screen setups with the i3wm window manager.  
No matter what monitor settings you have, you can shift the focus to the monitor from up/down/left/right  
to the workspace that is currently visible, with your preferred keyboard shortcut.  

It should also work with the Sway window manager, though it hasn't been tested.

### Table of Contents
- [](#)
    - [Table of Contents](#table-of-contents)
- [Performance](#performance)
    - [Parameters:](#parameters)
- [Installation](#installation)
- [Requirements](#requirements)

# Performance

### Parameters:
+ **-r**    Move focus to screen right.
+ **-l**    Move focus to screen left.
+ **-u**    Move focus to screen up.
+ **-d**    Move focus to screen down.

# Installation

Clone this repository, go into the directory and give execute permissions to the file **i3-left_right_workspace.py**.

~~~
git clone https://github.com/casaenobras/Moving_on_i3wm
cd Moving_on_i3wm/between_screens
chmod +x i3-between_screens.py
~~~

Open the i3wm configuration file (usually located in **~/.3/config** or **~/.config/i3/config**) with your favorite editor. For example **vim**.  
~~~
vim ~/.config/i3/config
~~~

Add these lines
~~~
#navigate workspaces next / previous
bindsym $mod+Ctrl-Right workspace next
bindsym $mod+Ctrl-Left workspace previous

bindsym $mod+Ctrl+Shift+Left exec /<Script Path>/i3-between_screens.py -l
bindsym $mod+Ctrl+Shift+Right exec /<Script Path>/i3-between_screens.py -r
bindsym $mod+Ctrl+Shift+Up exec /<Script Path>/i3-between_screens.py -u
bindsym $mod+Ctrl+Shift+Down exec /<Script Path>/i3-between_screens.py -d
~~~

Save the config file and reload your i3wm (by default `Mod+Shift+c` and then `Mod+Shift+r`) for the changes to take effect. 


# Requirements

See requirements.txt or execute

~~~
pip install -r requirements.txt
~~~