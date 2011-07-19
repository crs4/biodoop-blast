# BEGIN_COPYRIGHT
# END_COPYRIGHT
"""
Sequence alignment based on a wrapper for the blastall program.
"""

from pydoop.pipes import runTask, Factory
from mapper import Mapper
from reducer import Reducer


def run_task():
  return runTask(Factory(Mapper, Reducer))
