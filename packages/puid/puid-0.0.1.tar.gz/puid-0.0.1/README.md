# puid

*puid* provides a function to get the [PRONOM] Unique Identifier for a file. It's
just a small wrapper around the much more complicated and feature rich [fido].

    >>> from puid import get_puid
    >>> get_puid('file.jpg')
    'fmt/42'

puid was created largely for instructional purposes to help students identify
files in their own Python programs. You will want to use [fido] directly if you
need to identify files in containers like zip files, or do anything other than
to get a single PUID for a file.

[PRONOM]: http://www.nationalarchives.gov.uk/PRONOM/
[fido]: https://github.com/openpreserve/fido
