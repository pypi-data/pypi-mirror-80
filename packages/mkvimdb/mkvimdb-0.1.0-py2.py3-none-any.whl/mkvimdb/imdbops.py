"""IMDB operations module."""

import locale
import sys
import string
from imdb import IMDb


def ERR(outstring):
        sys.stderr.write(str(outstring) + '\n')


def genout(filmentry):
    outdict={}
    kind = filmentry.get('kind')
    try:
        director = ', '.join(map(lambda x: x['name'], filmentry['directors']))
    except:
        try:
            director = ', '.join(map(lambda x: x['name'], filmentry['director']))
        except:
            director = ''
    outdict['DIRECTOR'] = director
    outdict['ALBUM_ARTIST'] = director
    try:
        directorscanon = '-'.join(map(lambda x: x['canonical name'].replace(" ","").lower(), filmentry['directors']))
    except:
        try:
            directorscanon = '-'.join(map(lambda x: x['canonical name'].replace(" ","").lower(), filmentry['director']))
        except:
            directorscanon = 'unknown'
    outdict['directorscanon'] = directorscanon
    outdict['ARTIST'] = ', '.join(map(lambda x: x['name'], filmentry['actors'][0:3]))
    try:
        plot = filmentry['plot outline']
    except:
        try:
            plot = filmentry['plot']
        except:
            try:
                plot = filmentry['synopsis']
            except:
                plot = ''
    outdict['PLOT'] = plot
    outdict['COMMENTARY'] = plot
    outdict['DESCRIPTION'] = plot
    outdict['GENRE'] = ', '.join(filmentry['genre'])
    year = str(filmentry['year'])
    outdict['DATE_RELEASED'] = year
    outdict['TITLE'] = "%s %s" % (filmentry['canonical title'], year)
    titlecanon = filmentry['smart canonical title'].lower().replace(" ","_")
    outdict['titlecanon'] = titlecanon
    if kind == "episode":
        try:
            digits = len(str(filmentry.get('number of episodes')))
        except:
            digits = 2
        outdict['SERIES'] = filmentry.get('smart canonical series title')
        outdict['seriescanon'] = outdict['SERIES'].lower().replace(" ","_")
        outdict['season'] = filmentry.get('season')
        outdict['episode'] = filmentry.get('episode')
        filetemplate = "%s-S%02dE%0" + str(digits) + "d-%s"
        titletemplate = "S%02dE%0" + str(digits) + "d %s"
        outdict['TITLE'] = titletemplate % (int(outdict['season']), int(outdict['episode']), outdict['TITLE'])
        outdict['filename'] = filetemplate % (
            outdict['seriescanon'],
            int(outdict['season']),
            int(outdict['episode']),
            outdict['titlecanon'])
    else:
        outdict['filename'] = "%s-%s-%s" % (directorscanon, titlecanon, year)
    outdict['filename'] = ''.join(nchar for nchar in outdict['filename'] if nchar in string.printable)
    badchars='''\/:*?"<>'|~'''
    for nchar in badchars:
        outdict['filename'] = outdict['filename'].replace(nchar,'_')

    return(outdict)

def pickone(matches, title, year, interactive, verbose):
    acceptablekinds = ['movie', 'episode', 'video movie', 'tv miniseries']
    if not matches:
        return(None)
    else:
        candidates = []
        for entry in matches:
            try:
                entrykind = entry.get('kind')
                entrytitle = entry.get('smart long imdb canonical title')
                entryyear = entry.get('year')
            except:
                pass
            if entrykind in acceptablekinds:
                if entrytitle == title and entryyear == int(year):
                    if verbose:  ERR("Found an exact match for %s" % (entrytitle))
                    candidates.insert(0, entry)
                elif title in entrytitle and abs(entryyear - int(year)) <= 1:
                    if verbose:  ERR("Found a close match with %s" % (entrytitle))
                    candidates.insert(1, entry)
                else:
                    if verbose:  ERR("Found a poor match with %s" % (entrytitle))
                    candidates.append(entry)
            else:
                if verbose:  ERR("Skipping %s named %s" % (entrykind, entrytitle))
        if candidates:
            if interactive and len(candidates)>0:
                ERR("Pick the number that matches \"%s\" from \"%s\"" % (title, year))
                for index in range(len(candidates)):
                    entrykind = candidates[index].get('kind')
                    title = candidates[index].get('smart long imdb canonical title')
                    year = candidates[index].get('year')
                    ERR("%d :  %s :  %s %d" % (index, entrykind, title, year))
                choice = input('?:  ')
                try:
                    choice = int(choice)
                except:
                    ERR("Going with the first choice, then.")
                    choice = 0
                if choice >= len(candidates):
                    choice = None
                chosen = candidates.pop(choice)
                ERR("Picked %s from %s" % (chosen.get('smart long imdb canonical title'), chosen.get('year')))
                return(chosen)
            else:
                return(candidates[0])
        else:
            return(None)


def matchingnames(cursor, searchstring):
    '''Search IMDB for a particular movie.'''
    return(cursor.search_movie(str(searchstring)))


