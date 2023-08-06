# Copyright (c) 2016 Electric Power Research Institute, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the EPRI nor the names of its contributors may be used
#    to endorse or promote products derived from this software without specific
#    prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import logging

import numpy
from PySide2 import QtGui, QtWidgets

from . import util
from .. import export_script

logger = logging.getLogger(__name__)


def add_mean_std_dev_summary_button(figure, text):
    toolbar = figure.canvas.toolbar
    actionText = QtWidgets.QApplication.translate("RMSSummaryAction",
                                                  "Mean and Std Dev Summary")
    action = QtWidgets.QAction(actionText, toolbar)
    action.setIcon(QtGui.QIcon.fromTheme("multimeter_analog"))

    def show_rms_summary():
        QtWidgets.QMessageBox.information(toolbar, "Mean and Std Dev Summary",
                                          text)

    action.triggered.connect(show_rms_summary)

    toolbar.addAction(action)


def time_analysis(parent=None):
    ret = util.load_batch(parent=parent)
    if ret is None:
        return  # error message displayed, or user cancelled
    file_infos, header = ret

    channel_index = util.choose_channel(header, parent=parent)
    if channel_index is None:
        return  # error message displayed, or user cancelled

    batch_info = util.decode_batch(file_infos, header, [channel_index],
                                   parent=parent)
    if batch_info is None:
        return  # error message displayed, or user cancelled

    batch_info = util.get_datetime_subset(batch_info, parent=parent)
    if batch_info is None:
        return  # error message displayed, or user cancelled

    ret = util.warn_about_lost_packets(batch_info, parent=parent)
    if not ret:
        return  # user cancelled

    sequence_info, unit_info = util.sequence_data(batch_info, chunk=False,
                                                  parent=parent)

    time, data, _start, _end = sequence_info[channel_index][0]

    show_legend = False

    if data.shape[1] != 1:
        subchannel_index = util.choose_subchannel(batch_info[channel_index],
                                                  allow_all=True)
        if subchannel_index is None:
            return  # user cancelled
        elif subchannel_index != -1:
            data = data[:, subchannel_index:subchannel_index+1]
        else:
            show_legend = True

    # wrapper around matplotlib.pyplot.subplots()
    fig, ax = export_script.subplots_wrapper()

    ax.plot(time, data)

    channel_data = batch_info[channel_index]
    subchannel_names = channel_data.channel_decoder.subchannel_names

    mean_std_dev_lines = []
    mean = numpy.mean(data, axis=0)
    std_dev = numpy.std(data, axis=0)
    uf = unit_info[channel_index]['formatter']
    for m, std, n in zip(mean, std_dev, subchannel_names):
        m_str = uf.format_utf8(m)
        std_str = uf.format_utf8(std)
        mean_std_dev_lines.append(
            "{} mean: {}, std dev: {}".format(n, m_str, std_str))

    ax.set_xlabel("Time (s)")
    unit_str = unit_info[channel_index]['utf8']
    if unit_str:
        ax.set_ylabel("Magnitude ({})".format(unit_str))
    else:
        ax.set_ylabel("Magnitude")

    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    ax.get_yaxis().get_major_formatter().set_useOffset(False)

    if show_legend:
        ax.legend(subchannel_names)

    add_mean_std_dev_summary_button(fig, "\n".join(mean_std_dev_lines))

    fig.show()


def synchronous_time_analysis(parent=None):
    ret = util.load_batch(parent=parent)
    if ret is None:
        return  # error message displayed, or user cancelled
    file_infos, header = ret

    channel_indexes = util.choose_synchronous_channels(header, parent)
    if channel_indexes is None:
        return  # error message displayed, or user cancelled

    batch_info = util.decode_batch(file_infos, header, channel_indexes,
                                   parent=parent)
    if batch_info is None:
        return  # error message displayed, or user cancelled

    batch_info = util.get_datetime_subset(batch_info, parent=parent)
    if batch_info is None:
        return  # error message displayed, or user cancelled

    ret = util.warn_about_lost_packets(batch_info, once=True, parent=parent)
    if not ret:
        return  # user cancelled

    sequence_info, unit_info = util.sequence_data(
        batch_info, chunk=False, unscaled_units=True, parent=parent)

    # group channels by unit type
    plot_groups = []
    groups_by_unit_type = {}
    for channel_index in sorted(channel_indexes):
        channel = header['channels'][channel_index]
        if channel.unit_type == 0:
            # don't share plots between channels with unknown units
            plot_groups.append([channel_index])
        elif channel.unit_type in groups_by_unit_type:
            # already have a group made
            plot_group = groups_by_unit_type[channel.unit_type]
            plot_group.append(channel_index)
        else:
            # need a new group
            plot_group = [channel_index]
            plot_groups.append(plot_group)
            groups_by_unit_type[channel.unit_type] = plot_group

    # wrapper around matplotlib.pyplot.subplots()
    fig, ax_list = export_script.subplots_wrapper(len(plot_groups),
                                                  squeeze=False, sharex=True)

    mean_std_dev_lines = []

    for i, ax in enumerate(ax_list[:, 0]):
        plot_group = plot_groups[i]

        legend_strs = []

        for channel_index in plot_group:
            time, data, _start, _end = sequence_info[channel_index][0]
            ax.plot(time, data)

            channel_data = batch_info[channel_index]
            subchannel_names = channel_data.channel_decoder.subchannel_names
            legend_strs.extend(subchannel_names)

            mean = numpy.mean(data, axis=0)
            std_dev = numpy.std(data, axis=0)
            uf = unit_info[channel_index]['formatter']
            for m, std, n in zip(mean, std_dev, subchannel_names):
                m_str = uf.format_utf8(m)
                std_str = uf.format_utf8(std)
                mean_std_dev_lines.append(
                    "{} mean: {}, std dev: {}".format(n, m_str, std_str))

        ax.set_xlabel("Time (s)")
        unit_str = unit_info[plot_group[0]]['utf8']
        if unit_str:
            ax.set_ylabel("Magnitude ({})".format(unit_str))
        else:
            ax.set_ylabel("Magnitude")

        ax.get_xaxis().get_major_formatter().set_useOffset(False)
        ax.get_yaxis().get_major_formatter().set_useOffset(False)

        ax.legend(legend_strs)

    add_mean_std_dev_summary_button(fig, "\n".join(mean_std_dev_lines))

    fig.show()


