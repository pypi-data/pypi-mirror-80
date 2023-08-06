"""
   The package's modules are:
   - FactTable for defining a fact table
   - Dimension for defining a dimension, which can be attached a FactTable object
   - Datatype for letting users define their own datatypes
   - LOG for using the build-in log functionality from simpleetl
   - CONFIG for setting global configuration parameters
   - runETL for initiating an ETL batch run
   - datatypes giving access to pre-defined datatypes.
   - datatypefuncs giving access to pre-defined functions for defining new Datatype objects
"""

# Copyright (c) 2020, FlexDanmark
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from simpleetl._modules.Configuration import Configuration as __Configuration

CONFIG = __Configuration()
from simpleetl._modules.Logger import LOGCLASS

LOG = LOGCLASS()

from simpleetl._modules.Datatype import Datatype
from simpleetl._functions import _datatypes as datatypes
from simpleetl._functions import _datatypefuncs as datatypefuncs
from simpleetl._modules.Dimension import Dimension

from simpleetl._processing.runetl import runETL

from simpleetl._modules.FactTable import FactTable

__author__ = "FlexDanmark"
__maintainer__ = "FlexDanmark"
__version__ = '1.0.1'
__all__ = ['FactTable', 'Dimension', 'Datatype', 'LOG', 'CONFIG', 'runETL', 'datatypes', 'datatypefuncs']
