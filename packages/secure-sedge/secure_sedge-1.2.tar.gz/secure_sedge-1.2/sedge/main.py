from raft import Collection, Program
from .versioning import version
from . import sewer


ns = Collection.from_module(sewer)
program = Program(version=version, namespace=ns)
