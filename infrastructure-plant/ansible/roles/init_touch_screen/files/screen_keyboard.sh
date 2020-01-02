## Enables screen keyboard everytime a user logs in from GUI

if [ "$DISPLAY" != "" ]
then
        DISPLAY=$DISPLAY gsettings set org.gnome.desktop.a11y.applications screen-keyboard-enabled true
fi
