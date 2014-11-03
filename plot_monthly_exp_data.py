from matplotlib import cm
from matplotlib.colors import BoundaryNorm
from rpn.domains.rotated_lat_lon import RotatedLatLon

__author__ = 'huziy'


varname_to_nlevs = {
    "TBAR": 3,
     "SNO": 1
}


def do_seasonal_2d_plots(exp_name="", data_folder=""):
    """
    :param exp_name: name of the experiment
    """
    for vname, nlevs in varname_to_nlevs:

        pass


import os
from rpn.rpn import RPN
import matplotlib.pyplot as plt
import numpy as np
import sys


def plot_variable(varname, data, img_folder="", lons=None, lats=None, bmap=None, limit_levels=None):

    """

    :param varname:
    :param data:
    :param img_folder:
    :param lons:
    :param lats:
    :param bmap:
    :param limit_levels: If only first n levels are needed then set it to n, otherwise leave it None
    """
    dates = data.keys()
    dates_sorted = list(sorted(dates))
    start_date = dates_sorted[0]
    start_year, start_month = start_date.year, start_date.month
    x, y = bmap(lons, lats)
    current_month = start_month
    current_year = start_year

    #Create image folder if necessary
    if not os.path.isdir(img_folder):
        os.mkdir(img_folder)


    nclevs = 60
    cmap = cm.get_cmap("jet", lut=nclevs)
    clevels = None
    for d in dates_sorted:
        levs_sorted = sorted(data.items()[0][1].keys())
        for i, lev in enumerate(levs_sorted):

            if limit_levels is not None:
                #only plot selected number of levels
                if i >= limit_levels:
                    break

            fig = plt.figure()
            ax = plt.gca()
            field = data[d][lev]

            print type(field)
            field = np.ma.masked_where(np.abs(field) < 1e-10, field)

            ##Mask very small differences for temperature
            if varname in ["TBAR", "I0"]:
                field = np.ma.masked_where(np.abs(field) < 0.01, field)


            if varname in ["SNO", ]:
                field = np.ma.masked_where(np.abs(field) > 999, field)

                #specify levels for the differences
                if field.min() * field.max() < 0:
                    clevels = [-300, -250, -200, -150, -100, -80, -50, -20, -10, -5, -1]
                    clevels += [-c for c in reversed(clevels)]
                    cmap = cm.get_cmap("seismic", lut=len(clevels) - 1)
                else:
                    clevels = [1, 5, 10, 20, 50, 80, 100, 150, 200, 250, 300]


            im = bmap.contourf(x, y, field, cmap=cmap, ax=ax, levels=clevels)
            bmap.colorbar(im)
            bmap.drawcoastlines(linewidth=0.3, ax=ax)

            plt.title("{}: {}/{}".format(varname, current_month, current_year))
            fig.savefig("{}/{}_{}{:02d}_{}.png".format(img_folder, varname, current_year, current_month, lev))
            plt.close(fig)

        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1




def plot_all(folder_path="", limit_levels=1):

    if folder_path == "":
        folder_path = sys.argv[1]

    for f in os.listdir(folder_path):
        #skip files other than monthly
        if not "monthly_fields.rpn" in f.lower():
            continue


        r = RPN(os.path.join(folder_path, f))

        #Exclude coordinate variables
        vlist = [v for v in r.get_list_of_varnames() if v not in ["^^", ">>"]]

        #remove coordinates from the list
        for varname in vlist:
            data = r.get_4d_field(name=varname)
            img_folder = os.path.join(folder_path, "img")
            params = r.get_proj_parameters_for_the_last_read_rec()
            rll = RotatedLatLon(**params)
            lons, lats = r.get_longitudes_and_latitudes_for_the_last_read_rec()
            plot_variable(varname, data, img_folder=img_folder,
                          lons=lons, lats=lats,
                          bmap=rll.get_basemap_object_for_lons_lats(lons2d=lons, lats2d=lats),
                          limit_levels=limit_levels)


def main():
    plot_all(folder_path="")

if __name__ == '__main__':
    main()
