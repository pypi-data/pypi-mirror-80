"""Main module."""

import locale
import sys
from imdb import IMDb
from collections import OrderedDict
import mkvimdb.tagify as tagify
import mkvimdb.imdbops as imdbops


def ERR(outstring):
        sys.stderr.write(str(outstring) + '\n')


class moviecursor:
    def __init__(
            self, title='Pulp Fiction',
            year='1994',
            output_dir='',
            extragenre='',
            replacegenre='',
            replacetitle='',
            interactive=False,
            verbose=False):
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
        self.c = IMDb()
    def matchingnames(self):
        self.matches = imdbops.matchingnames(self.c, self.searchstring)
    def pickone(self):
        self.entry = imdbops.pickone(
            self.matches,
            self.title,
            self.year,
            self.interactive,
            self.verbose)
        self.entry = self.c.get_movie(self.entry.getID())
    def genout(self):
        self.tagdata.update(imdbops.genout(self.entry))
    def overrides(self):
        if self.replacegenre:
            self.tagdata['GENRE'] = self.replacegenre
        if self.extragenre:
            self.tagdata['GENRE'] = self.extragenre + ', ' + self.tagdata['GENRE']
        if self.replacetitle:
            self.tagdata['TITLE'] = self.replacetitle
    def spit(self):
        if self.output_dir:
            with open(self.tagdata['filename'] + '.xml', 'w') as FH:
                FH.write(tagify.givexml(self.tagdata))
        else:
            print(tagify.givexml(self.tagdata))


