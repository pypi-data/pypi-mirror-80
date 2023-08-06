#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Artella About plugin implementation
"""

from __future__ import print_function, division, absolute_import

import logging

import artella
import artella.dcc as dcc
from artella.core import dcc as core_dcc
from artella.core import plugin, utils, qtutils

if qtutils.QT_AVAILABLE:
    from artella.externals.Qt import QtWidgets

logger = logging.getLogger('artella')


class AboutPlugin(plugin.ArtellaPlugin, object):

    ID = 'artella-plugins-about'
    INDEX = 101

    def __init__(self, config_dict=None, manager=None):
        super(AboutPlugin, self).__init__(config_dict=config_dict, manager=manager)

    def about(self):
        """
        Shows an about window that shows information about current installed Artella plugin
        """

        about_dialog = AboutDialog()
        about_dialog.exec_()


class AboutDialog(artella.Dialog, object):
    def __init__(self, parent=None, **kwargs):
        super(AboutDialog, self).__init__(parent, **kwargs)

        self.setWindowTitle('About Artella Plugin')

        self._fill_data()

    def get_main_layout(self):
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)

        return main_layout

    def setup_ui(self):
        super(AboutDialog, self).setup_ui()

        version_layout = QtWidgets.QHBoxLayout()
        version_layout.setContentsMargins(2, 2, 2, 2)
        version_layout.setSpacing(2)
        version_label = QtWidgets.QLabel('Version: '.format(dcc.nice_name()))
        self._artella_dcc_plugin_version_label = QtWidgets.QLabel()
        version_layout.addStretch()
        version_layout.addWidget(version_label)
        version_layout.addWidget(self._artella_dcc_plugin_version_label)
        version_layout.addStretch()

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setContentsMargins(2, 2, 2, 2)
        button_layout.setSpacing(2)
        self._show_plugins_btn = QtWidgets.QPushButton('Show Plugins')
        button_layout.addStretch()
        button_layout.addWidget(self._show_plugins_btn)
        button_layout.addStretch()

        self._plugins_tree = QtWidgets.QTreeWidget()
        self._plugins_tree.setHeaderLabels(['Name', 'Version', 'ID'])
        self._plugins_tree.setColumnCount(3)
        self._plugins_tree.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self._plugins_tree.setVisible(False)

        self.main_layout.addStretch()
        self.main_layout.addLayout(version_layout)
        self.main_layout.addLayout(button_layout)
        self.main_layout.addStretch()
        self.main_layout.addLayout(button_layout)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self._plugins_tree)

        self._show_plugins_btn.clicked.connect(self._on_toggle_plugins_visibility)

    def _fill_data(self):
        current_plugin_version = artella.DccPlugin().get_version() or 'Undefined'
        self._artella_dcc_plugin_version_label.setText(current_plugin_version)

        added_packages = dict()

        # Retrieve Artella plugins versions
        plugins = artella.PluginsMgr().plugins
        for plugin_id, plugin_data in plugins.items():
            plugin_package = plugin_data.get('package', 'Not Defined')
            package_item = added_packages.get(plugin_package, None)
            if not package_item:
                package_item = QtWidgets.QTreeWidgetItem([plugin_package])
                self._plugins_tree.addTopLevelItem(package_item)
                added_packages[plugin_package] = package_item
            plugin_name = plugin_data['name']
            plugin_version = plugin_data.get('version', 'Undefined')
            plugin_item = QtWidgets.QTreeWidgetItem([plugin_name, plugin_version, plugin_id])
            package_item.addChild(plugin_item)

        package_item = added_packages.get('Artella', None)
        if not package_item:
            package_item = QtWidgets.QTreeWidgetItem(['Artella'])
            self._plugins_tree.addTopLevelItem(package_item)

        # Retrieve DCC plugin version
        dcc_version = None
        dcc_module_name = core_dcc.CURRENT_DCC_MODULE
        if dcc_module_name:
            try:
                dcc_module_version = '{}.__version__'.format(dcc_module_name)
                dcc_version_mod = utils.import_module(dcc_module_version)
                dcc_version = dcc_version_mod.get_version()
            except Exception as exc:
                logger.warning('Impossible to retrieve {} Artella plugin version: {}'.format(dcc.name(), exc))
        dcc_version = dcc_version or 'Undefined'
        dcc_version_item = QtWidgets.QTreeWidgetItem([dcc.nice_name(), dcc_version, dcc_module_name.replace('.', '- ')])
        package_item.insertChild(0, dcc_version_item)

        # Retrieve Artella core version
        core_version = None
        core_version_path = 'artella.__version__'
        try:
            core_version_mod = utils.import_module(core_version_path)
            core_version = core_version_mod.get_version()
        except Exception as exc:
            logger.warning('Impossible to retrieve Artella Core version: {}'.format(exc))
        core_version = core_version or 'Undefined'
        core_version_item = QtWidgets.QTreeWidgetItem(['Core', core_version, 'artella-plugins-core'])
        package_item.insertChild(0, core_version_item)

        self._plugins_tree.expandAll()
        self._plugins_tree.resizeColumnToContents(0)
        self._plugins_tree.resizeColumnToContents(1)
        self._plugins_tree.resizeColumnToContents(2)

    def _on_toggle_plugins_visibility(self):
        self._plugins_tree.setVisible(not self._plugins_tree.isVisible())
        self._show_plugins_btn.setText('Show Plugins' if not self._plugins_tree.isVisible() else 'Hide Plugins')
        self.resize(self.sizeHint())
