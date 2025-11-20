#!/usr/bin/env python3
"""
Simple CLI for Anechoic Chamber control
Inspired by uno6_minimal.m MATLAB API

Usage:
  python chamber.py move 10 20 45      # Move to X=10, Y=20, A=45
  python chamber.py home               # Home all axes
  python chamber.py home x             # Home X only
  python chamber.py jog x 5            # Jog X by +5 degrees
  python chamber.py zero               # Set current position as (0,0,0)
  python chamber.py status             # Get current position
"""

import sys
import asyncio
import httpx


SERVER_URL = "http://10.128.3.114:8000"


async def send(cmd):
    """Send command to server and return response"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{SERVER_URL}/cmd/{cmd}")
            return response.json()
    except (httpx.ConnectError, httpx.TimeoutException):
        print("Error: Server offline")
        sys.exit(1)


async def move(x, y, a):
    """Absolute move to X, Y, A (degrees)"""
    cmd = f"G0 X{x} Y{y} A{a}"
    print(f"Moving to X={x}, Y={y}, A={a}")
    result = await send(cmd)
    print(f"Response: {result}")
    return result


async def home(axis="all"):
    """Home axes (all, x, y, or a)"""
    axis = axis.lower()
    if axis == "all":
        cmd = "$H"
    elif axis == "x":
        cmd = "$HX"
    elif axis == "y":
        cmd = "$HY"
    elif axis == "a":
        cmd = "$HA"
    else:
        print(f"Unknown axis: {axis}")
        sys.exit(1)
    
    print(f"Homing {axis.upper()}...")
    result = await send(cmd)
    print(f"Response: {result}")
    return result


async def jog(axis, delta):
    """Relative move (jog) on specified axis"""
    axis = axis.upper()
    delta = float(delta)
    
    if axis == "X":
        cmd = f"$J=G91 X{delta} F1000"
    elif axis == "Y":
        cmd = f"$J=G91 Y{delta} F1000"
    elif axis == "A":
        cmd = f"$J=G91 A{delta} F1000"
    else:
        print(f"Unknown axis: {axis}")
        sys.exit(1)
    
    print(f"Jogging {axis} by {delta:+.2f}°")
    result = await send(cmd)
    print(f"Response: {result}")
    return result


async def zero():
    """Set current position as (0,0,0)"""
    cmd = "G10 P1 L20 X0 Y0 A0"
    print("Setting current position as zero (0,0,0)")
    result = await send(cmd)
    print(f"Response: {result}")
    return result


async def status():
    """Get current status/position"""
    result = await send("?")
    print(f"Status: {result}")
    return result


def usage():
    print(__doc__)
    sys.exit(1)


async def main():
    if len(sys.argv) < 2:
        usage()
    
    command = sys.argv[1].lower()
    
    if command == "move":
        if len(sys.argv) != 5:
            print("Usage: chamber.py move <x> <y> <a>")
            sys.exit(1)
        x, y, a = float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
        await move(x, y, a)
    
    elif command == "home":
        axis = sys.argv[2] if len(sys.argv) > 2 else "all"
        await home(axis)
    
    elif command == "jog":
        if len(sys.argv) != 4:
            print("Usage: chamber.py jog <axis> <delta>")
            print("Example: chamber.py jog x 5")
            sys.exit(1)
        axis = sys.argv[2]
        delta = sys.argv[3]
        await jog(axis, delta)
    
    elif command == "zero":
        await zero()
    
    elif command == "status":
        await status()
    
    else:
        print(f"Unknown command: {command}")
        usage()


if __name__ == "__main__":
    asyncio.run(main())
