# A tiny deep work tracker for the command line

## Installation instructions

1. Make sure you have Python 3.13 or newer installed. You can download it [here](https://www.python.org/downloads/).
2. Make sure [pip](https://pip.pypa.io/en/stable/installation/) is installed by using Terminal to run
```
which pip3
```
if it doesn't work, try
```
which pip
```
and use whichever one works for the remainder of the installation. It should come automatically with Python, but if it doesn't, you can use the link above for installation instructions.
3. Clone this repository, or alternatively just download the "whl" file contained within it. Copy the path to the whl file to your clipboard (you can use option-click in finder to copy path names). It should look something like my path:
```
/Users/caldermf/Documents/dw-cli/dw-0.1.0-py3-none-any.whl
```
4. Run the following in Terminal, replacing my path with your path:
```
pip3 install --user /Users/caldermf/Documents/dw-cli/dw/dist/dw-0.1.0-py3-none-any.whl --break-system-packages
```
5. You will probably get something along the lines of the following warning
```
WARNING: The script dw is installed in '/Users/caldermf/Library/Python/3.13/bin' which is not on PATH.
Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
```
6. Copy the path in the warning, and run the following in Terminal, replacing my path with your new path which you just copied.
```
echo 'export PATH="$PATH:/Users/caldermf/Library/Python/3.13/bin"' >> ~/.bashrc
```
7. Run the following:
```
open -e ~/.zshrc
```
A file will open in TextEdit. Add
```
source ~/.bashrc
```
to this file, and save it.

8. Restart Terminal. Now run
```
dw --help
```
and you should see a list of commands. You're ready to go!

## Using the app

Start by running
```
dw init
```
and then choose a folder in which to store your deep work data. I recommend putting it in Dropbox or iCloud or something because you're going to want to hold on to this deep work data for as long as you live.

After you do that, I hope that running
```
dw --help
```
and then examining the available commands should be pretty self-explanatory. To almost any command, you can add a date. Dates are always in YYYY-MM-DD format. Durations are always in minutes. For example, to add 30 minutes to the work you did on New Year's Eve 2024, you would write
```
dw add 30 --date 2024-12-31
```
Try setting a daily goal, e.g. for 4hrs per day, you would write
```
dw goal 240
```
Of course you can use
```
dw go
```
and
```
dw stop
```
to start and stop a session.
```
dw status
```
and
```
dw day
```
should be your "go-to" functionalities for monitoring your deep work "in action."
Weekly and yearly views are available too. The week starts on Monday and ends on Sunday, and this is non-negotiable.