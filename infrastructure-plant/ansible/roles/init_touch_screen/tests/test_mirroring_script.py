from roles.init_touch_screen.files.mirroring_script import build_screens_dict, command_iterator


class TestMirroringScript:

    def test_build_screens_dict_shoud_return_only_id_screen_and_resolution(self):
        # Given
        lines = ["DP-0 connected (normal left inverted right x axis y axis)",
                 "   1280x1024     60.02 +",
                 "DP-2 connected primary 1920x1080+0+0 (normal left inverted right x axis y axis) 435mm x 239mm",
                 "   1920x1080     60.00*+  59.94    50.00"]
        expected = {"DP-0": "1280x1024",
                    "DP-2": "1920x1080"}

        # When
        result = build_screens_dict(lines)

        # Then
        assert expected == result

    def test_mirroring_script_should_configure_two_screens_when_detected(self):
        # Given
        final_command = "xrandr"
        screens = {"DP-0": "1920x1080",
                   "DP-1": "1300x1200"}

        expected = "xrandr --output DP-0 --mode 1920x1080 --output DP-1 --mode 1300x1200 --scale-from 1920x1080 " \
                   "--same-as DP-0"

        # When
        result = command_iterator(final_command, screens)

        # Then
        assert expected == result

    def test_mirroring_script_should_configure_four_screens_when_detected(self):
        # Given
        final_command = "xrandr"
        screens = {"DP-0": "1235x1080",
                   "DP-1": "1300x1200",
                   "DP-2": "1920x1080",
                   "DP-3": "1600x1200"}

        expected = "xrandr --output DP-0 --mode 1235x1080 --scale-from 1920x1080 --output DP-1 --mode 1300x1200 " \
                   "--scale-from 1920x1080 --same-as DP-0 --output DP-2 --mode 1920x1080 --same-as DP-0 " \
                   "--output DP-3 --mode 1600x1200 --scale-from 1920x1080 --same-as DP-0"

        # When
        result = command_iterator(final_command, screens)

        # Then
        assert expected == result
