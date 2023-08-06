#
#The tool processed a dataset in input [ds]  and return some statistics in netcdf format:
#
#descriptive.Processer(ds, output_path) has the following modules:
#
#- _mean
#- _min
#- _max
#_ _95p
##
#
#Each module apply the statistics required by resampling the dataset at different timescale:#
##
#
#- overall
#- seasonal: the seasons are so defined DJF, MAM, JJA, SON
#- monthly
#- yearly

