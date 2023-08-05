# pylint: disable = invalid-name
import sys
from pathlib import Path
from typing import Tuple
from databricksbundle.detector import isDatabricks
from databricksbundle.notebook.helpers import isNotebookEnvironment
from databricksbundle.pipeline.decorator.containerLoader import containerInitEnvVarDefined
from databricksbundle.pipeline.function.ServicesResolver import ServicesResolver
from databricksbundle.pipeline.decorator.argsChecker import checkArgs
from databricksbundle.pipeline.decorator.executor.dataFrameLoader import loadDataFrame
from databricksbundle.pipeline.decorator.executor.transformation import transform
from databricksbundle.pipeline.decorator.executor.dataFrameSaver import saveDataFrame

if containerInitEnvVarDefined():
    from databricksbundle.container.envVarContainerLoader import container
else:
    from databricksbundle.container.pyprojectContainerLoader import container

def _getPipelinePath():
    if isDatabricks() and not isNotebookEnvironment():
        return Path(sys.argv[1])  # calling from Databricks job
    else:
        return Path(sys.argv[0])

def _resolveServices(fun, index: int):
    return container.get(ServicesResolver).resolve(fun, index, _getPipelinePath())  # pylint: disable = no-member

class pipelineFunction:

    def __init__(self, *args, **kwargs): # pylint: disable = unused-argument
        checkArgs(args, self.__class__.__name__)

    def __call__(self, fun, *args, **kwargs):
        services = _resolveServices(fun, 0)
        fun(*services)

        return fun

class dataFrameLoader:

    def __init__(self, *args, **kwargs): # pylint: disable = unused-argument
        checkArgs(args, self.__class__.__name__)

    def __call__(self, fun, *args, **kwargs):
        services = _resolveServices(fun, 0)
        loadDataFrame(fun, services)

        return fun

class transformation:

    def __init__(self, *args, **kwargs): # pylint: disable = unused-argument
        self._sources = args # type: Tuple[callable]

    def __call__(self, fun, *args, **kwargs):
        services = _resolveServices(fun, len(self._sources))
        transform(fun, self._sources, services)

        return fun

class dataFrameSaver:

    def __init__(self, *args):
        self._sources = args # type: Tuple[callable]

    def __call__(self, fun, *args, **kwargs):
        services = _resolveServices(fun, 1)
        saveDataFrame(fun, self._sources, services)

        return fun
