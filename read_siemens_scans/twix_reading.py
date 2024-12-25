import twixtools
from collections import OrderedDict
from read_siemens_scans.config import DIM_DESCRIPTION
import json


class Dimensions(OrderedDict):
    def __init__(self, d):
        super().__init__(d)

    def print(self):
        print(json.dumps(self, indent=4))



def read_raw_twix_data(twix_path: str, fix_oversampling: bool = False):
    """

    :param twix_path:           TWIX (.dat) file path.
    :param fix_oversampling:    Enable handling of oversampling.
    :return:
    """
    assert twix_path.endswith('.dat')

    twix = twixtools.read_twix(twix_path, keep_syncdata=True, keep_acqend=True)
    mapped = twixtools.map_twix(twix)
    kspace = mapped[-1]['image']
    kspace.flags['remove_os'] = fix_oversampling
    dim_keys = list(kspace._dim_order)
    active_image_dims = Dimensions(
        (DIM_DESCRIPTION[dim_keys[dim]], kspace.shape[dim]) for dim in range(kspace.ndim) if kspace.shape[dim] > 1
    )
    kspace_squeezed = kspace[:].squeeze()
    return kspace_squeezed, active_image_dims








if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from matplotlib import use
    from read_siemens_scans.recon import adjoint_recon, adjoint_recon_fix_aspect_ratio
    use('TkAgg')

    file = '/mnt/c/Users/along/Downloads/meas_MID00210_FID12025_pulseq.dat'
    kspace_data, dim_data = read_raw_twix_data(file, fix_oversampling=False)
    images = adjoint_recon(kspace_data, dim_data)
    images_interp, _ = adjoint_recon_fix_aspect_ratio(kspace_data, dim_data)
    breakpoint()

