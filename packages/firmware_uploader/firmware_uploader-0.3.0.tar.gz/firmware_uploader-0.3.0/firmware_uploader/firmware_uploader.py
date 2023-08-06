import os
import click
import sre_yield
import tempfile
import subprocess
from pathlib import Path

try:
    from pkg_resources import get_distribution, DistributionNotFound
    _dist = get_distribution('firmware_uploader')
    # Normalize case for Windows systems
    dist_loc = os.path.normcase(_dist.location)
    here = os.path.normcase(__file__)
    if not here.startswith(os.path.join(dist_loc,'firmware_uploader')):
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

    def __init__(self,environment,dry_run,firmware_url,upload_ports,*args,**kwargs):
        self.environment = environment
        self.dry_run = dry_run
        self.firmware_url = firmware_url
        self.upload_ports = upload_ports
        if isinstance(self.upload_ports,str):
            self.upload_ports = list(sre_yield.AllStrings(self.upload_ports))

    def _output(self,args):
        if not self.dry_run:
            subprocess.run(args)
        else:
            print(args)

    def run(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            tmpdirpath = Path(tmpdirname)
            os.chdir(tmpdirpath)
            subprocess.run(['git','clone',self.firmware_url],check=True)
            repository_name = Path(self.firmware_url).name
            tmpdirpath /= repository_name
            os.chdir(tmpdirpath)
            for upload_port in self.upload_ports:
                if self.environment is not None:
                    if 'teensy' in self.environment:
                        # teensy loader ignores --upload-port, so must manually
                        # put into bootloader mode by setting baud of port
                        # before uploading
                        self._output(['stty','-F',upload_port,'134'])
                    self._output(['pio','run','-e',self.environment,'--target','upload','--upload-port',upload_port])
                else:
                    self._output(['pio','run','--target','upload','--upload-port',upload_port])


@click.command()
@click.option('-e','--environment')
@click.option('-d','--dry-run', is_flag=True)
@click.argument('firmware_url')
@click.argument('upload_ports_re')
def cli(environment,dry_run,firmware_url,upload_ports_re):
    upload_ports = list(sre_yield.AllStrings(upload_ports_re))

    print('Environment: {0}'.format(environment))
    print('Dry Run: {0}'.format(dry_run))
    print('Firmware URL: {0}'.format(firmware_url))
    print('Upload ports: {0}'.format(upload_ports))

    if click.confirm('Do you want to continue?', abort=True):
        fu = FirmwareUploader(environment,dry_run,firmware_url,upload_ports)
        fu.run()

# -----------------------------------------------------------------------------------------
if __name__ == '__main__':
    cli()
