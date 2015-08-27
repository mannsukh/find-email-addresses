#!/usr/bin/env python
import sys
import urllib2
import re
from urlparse import urlparse, urlsplit
import argparse
import pdb

from bs4 import BeautifulSoup


# write unit tests

# Start class FindEmailAddresses
class FindEmailAddresses(object):
    # Class Constants for success and failure to be used as exit codes
    SUCCESS = 0
    FAILED = 3

    PARSER = 'lxml'

    def __init__(self):
        self.url = ''
        self.emails = []
        self.hrefs = []
        self.mailTos = []
        self.discoveredPages = []
        self.openedPages = []
        parser = argparse.ArgumentParser(description='Find email addresses from the given domain.')
        parser.add_argument('domain', type=str, help='A domain name for the file to parse and find email addresses')
        args = parser.parse_args()
        # Convert argparse.NameSpace to dict and remove empty arguments
        args_dict = vars(args)
        for key in args_dict.keys():
            if args_dict[key] is None:
                del args_dict[key]

        self.args_dict = args_dict

    def createUrl(self, url):
        # Parse the url to get netloc and path to check if the url belongs to the input domain, else add it
        # to make the relative url a complete one with domain
        # if command line domain (jana.com) is equal to url jana.com
        if self.args_dict['domain'] is not url:
            # if command line domain jana.com does NOT match url twitter.com/signup
            if re.search(self.args_dict['domain'], url) is None:
                parsed = urlparse(url)
                if not bool(parsed.netloc):
                    url = self.args_dict['domain'] + '/' + url

        if re.match(r"http", url) is None:
            url = 'http://' + url
        return url

    @staticmethod
    def getDomain(url):
        """
        Static method to get domain out of a given link
        :param url: Link given to parse the domain
        :return: domain from the given url
        """
        domain = (urlsplit(url)[1] and urlsplit(url)[1].split('.') or urlsplit(url)[2].split('.'))
        if domain[0].lower() == 'www':
            domain = domain[1:]
        return '.'.join(domain)

    def openUrl(self, url):
        """
        Opens the url using library urllib2 and calls the soupify routine
        :param url: link that needs to be opened and then soupified
        """
        try:
            conn = urllib2.urlopen(url)
            # Collect all the pages open
            self.openedPages.append(url)
            self.soupify(conn)
        except Exception:
            pass
            #print 'Cannot open url or invalid domain name %s' % url

    def soupify(self, conn):
        """
        Uses the BeautifulSoup library to read text from the conn object
        :param conn: Object returned by the urllib2 library when opening the url
        """
        soup = None
        try:
            soup = BeautifulSoup(conn.read(), self.PARSER)
        except Exception as e:
            print 'Failed, BeautifulSoup issue %s:' % e

        if soup:
            # find all discoverable pages/links
            self.hrefs = soup.find_all('a', href=True)

            if self.hrefs:
                for href in self.hrefs:
                    if bool(href.attrs['href']):
                        url = self.createUrl(href.attrs['href'])
                        parsed = urlparse(url)
                        if bool(parsed.netloc):
                            # if domain matches the link then append to discoveredPages as we will use it later
                            # if the domain does not match then we skip them as we do not want to parse other domains
                            if re.search(self.args_dict['domain'], parsed.netloc) is not None:
                                self.discoveredPages.append(url)

            # find all mailto (email) tags elements and store in self.emails list data structure
            self.mailTos = soup.select('a[href^=mailto]')
            for i in self.mailTos:
                if bool(i.string):
                    self.emails.append(i.string.encode('utf-8').strip())

            # Use regular expressions to get emails out of general text appearing on browser
            if bool(soup.get_text()):
                # Regular expression to read email addresses
                textEmails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", soup.get_text(), re.I)
                # find all email addresses and store in self.emails list data structure
                for i in textEmails:
                    self.emails.append(i.encode('utf-8').strip())

    def getEmailAddresses(self):
        """
        Loops through the discovered pages in the command line domain
        Prints the list of email addresses found using this class; FindEmailAddresses

        """
        if self.discoveredPages:
            for discoveredPage in self.discoveredPages:
                if not discoveredPage in self.openedPages:
                    self.openUrl(discoveredPage)

        # Create a unique list of email addresses found in the domain
        uniqueList = set(self.emails)
        # Output to the screen
        if uniqueList:
            print 'Found these email addresses:'
            for email in uniqueList:
                print email
        else:
            print 'No email addresses found at %s' % self.args_dict['domain']


# END class FindEmailAddresses

def main():
    """
    Main function to create the FindEmailAddresses object
    Calls the required routines to process the given domain and get email addresses.
    :return: bool; Success or Failure
    """
    findEmailAddresses = FindEmailAddresses()

    parsed = urlparse(findEmailAddresses.args_dict['domain'])
    # if parsed.scheme is empty, http:// is missing we need to prepend that to the args.url
    if not parsed.scheme:
        findEmailAddresses.url = findEmailAddresses.createUrl(findEmailAddresses.args_dict['domain'])

    try:
        findEmailAddresses.openUrl(findEmailAddresses.url)
    except Exception:
        print 'Find email addresses failed. Please try again.'
        return findEmailAddresses.FAILED

    findEmailAddresses.getEmailAddresses()
    return findEmailAddresses.SUCCESS


if __name__ == "__main__":
    # Call the main method
    sys.exit(main())

    # END: if __name__ == "__main__":
