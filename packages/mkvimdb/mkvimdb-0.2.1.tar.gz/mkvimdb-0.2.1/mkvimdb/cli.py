"""Console script for mkvimdb."""
import sys
import os
from optparse import OptionParser
import mkvimdb.mkvimdb as mi


def main(argv=None):
    """
    Console script for mkvimdb.
    """
    program_name = os.path.basename(sys.argv[0])
    program_version = "all"
    program_build_date = "%s" % 2020

    program_version_string = '%%prog %s (%s)' % (program_version,
                                                 program_build_date)
    program_longdesc = '''MKV tags from IMDB info, interactively or not.'''

    program_license = '''Copyright 2020 Dimitry Dukhovny'''

    if argv is None:
        argv = sys.argv[1:]
    try:
        # setup option parser
        parser = OptionParser(version=program_version_string,
                              epilog=program_longdesc,
                              description=program_license)
        parser.add_option("-v", "--verbose", dest="verbose",
                          action="store_true",
                          help="set verbosity level \
                          [default: %default]")
        parser.add_option("-I", "--interactive", dest="interactive",
                          action="store_true",
                          help="Select best match interactively instead of guessing. \
                          [default: %default]")
        parser.add_option("-s", "--search", dest="searchtitle",
                          action="store", type="string",
                          help="Set the search string. \
                          [default: %default]")
        parser.add_option("-y", "--year", dest="searchyear",
                          action="store", type="string",
                          help="Set the likely release year. \
                          [default: %default]")
        parser.add_option("-o", "--outputdir", dest="output_dir",
                          action="store", type="string",
                          help="Set the output directory, if any. \
                          [default: %default]")
        parser.add_option("-g", "--genre", dest="extragenre",
                          action="store", type="string",
                          help="Add comma-separated genre list. \
                          [default: %default]")
        parser.add_option("-G", "--replace-genre", dest="replacegenre",
                          action="store", type="string",
                          help="Replace discovered genre. \
                          [default: %default]")
        parser.add_option("-T", "--replace-title", dest="replacetitle",
                          action="store", type="string",
                          help="Replace discovered title. \
                          [default: %default]")

        # set defaults
        parser.set_defaults(verbose=False)
        parser.set_defaults(interactive=False)
        parser.set_defaults(searchtitle='Pulp Fiction')
        parser.set_defaults(searchyear='1994')
        parser.set_defaults(output_dir='')
        parser.set_defaults(extragenre='')
        parser.set_defaults(replacegenre='')
        parser.set_defaults(replacetitle='')

        # process options
        (opts, args) = parser.parse_args(argv)

        if opts.extragenre:
            opts.extragenre = opts.extraganre.replace(",", ", ")
        if opts.replacegenre:
            opts.replacegenre = opts.replaceganre.replace(",", ", ")

    except:
        return(2)

    m = mi.moviecursor(
        title=opts.searchtitle,
        year=opts.searchyear,
        output_dir=opts.output_dir,
        extragenre=opts.extragenre,
        replacegenre=opts.replacegenre,
        replacetitle=opts.replacetitle,
        interactive=opts.interactive,
        verbose=opts.verbose)

if __name__ == "__main__":
    sys.exit(main(sys.argv))  # pragma: no cover
