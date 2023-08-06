import os
from glob import glob
import numpy as np
import xarray as xr



seasonLabel={'MAM':'Spring','JJA':'Summer','DJF':'Winter','SON':'Autumn'}
seasonIndex=['DJF','MAM','JJA','SON']
monthIndex=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Now','Dec']


class Trend():
    def __init__(self, exp_outpath,mask_pval=True):
        self.exp_outpath = exp_outpath
        self.mask_pval=mask_pval

    def manage_output(self, inputType):
        exp_outpath = self.exp_outpath

        self.outpath_trend_seasons = os.path.join(exp_outpath, f"trend_seasons_{inputType}")
        self.outpath_trend_months= os.path.join(exp_outpath, f"trend_months_{inputType}")
        self.outpath_trend_days = os.path.join(exp_outpath, f"trend_days_{inputType}")
        self.outpath_trend_global = os.path.join(exp_outpath, f"trend_global_{inputType}")

        checkOutdir(self.outpath_trend_seasons)
        checkOutdir(self.outpath_trend_months)
        checkOutdir(self.outpath_trend_days)
        checkOutdir(self.outpath_trend_global)

    def manage_input(self,inputType):
        self.stat_seasons = os.path.join(self.exp_outpath, f"seasons_{inputType}")
        print (self.stat_seasons)
        self.stat_month = os.path.join(self.exp_outpath, f"months_{inputType}")
        self.stat_daily = os.path.join(self.exp_outpath, f"daily_{inputType}")

    def _seasons(self,input_type):
        output_type = 'trend_seasons'
        print (f'*** processing {output_type} ***')
        self.manage_output(input_type)
        self.manage_input(input_type)
        for variable in ['hs', 'tp']:
            print (variable)
            seasons_ds = xr.open_mfdataset(glob(f"{self.stat_seasons}/seasonal*.nc"), combine='by_coords')
            for season in [0,1,2,3]:
                print (seasonIndex[season])
                outfile_seasons = os.path.join(self.outpath_trend_seasons, f'{variable}_{seasonIndex[season]}.npy')
                if not os.path.exists(outfile_seasons):
                    time_selection=range(season,len(seasons_ds.time.data),4)
                    #print(time_selection,seasons_ds[variable].time)
                    if variable == 'tp':
                        #print (seasons_ds[variable].isel(time=time_selection).data.shape)
                        seasons_regression = self.mannKendall(seasons_ds['t01'].isel(time=time_selection).data.compute())
                    else:
                        seasons_regression = self.mannKendall(
                            seasons_ds[variable].isel(time=time_selection).data.compute())
                        if input_type == 'mean':
                            np.save(os.path.join(self.outpath_trend_seasons, f'dir_{seasonIndex[season]}.npy'), seasons_ds.dir.isel(time=time_selection).mean('time').data)

                    np.save(outfile_seasons, seasons_regression)
    def _days(self,input_type):
        output_type = 'trend_days'
        print (f'*** processing {input_type} ***')
        self.manage_output(input_type)
        self.manage_input(input_type)
        for variable in ['hs', 'tp']:
            print (variable)
            outfile_days = os.path.join(self.outpath_trend_days, f'{variable}_days.npy')
            if not os.path.exists(outfile_days):
                days = xr.open_mfdataset(glob(f"{self.stat_daily}/*.nc"), combine='by_coords')
                if variable == 'tp':
                    days_regression = self.mannKendall(days['t01'].data.compute())
                else:
                    days_regression = self.mannKendall(days[variable].data.compute())
                    if input_type == 'mean':
                        np.save(os.path.join(self.outpath_trend_days, f'dir_days.npy'),
                            days.dir.mean('time').data)
                np.save(outfile_days,days_regression)

    def _months(self,input_type):
        output_type = 'trend_months'
        print (f'*** processing {input_type} ***')
        self.manage_output(input_type)
        self.manage_input(input_type)
        for variable in ['hs', 'tp']:
            print (variable)
            months_ds = xr.open_mfdataset(glob(f"{self.stat_month}/months*.nc"), combine='by_coords')
            for month in range(12):
                print (monthIndex[month])
                outfile_months = os.path.join(self.outpath_trend_months, f'{variable}_{monthIndex[month]}.npy')
                if not os.path.exists(outfile_months):
                    time_selection=range(month,len(months_ds.time.data),12)
                    if variable=='tp':
                        months_regression = self.mannKendall(months_ds['t01'].isel(time=time_selection).data.compute())
                    else:
                        months_regression = self.mannKendall(
                            months_ds[variable].isel(time=time_selection).data.compute())
                        if input_type == 'mean':
                            np.save(os.path.join(self.outpath_trend_months, f'dir_{monthIndex[month]}.npy'),
                                months_ds.dir.isel(time=time_selection).mean('time').data)
                    np.save(outfile_months, months_regression)

    def _global(self,input_type):

        print (f'*** processing {input_type} ***')
        self.manage_output(input_type)
        self.manage_input(input_type)
        for variable in ['hs', 'tp']:
            print (variable)
            months_ds = xr.open_mfdataset(glob(f"{self.stat_month}/months*.nc"), combine='by_coords')
            outfile_glob = os.path.join(self.outpath_trend_global, f'{variable}_global.npy')
            if not os.path.exists(outfile_glob):
                    if variable=='tp':
                        months_regression = self.mannKendall(months_ds['t01'].data.compute())
                    else:
                        months_regression = self.mannKendall(
                            months_ds[variable].data.compute())
                        if input_type=='mean':
                            np.save(os.path.join(self.outpath_trend_months, f'dir_global.npy'),
                                months_ds.dir.mean('time').data)
                    np.save(outfile_glob, months_regression)

    def mannKendall(self,data_to_plot):
        return linearRegression3D(data_to_plot).mannKendall(maskpvalue=self.mask_pval)