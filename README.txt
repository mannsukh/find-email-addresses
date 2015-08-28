# find-email-addresses
Website scrapper for email addresses in Python
Steps to install FindEmailAddresses.py

1. Make sure you install python 2.7, this is developed on a machine running Python 2.7

2. If pip is not installed on your machine, please do so.
2.1. sudo apt-get install python-pip

3. If BeautifulSoup library is not installed on your machine, please do so.
3.1. sudo pip install beautifulsoup4
3.2. sudo pip install PyQt4

If the above command does not work then use yum or apt-get or the appropriate command for your *nix distribution. For example, if using Ubuntu 14.04 LTS OS, use the following command
sudo apt-get install python-beautifulsoup

4. Save file named find_email_addresses.py in a location on your computer.
Run the following command to set PYTHONPATH, export PYTHONPATH=/path/to/the/file
Check that the PYTHONPATH is set correctly by typing: echo $PYTHONPATH, the terminal should show the folder path of where your file is.

5. Sometimes the output shows :
QFont::setPixelSize: Pixel size <= 0 (0)
- This is due to a bug in PyQt4 and this bug has been fixed with PyQt5, but PyQt5 is for Python3 and it is not backwards compatible. So leaving the issue as-is.

6. Output:
$ python find_email_addresses.py jana.com
Found these email addresses:
press@jana.com
info@jana.com
sales@jana.com
msingh@msingh-Precision-M4700:~$
