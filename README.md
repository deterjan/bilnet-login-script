# bilnet-login-script

This repository contains a python script and bash script for programmatic login to Bilnet. The scripts are only tested for wi-fi connection and may not work for ethernet.

## bash script

Can be found in `bilnet.sh`. Enter student ID and password in the script. This script is recommended for environments that don't have `python3` or the `requests` package installed. Keep request interval long as spamming login requests may trigger a temporary ban for your account or MAC address. 

Password is stored in plaintext. Use at your own risk.

## python script

Can be found in `bilnet.py`. Requires `python3` and the `requests` package. Enter student ID and password in the script or set `-i` and `-p` flags to manually input username and password. This script doesn't issue a login request if you are already connected to the internet. Use `python bilnet.py --help` to show options.

Password is stored in plaintext. Use at your own risk.
