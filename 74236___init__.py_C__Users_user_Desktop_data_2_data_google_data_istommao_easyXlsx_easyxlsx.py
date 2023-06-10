# -*- coding: utf-8 -*-
"""
    easyXlsx
    ~~~~~

    A easy way to export excel based on XlsxWriter.

    :copyright: (c) 2015 by tommao.
    :license: MIT, see LICENSE for more details.
"""

__title__ = 'easyXlsx'
__version__ = '0.1.0'
__author__ = 'tommao'
__license__ = 'MIT 2.0'
__copyright__ = 'Copyright 2015 tommao'

from .excel import BaseExport, ModelExport

__all__ = [
    BaseExport,
    ModelExport
]
