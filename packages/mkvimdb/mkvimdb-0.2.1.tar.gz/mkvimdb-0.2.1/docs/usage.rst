=====
Usage
=====

To use mkvimdb in a project::

    import mkvimdb

From the commandline::

    Usage: mkvimdb [options]

    Options:
    --version             show program version number and exit
    -h, --help            show this help message and exit
    -v, --verbose         set verbosity level
                          [default: False]
    -I, --interactive     Select best match interactively instead of guessing.
                          [default: False]
    -s SEARCHTITLE, --search=SEARCHTITLE
                          Set the search string.
                          [default: Pulp Fiction]
    -y SEARCHYEAR, --year=SEARCHYEAR
                          Set the likely release year.
                          [default: 1994]
    -o OUTPUT_DIR, --outputdir=OUTPUT_DIR
                          Set the output directory, if any.
                          [default: ]
    -g EXTRAGENRE, --genre=EXTRAGENRE
                          Add comma-separated genre list.
                          [default: ]
    -G REPLACEGENRE, --replace-genre=REPLACEGENRE
                          Replace discovered genre.
                          [default: ]
    -T REPLACETITLE, --replace-title=REPLACETITLE
                          Replace discovered title.
                          [default: ]
    MKV tags from IMDB info, interactively or not.

