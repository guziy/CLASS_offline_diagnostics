import matplotlib.pyplot as plt
from rpn.rpn import RPN

import numpy as np
import os
from datetime import datetime


def _convert_dict_to_4d_arr(the_dict):
    """
    the_dict - {t: {lev: field(x, y)}}
    """

    t_sorted = list(sorted(the_dict.keys()))
    z_sorted = list(sorted(the_dict.items()[0][1].keys()))

    return np.asarray([[the_dict[t][z] for z in z_sorted] for t in t_sorted]).squeeze()


def compare_2d(path_base, path_list, label_list):
    """
    compare only monthly fields
    """
    delta_small = 1e-6
    nvert_levs_for_soiltemp = 3  # Compare only 3 levels of the soil temperature

    img_folder = "{:%Y%m%d}".format(datetime.now())

    for vname in ["TBAR", "SNO"]:
        r = RPN(os.path.join(path_base, "{}_monthly_fields.rpn".format(vname)))
        data_base = r.get_4d_field_fc_hour_as_time(name=vname)
        r.close()


def compare_swe(path_base, path_list, label_list):
    vname = "SNO"

    delta_small = 1e-6

    r = RPN(os.path.join(path_base, "{}_monthly_fields.rpn".format(vname)))
    data_base = r.get_4d_field_fc_hour_as_time(name=vname)
    r.close()

    data_base = _convert_dict_to_4d_arr(data_base)

    to_mask = data_base < delta_small

    if vname == "SNO":
        to_mask |= data_base > 1000

    data_base = np.ma.masked_where(to_mask, data_base)

    fig = plt.figure(figsize=(15, 6))

    data_base_ts = data_base.mean(axis=1).mean(axis=1)

    plt.plot(data_base_ts, label="base")

    for the_path, the_label in zip(path_list, label_list):
        r1 = RPN(os.path.join(the_path, "{}_monthly_fields.rpn".format(vname)))
        data1 = _convert_dict_to_4d_arr(r1.get_4d_field_fc_hour_as_time(name=vname))
        to_mask1 = (data1 < delta_small)
        if vname == "SNO":
            to_mask1 |= data1 > 1000

        data1 = np.ma.masked_where(to_mask1, data1)
        r1.close()
        data1_ts = data1.mean(axis=1).mean(axis=1)
        plt.plot(data1_ts, label=the_label)
        plt.plot(data1_ts - data_base_ts, label=r"$\Delta$" + the_label, lw=5)


    # Shrink current axis by 20%
    ax = plt.gca()
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    # fig.tight_layout()
    fig.savefig("{0}_diag_1d_{1:%Y-%m-%d_%H}.png".format(vname, datetime.now()))


def compare_soiltemp_1d(path_base, path_list, label_list):
    vname = "TBAR"
    level = 0

    delta_small = 1e-6

    r = RPN(os.path.join(path_base, "{}_monthly_fields.rpn".format(vname)))
    data_base = r.get_4d_field_fc_hour_as_time(name=vname)
    r.close()

    data_base = _convert_dict_to_4d_arr(data_base)

    to_mask = data_base < delta_small

    if vname == "SNO":
        to_mask = to_mask | (data_base > 1000)

    data_base = np.ma.masked_where(to_mask, data_base)

    fig = plt.figure(figsize=(15, 6))

    data_base_ts = data_base.mean(axis=2).mean(axis=2)[:, level] - 273.15

    plt.plot(data_base_ts, label="base")

    for the_path, the_label in zip(path_list, label_list):
        r1 = RPN(os.path.join(the_path, "{}_monthly_fields.rpn".format(vname)))
        data1 = _convert_dict_to_4d_arr(r1.get_4d_field_fc_hour_as_time(name=vname))
        to_mask1 = (data1 < delta_small)
        if vname == "SNO":
            to_mask1 = to_mask1 | (data1 > 1000)

        data1 = np.ma.masked_where(to_mask1, data1)
        r1.close()
        data1_ts = data1.mean(axis=2).mean(axis=2)[:, level] - 273.15
        plt.plot(data1_ts, label=the_label)
        plt.plot(data1_ts - data_base_ts, label=r"$\Delta$" + the_label, lw=5)

    # Shrink current axis by 20%
    ax = plt.gca()
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


    # fig.tight_layout()
    fig.savefig("{0}_{1}_diag_1d_{2:%Y-%m-%d_%H}.png".format(vname, level, datetime.now()))


def main():
    path_base = "/gs/project/ugh-612-aa/huziy/CLASS_offline_VG/CLASS_output_debug0"

    path_list = [
        "/gs/project/ugh-612-aa/huziy/CLASS_offline_VG/CLASS_output_debug1",
        "/home/huziy/current_project/CLASS_offline_VG/exp_debug2/CLASS_output_debug2",
        "/home/huziy/current_project/CLASS_offline_VG/exp_debug2/CLASS_output_debug3",
        "/home/huziy/current_project/CLASS_offline_VG/exp_debug2/CLASS_output_debug4",
        "/gs/project/ugh-612-aa/huziy/CLASS_offline_VG/exp_debug2/CLASS_output_debug5"
    ]

    label_list = ["debug1 (11sept2014)", "new configuration system", "debug3", "debug4", "debug5"]

    compare_swe(path_base, path_list, label_list)
    compare_soiltemp_1d(path_base, path_list, label_list)


if __name__ == "__main__":
    main()
