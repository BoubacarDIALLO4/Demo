#!/usr/bin/env python
import os
import subprocess


def main():
    """
    Send the command on the standard output to launch it in the next task with ansible
    :return: String
    """
    os.environ["DISPLAY"] = ":0"
    connected_screens_list = subprocess.check_output(['xrandr | grep -A 1 -w connected | sed -e \'s/--//g\''],
                                                     shell=True)

    screens_information_lines = list(filter(str.strip, connected_screens_list.split("\n")))

    mirroring_command = "xrandr"

    os.system(command_iterator(mirroring_command, build_screens_dict(screens_information_lines)))


def build_screens_dict(lines):
    """
    That function builds a dictionary that contains for each screen (key) a specific resolution (value)
    :param lines:
    :return: dict with a resolution for each screen
    """
    screens = dict()

    for i in range(0, len(lines), +2):
        screen = lines[i].split(' ')[0]
        resolution = lines[i + 1].split(' ')[3]
        screens[screen] = resolution

    return screens


def command_iterator(final_command, screens):
    """
    That function is parsing the dictionary in order to build the command with the right parameters for each screen
    :param final_command:
    :param screens:
    :return: the final command to execute in the next task in ansible
    """
    first = True
    for key, value in screens.items():
        if first:
            if "1920x1080" in value:
                final_command += " --output " + key + " --mode " + value
            else:
                final_command += " --output " + key + " --mode " + value + " --scale-from 1920x1080"
        else:
            if "1920x1080" in value:
                final_command += " --output " + key + " --mode " + value + " --same-as " + list(screens.keys())[0]
            else:
                final_command += " --output " + key + " --mode " + value + " --scale-from 1920x1080" + \
                                 " --same-as " + list(screens.keys())[0]
        first = False
    return final_command


if __name__ == "__main__":
    main()
