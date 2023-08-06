import numpy as np
from napari_sentinel_zip.napari_sentinel_zip import reader_function


def test_read_write():
    zipfn = "/media/draga/My Passport/pepsL2A_zip_img/55HBU"
    data = reader_function(zipfn)

if __name__ == "__main__":
    test_read_write()