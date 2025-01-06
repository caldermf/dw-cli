# A tiny deep work tracker for the command line

## Installation instructions

1. Make sure you have Python 3.13 or newer installed. You can download it [here](https://www.python.org/downloads/).
2. Make sure [pip](https://pip.pypa.io/en/stable/installation/) is installed by using Terminal to run
	which pip3
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
	