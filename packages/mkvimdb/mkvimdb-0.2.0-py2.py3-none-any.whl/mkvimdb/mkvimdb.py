"""Main module."""

import locale
import sys
from imdb import IMDb
from collections import OrderedDict
import mkvimdb.tagify as tagify
import mkvimdb.imdbops as imdbops


def ERR(outstring):
    """
    Stupid stderr printer.  Don't mock me.
    """
    sys.stderr.write(str(outstring) + '\n')


class moviecursor:
    """
    ETL heavy lifter class that coordinates among the transformations.
    """
    def __init__(
            self, title='Pulp Fiction',
            year='1994',
            output_dir='',
            extragenre='',
            replacegenre='',
            replacetitle='',
            interactive=False,
            verbose=False):
        """
        constructor for moviecursor()
        ETL heavy lifter class that coordinates among the transformations.
        """
        self.title = title
        self.year = year
        self.output_dir = output_dir
        self.extragenre = extragenre
        self.replacegenre = replacegenre
        self.replacetitle = replacetitle
        self.interactive = interactive
        self.verbose = verbose
        self.data = {}
        self.tagdata = OrderedDict()
        self.tagdata['TITLE'] = ''
        self.tagdata['ARTIST'] = ''
        self.tagdata['DIRECTOR'] = ''
        self.tagdata['ALBUM_ARTIST'] = ''
        self.tagdata['PLOT'] = ''
        self.tagdata['COMMENTARY'] = ''
        self.tagdata['DESCRIPTION'] = ''
        self.tagdata['DATE_RELEASED'] = ''
        self.tagdata['GENRE'] = ''
        self.searchstring = "%s (%s)" % (self.title, self.year)
        self.makecursor()
        self.matchingnames()
        self.pickone()
        self.genout()
        self.overrides()
        self.spit()
    def makecursor(self):
        """
        Just returns a connection object to IMDB from the blessed imdb module.
        """
        self.c = IMDb()
    def matchingnames(self):
        """
        Calls the search with its own parameters.
        """
        self.matches = imdbops.matchingnames(self.c, self.searchstring)
    def pickone(self):
        """
        Uses the search resutls from self.matchingnames() to pick a winner.
        """
        self.entry = imdbops.pickone(
            self.matches,
            self.title,
            self.year,
            self.interactive,
            self.verbose)
        self.entry = self.c.get_movie(self.entry.getID())
    def genout(self):
        """
        Navigates the IMDB object definition to get meat for our tags.
        """
        self.tagdata.update(imdbops.genout(self.entry))
    def overrides(self):
        """
        Implement commandline overrides as specified in the help text.
        """
        if self.replacegenre:
            self.tagdata['GENRE'] = self.replacegenre
        if self.extragenre:
            self.tagdata['GENRE'] = self.extragenre + ', ' + self.tagdata['GENRE']
        if self.replacetitle:
            self.tagdata['TITLE'] = self.replacetitle
    def spit(self):
        """
        Generate output to disk, if specified or to STDOUT if not.
        """
        if self.output_dir:
            with open(self.tagdata['filename'] + '.xml', 'w') as FH:
                FH.write(tagify.givexml(self.tagdata))
        else:
            print(tagify.givexml(self.tagdata))


