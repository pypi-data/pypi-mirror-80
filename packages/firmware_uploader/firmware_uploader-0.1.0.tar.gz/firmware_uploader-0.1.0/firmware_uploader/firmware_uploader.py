import sre_yield

try:
    from pkg_resources import get_distribution, DistributionNotFound
    _dist = get_distribution('firmware_uploader')
    # Normalize case for Windows systems
    dist_loc = os.path.normcase(_dist.location)
    here = os.path.normcase(__file__)
    if not here.startswith(os.path.join(dist_loc, 'firmware_uploader')):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except (ImportError,DistributionNotFound):
    __version__ = None
else:
    __version__ = _dist.version


class FirmwareUploader(object):
    '''
    Uploads firmware to multiple embedded devices.

    Example Usage:

    '''

    def __init__(self,*args,**kwargs):
        pass

# -----------------------------------------------------------------------------------------
if __name__ == '__main__':

    debug = False
    dev = FirmwareUploader(debug=debug)
