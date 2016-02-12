# i3-dispatch
Allows i3 to move focus differently depending on the focused window.

The goal of this script is to control applications that create tabs themselves (rather then letting the window manager do it) with the same bindings 
then the WM's.
For instance, if you are focusing a vim terminal with 2 splits, your WM bindings will allow you to move between splits.


Pull requests welcome at https://github.com/teto/i3-dispatch

Works in pair with the vim plugin https://github.com/teto/nvim-wm


#How to use ?
In your i3 configuration, you can replace (some of) your focus bindings by these:
```
# This may be slow since script involves a few steps
# so you should keep one set of focus bindings that don't use i3dispatch "just in case"
bindsym $mod+h exec 3dispatch left
bindsym $mod+j exec 3dispatch down
bindsym $mod+k exec 3dispatch up
bindsym $mod+l exec 3dispatch right

# alternatively, you can use the cursor keys:
bindsym $mod+Left  exec i3dispatch left
bindsym $mod+Down  exec i3dispatch down
bindsym $mod+Up    exec i3dispatch up
bindsym $mod+Right exec i3dispatch right

```
