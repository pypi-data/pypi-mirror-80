import xarray as xr
import os
from LRstats.utils import checkOutdir


class Processer:
    def __init__(self, ds, exp_outpath):
        self.ds = ds
        self.exp_outpath = exp_outpath

    def manage_output(self, inputType):
        exp_outpath = self.exp_outpath

        self.outpath_years = os.path.join(exp_outpath, f"years_{inputType}")
        self.outpath_global = os.path.join(exp_outpath, f"global_{inputType}")
        self.outpath_months = os.path.join(exp_outpath, f"months_{inputType}")
        self.outpath_seasons = os.path.join(exp_outpath, f"seasons_{inputType}")

        checkOutdir(self.outpath_years)
        checkOutdir(self.outpath_global)
        checkOutdir(self.outpath_months)
        checkOutdir(self.outpath_seasons)

    def _mean(self):

        ds=self.ds
        input_type = 'mean'
        print (f'*** processing {input_type} ***')
        self.manage_output(input_type)

        # global mean
        if not os.path.exists(os.path.join(self.outpath_global, f"{input_type}.nc")):
            ds.mean('time', skipna=True).to_netcdf(os.path.join(self.outpath_global, f"global_{input_type}.nc"))
        print(f'{input_type} global done')

        # annual mean
        if not os.path.exists(os.path.join(self.outpath_years, f"years_{input_type}.nc")):
            ds.groupby('time.year').mean('time').to_netcdf(os.path.join(self.outpath_years, f"years_{input_type}.nc"))

        print(f'{input_type} annual done')

        # month mean
        if not os.path.exists(os.path.join(self.outpath_months, f"months_{input_type}.nc")):
            ds.resample(time='1M').mean().to_netcdf(os.path.join(self.outpath_months, f"months_{input_type}.nc"))

        print(f'{input_type} monthly done')

        # seasonal mean
        if not os.path.exists(os.path.join(self.outpath_seasons, f"seasons_{input_type}.nc")):
            a= ds.resample(time="QS-DEC").mean()
            a.to_netcdf(
            os.path.join(self.outpath_seasons, f"seasons_{input_type}.nc"))

        print(f'{input_type} seasons done')

        print(f'{input_type} completed')

    def _min(self):
        ds=self.ds
        input_type = 'min'
        print (f'*** processing {input_type} ***')
        self.manage_output(input_type)

        # global min
        if not os.path.exists(os.path.join(self.outpath_global, f"{input_type}.nc")):
            ds.min('time', skipna=True).to_netcdf(os.path.join(self.outpath_global, f"{input_type}.nc"))

        print(f'{input_type} global done')

        # annual min
        if not os.path.exists(os.path.join(self.outpath_years, f"years_{input_type}.nc")):
            ds.groupby('time.year').min('time').to_netcdf(os.path.join(self.outpath_years, f"years_{input_type}.nc"))

        print(f'{input_type} annual done')

        # month min
        if not os.path.exists(os.path.join(self.outpath_months, f"months_{input_type}.nc")):
            ds.resample(time='1M').min().to_netcdf(os.path.join(self.outpath_months, f"months_{input_type}.nc"))
        print(f'{input_type} monthly done')

        # seasonal min
        if not os.path.exists(os.path.join(self.outpath_seasons, f"seasons_{input_type}.nc")):
            a= ds.resample(time="QS-DEC").min()
            a.to_netcdf(
            os.path.join(self.outpath_seasons, f"seasons_{input_type}.nc"))
        print(f'{input_type} seasons done')

        print(f'{input_type} completed')


    def _max(self):
        ds=self.ds
        input_type = 'max'
        print (f'*** processing {input_type} ***')
        self.manage_output(input_type)

        # global max
        if not os.path.exists(os.path.join(self.outpath_global, f"{input_type}.nc")):
            ds.max('time', skipna=True).to_netcdf(os.path.join(self.outpath_global, f"{input_type}.nc"))

        print(f'{input_type} global done')

        # annual max
        if not os.path.exists(os.path.join(self.outpath_years, f"years_{input_type}.nc")):
            ds.groupby('time.year').max('time').to_netcdf(os.path.join(self.outpath_years, f"years_{input_type}.nc"))

        print(f'{input_type} annual done')

        # month max
        if not os.path.exists(os.path.join(self.outpath_months, f"months_{input_type}.nc")):
            ds.resample(time='1M').max().to_netcdf(os.path.join(self.outpath_months, f"months_{input_type}.nc"))
        print(f'{input_type} monthly done')

        # seasonal max
        if not os.path.exists(os.path.join(self.outpath_seasons, f"seasons_{input_type}.nc")):
            a= ds.resample(time="QS-DEC").max()
            a.to_netcdf(
            os.path.join(self.outpath_seasons, f"seasons_{input_type}.nc"))
        print(f'{input_type} seasons done')

        print(f'{input_type} completed')

    def _95p(self):

        ds=self.ds
        input_type = '95p'
        print (f'*** processing {input_type} ***')
        self.manage_output(input_type)

        # global '95p'
        if not os.path.exists(os.path.join(self.outpath_global, f"{input_type}.nc")):
            ds.mean('time', skipna=True).to_netcdf(os.path.join(self.outpath_global, f"global_{input_type}.nc"))
            #ds.reduce(np.nanpercentile, dim='time', q=0.95).to_netcdf(os.path.join(self.outpath_global, f"{input_type}.nc"))

        print(f'{input_type} global done')

        # annual '95p'
        if not os.path.exists(os.path.join(self.outpath_years, f"years_{input_type}.nc")):
            ds.groupby('time.year').mean('time', skipna=True).to_netcdf(
                os.path.join(self.outpath_years, f"years_{input_type}.nc"))
            #ds.groupby('time.year').reduce(np.nanpercentile, dim='time', q=0.95).to_netcdf(os.path.join(self.outpath_years, f"years_{input_type}.nc"))

        print(f'{input_type} annual done')

        # month '95p'
        if not os.path.exists(os.path.join(self.outpath_months, f"months_{input_type}.nc")):
            ds.resample(time='1M').mean( dim='time',skipna=True).to_netcdf(os.path.join(self.outpath_months, f"months_{input_type}.nc"))
            #ds.resample(time='1M').reduce(np.nanpercentile, dim='time', q=0.95).to_netcdf(os.path.join(self.outpath_months, f"months_{input_type}.nc"))
        print(f'{input_type} monthly done')

        # seasonal '95p'
        if not os.path.exists(os.path.join(self.outpath_seasons, f"seasons_{input_type}.nc")):
            a = ds.resample(time="QS-DEC").mean(dim='time',skipna=True)
            a.to_netcdf(
            os.path.join(self.outpath_seasons, f"seasons_{input_type}.nc"))
        print(f'{input_type} seasonal done')

        print(f'{input_type} completed')


