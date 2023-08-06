from fido.fido import Fido

def get_puid(path):
    '''
    Get the PUID for a file.
    '''
    odif.identify_file(path)
    puid = odif.last_puid
    odif.last_puid = None
    return puid


class Odif(Fido):
    """
    A class that extends Fido to stash the PUID of the last matched file on an 
    object property.
    """

    def print_matches(self, filename, matches, duration, match_type=''):
        puid = None
        if len(matches) > 0:
            puid = self.get_puid(matches[0][0])
        self.last_puid = puid


# create Fido once so PRONOM XML isn't parsed every time get_puid is called
odif = Odif(quiet=True, nocontainer=True)

