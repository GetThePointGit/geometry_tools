
import sys
import os.path
import numpy as np

sys.path.append('C:\\Users\\basti\\.qgis2\\python\\plugins\\ThreeDiToolbox\\external\\netCDF4-win64')

from netCDF4 import Dataset


def compress_tdi_results(source_filepath, dest_filepath, variables=None):

    with Dataset(source_filepath, mode='r', format='NETCDF4') as sf:
        with Dataset(dest_filepath, mode='w', format='NETCDF4') as df:

            # copy dimensions
            for sdim in sf.dimensions.values():
                print sdim.name
                ddim = df.createDimension(sdim.name, len(sdim) if not sdim.isunlimited() else None)

            # copy variables
            for svar in sf.variables.values():
                print 'Variable: ' + svar.name
                if variables is None or svar.name in variables or svar.name in ['time']:

                    if svar.dtype == np.float64:
                        datatype = np.float32
                    else:
                        datatype = svar.dtype

                    dvar = df.createVariable(svar.name, datatype, svar.dimensions, zlib=True)

                    # Copy variable attributes

                    # dvar.setncatts({k: svar.getncattr(k) for k in svar.ncattrs()})

                    print len(svar.ncattrs())

                    for k in svar.ncattrs():

                        print k
                        print svar.getncattr(k)
                        if k == 'coordinates':
                            dvar.setncatts({k: svar.getncattr(k) for k in svar.ncattrs()})


    return True





source_filepath = os.path.join(r'C:\Users\basti\.qgis2\python\plugins\legger\tests\data\Marken\results_3di.nc')
dest_filepath = os.path.join(r'C:\Users\basti\.qgis2\python\plugins\legger\tests\data\Marken\results_3di_compressed.nc')

compress_tdi_results(source_filepath, dest_filepath)


