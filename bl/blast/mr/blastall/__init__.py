# BEGIN_COPYRIGHT
# 
# Copyright (C) 2009-2013 CRS4.
# 
# This file is part of biodoop-blast.
# 
# biodoop-blast is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
# 
# biodoop-blast is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
# 
# You should have received a copy of the GNU General Public License along with
# biodoop-blast.  If not, see <http://www.gnu.org/licenses/>.
# 
# END_COPYRIGHT
"""
Sequence alignment based on a wrapper for the blastall program.
"""

from pydoop.pipes import runTask, Factory
from mapper import Mapper
from reducer import Reducer


def run_task():
  return runTask(Factory(Mapper, Reducer))
