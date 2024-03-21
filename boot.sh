#!/usr/bin/bash

script="$( realpath $( dirname "${BASH_SOURCE[0]}" ) )/dogo.py"
chmod +x $script

crontab -l > mycron 2>/dev/null
echo "00 08 * * * .$script" >> mycron
crontab mycron
rm mycron

exit 0
