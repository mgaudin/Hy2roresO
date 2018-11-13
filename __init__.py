# -*- coding: utf-8 -*-

#*******************************************************************************
# This plugin is released under the 3-Clause BSD License
#
# see license-3-Clause-BSD.txt
#
# see <a href="https://opensource.org/licenses/BSD-3-Clause">https://opensource.org/licenses/BSD-3-Clause</a>
#
# @author Michaël Gaudin, Alice Gonnaud, Guillaume Vasseur
#
# @copyright 2018 - Michaël Gaudin, Alice Gonnaud, Guillaume Vasseur, ENSG
#*****************************************************************************/



# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Hydroreso class from file Hydroreso.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .hydroreso import Hydroreso
    return Hydroreso(iface)
