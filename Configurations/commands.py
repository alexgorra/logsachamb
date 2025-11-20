from Configurations import settings


COMMANDS_X = {
    "x_minus_10": f"$J=G91 X-10 F{settings.X_JOG_FEEDRATE}",
    "x_minus_1":  f"$J=G91 X-1 F{settings.X_JOG_FEEDRATE}",
    "x_minus_0_1": f"$J=G91 X-0.1 F{settings.X_JOG_FEEDRATE}",
    "x_minus_0_02": f"$J=G91 X-0.02 F{settings.X_JOG_FEEDRATE}",
    "x_plus_0_02": f"$J=G91 X0.02 F{settings.X_JOG_FEEDRATE}",
    "x_plus_0_1":  f"$J=G91 X0.1 F{settings.X_JOG_FEEDRATE}",
    "x_plus_1":    f"$J=G91 X1 F{settings.X_JOG_FEEDRATE}",
    "x_plus_10":   f"$J=G91 X10 F{settings.X_JOG_FEEDRATE}",
}

COMMANDS_Y = {
    "y_minus_10": f"$J=G91 Y-10 F{settings.Y_JOG_FEEDRATE}",
    "y_minus_1":  f"$J=G91 Y-1 F{settings.Y_JOG_FEEDRATE}",
    "y_minus_0_1": f"$J=G91 Y-0.1 F{settings.Y_JOG_FEEDRATE}",
    "y_minus_0_02": f"$J=G91 Y-0.02 F{settings.Y_JOG_FEEDRATE}",
    "y_plus_0_02": f"$J=G91 Y0.02 F{settings.Y_JOG_FEEDRATE}",
    "y_plus_0_1":  f"$J=G91 Y0.1 F{settings.Y_JOG_FEEDRATE}",
    "y_plus_1":    f"$J=G91 Y1 F{settings.Y_JOG_FEEDRATE}",
    "y_plus_10":   f"$J=G91 Y10 F{settings.Y_JOG_FEEDRATE}",
}

COMMANDS_A = {
    "a_minus_10": f"$J=G91 A-10 F{settings.A_JOG_FEEDRATE}",
    "a_minus_1":  f"$J=G91 A-1 F{settings.A_JOG_FEEDRATE}",
    "a_minus_0_1": f"$J=G91 A-0.1 F{settings.A_JOG_FEEDRATE}",
    "a_minus_0_02": f"$J=G91 A-0.02 F{settings.A_JOG_FEEDRATE}",
    "a_plus_0_02": f"$J=G91 A0.02 F{settings.A_JOG_FEEDRATE}",
    "a_plus_0_1":  f"$J=G91 A0.1 F{settings.A_JOG_FEEDRATE}",
    "a_plus_1":    f"$J=G91 A1 F{settings.A_JOG_FEEDRATE}",
    "a_plus_10":   f"$J=G91 A10 F{settings.A_JOG_FEEDRATE}",
}

COMMANDS_SPECIAL = {
    "save_zero": "G10 P1 L20 X0 Y0 A0",
    "save_zero_session": "G92 X0 Y0 A0",
    "home_all": "$H",
    "home_x": "$HX",
    "home_y": "$HY",
    "home_a": "$HA",
    "home_all": "$H",
    "goto_zero": "X0 Y0 A0",
    "CONNECT": "CONNECT",
    "DISCONNECT": "DISCONNECT",
}