def overlaid_time_analysis(parent=None):
    sequences = []
    subchannel_indexes = []
    unit_types = []
    unit_names = []
    unit_formatters = []
    names = []

    while True:
        # load a batch of files
        ret = util.load_batch(parent=parent)
        if ret is None:
            return  # error message displayed, or user cancelled
        file_infos, header = ret

        # choose a channel
        channel_index = util.choose_channel(header, parent=parent)
        if channel_index is None:
            return  # error message displayed, or user cancelled

        batch_info = util.decode_batch(file_infos, header, [channel_index],
                                       parent=parent)
        if batch_info is None:
            return  # error message displayed, or user cancelled

        subchannel_index = util.choose_subchannel(
            batch_info[channel_index], allow_all=False)
        if subchannel_index is None:
            return  # user cancelled
        subchannel_indexes.append(subchannel_index)

        batch_info = util.get_datetime_subset(batch_info, parent=parent)
        if batch_info is None:
            return  # error message displayed, or user cancelled

        ret = util.warn_about_lost_packets(batch_info, parent=parent)
        if not ret:
            return  # user cancelled

        sequence_info, unit_info = util.sequence_data(
            batch_info, chunk=False, unscaled_units=True, parent=parent)

        sequence = sequence_info[channel_index][0]

        sequences.append(sequence)
        unit_types.append(header['channels'][channel_index].unit_type)
        unit_names.append(unit_info[channel_index]['utf8'])
        unit_formatters.append(unit_info[channel_index]['formatter'])

        # ask the user for a name for this set
        msg = "Display name for this batch (#{}):".format(len(sequences))
        name, ok = QtWidgets.QInputDialog.getText(parent, "Batch Name", msg)
        if not ok:
            return  # user cancelled

        names.append(name.strip())

        # ask the user if they want to load more
        msg = "Load more batches? Loaded {} so far".format(len(sequences))
        ret = QtWidgets.QMessageBox.question(
            parent, "More Batches?", msg,
            buttons=(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No),
            default=QtWidgets.QMessageBox.No)
        if ret != QtWidgets.QMessageBox.Yes:
            break

    # group channels by unit type
    plot_groups = []
    groups_by_unit_type = {}
    for batch_index, unit_type in enumerate(unit_types):
        if unit_type == 0:
            # don't share plots between channels with unknown units
            plot_groups.append([batch_index])
        elif unit_type in groups_by_unit_type:
            # already have a group made
            plot_group = groups_by_unit_type[unit_type]
            plot_group.append(batch_index)
        else:
            # need a new group
            plot_group = [batch_index]
            plot_groups.append(plot_group)
            groups_by_unit_type[unit_type] = plot_group

    # wrapper around matplotlib.pyplot.subplots()
    fig, ax_list = export_script.subplots_wrapper(len(plot_groups),
                                                  squeeze=False, sharex=True)

    mean_std_dev_lines = []

    for i, ax in enumerate(ax_list[:, 0]):
        plot_group = plot_groups[i]

        for batch_index in plot_group:
            time, data, _start, _end = sequences[batch_index]
            subchannel_index = subchannel_indexes[batch_index]
            ax.plot(time, data[:, subchannel_index], label=names[batch_index])

            mean = numpy.mean(data[:, subchannel_index], axis=0).item(0)
            std_dev = numpy.std(data[:, subchannel_index], axis=0).item(0)
            uf = unit_formatters[batch_index]
            m_str = uf.format_utf8(mean)
            std_str = uf.format_utf8(std_dev)
            mean_std_dev_lines.append(
                "{} mean: {}, std dev: {}".format(names[batch_index], m_str,
                                                  std_str))

        ax.legend()

        ax.set_xlabel("Time (s)")
        unit_str = unit_names[plot_group[0]]
        if unit_str:
            ax.set_ylabel("Magnitude ({})".format(unit_str))
        else:
            ax.set_ylabel("Magnitude")

        ax.get_xaxis().get_major_formatter().set_useOffset(False)
        ax.get_yaxis().get_major_formatter().set_useOffset(False)

    add_mean_std_dev_summary_button(fig, "\n".join(mean_std_dev_lines))

    fig.show()
