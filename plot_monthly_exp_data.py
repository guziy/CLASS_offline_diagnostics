from matplotlib import cm

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


def plot_variable(varname, data, img_folder="", lons=None, lats=None, bmap=None):

    dates = data.keys()
    dates_sorted = list(sorted(dates))
    start_date = dates_sorted[0]
    start_year, start_month = start_date.year, start_date.month
    x, y = bmap(lons, lats)
    current_month = start_month
    current_year = start_year

    cmap = cm.get_cmap("jet", lut=20)
    for d in dates_sorted:
        levs_sorted = sorted(data.items[0][1].keys())
        for lev in levs_sorted:
            fig = plt.figure()

            field = data[d][lev]

            print type(field)
            field = np.ma.masked_where(field.abs() < 1e-10, field)

            im = bmap.pcolormesh(x, y, field, cmap=cmap)
            bmap.colorbar(im)

            fig.savefig("{}/{}_{}{:0d}_{}.jpg".format(img_folder, varname, current_year, current_month, lev))
            plt.close(fig)

        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1




def plot_all(folder_path=""):
    bmap = None

    if folder_path == "":
        folder_path = sys.argv[1]

    for f in os.listdir(folder_path):
        #skip files other than monthly
        if not "monthly_fields.rpn" in f.lower():
            continue

        r = RPN(bmap)
        vlist = r.get_list_of_varnames()

        #remove coordinates from the list
        for varname in vlist:
            data = r.get_4d_field(name=varname)
            img_folder = os.path.join(folder_path, "img")
            plot_variable(varname, data, img_folder=img_folder)


def main():
    plot_all(folder_path="")

if __name__ == '__main__':
    main()
