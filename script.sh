#!/bin/bash

gnome-terminal -- bash -c "python3 server.py; exec bash"
gnome-terminal -- bash -c "python3 client.py; exec bash"
gnome-terminal -- bash -c "python3 client.py; exec bash"
