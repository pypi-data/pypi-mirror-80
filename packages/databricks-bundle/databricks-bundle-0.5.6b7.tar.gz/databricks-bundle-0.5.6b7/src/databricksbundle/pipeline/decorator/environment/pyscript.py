# pylint: disable = invalid-name
import os
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

print('pyscript init')
print(f'isDatabricks: {isDatabricks()}')
print(f'isNotebookEnvironment: {isNotebookEnvironment()}')
print(f'containerInitEnvVarDefined: {containerInitEnvVarDefined()}')

if containerInitEnvVarDefined():
    print('envVarContainerLoader')
    from databricksbundle.container.envVarContainerLoader import container
else:
    print('pyprojectContainerLoader')
    from databricksbundle.container.pyprojectContainerLoader import container

def _getPipelinePath():
    if isDatabricks() and not isNotebookEnvironment():
        return Path(sys.argv[1])  # calling from Databricks job
    else:
        return Path(sys.argv[0])

class pipelineFunction:

    def __init__(self, *args, **kwargs): # pylint: disable = unused-argument
        print("pipelineFunction init")
        checkArgs(args, self.__class__.__name__)

    def __call__(self, fun, *args, **kwargs):
        print("pipelineFunction call")
        pp = _getPipelinePath()
        print(f"pipeline path: {pp}")

        services = container.get(ServicesResolver).resolve(fun, 0, pp)  # pylint: disable = no-member

        print('calling decorated function')
        fun(*services)

        return fun

class dataFrameLoader:

    def __init__(self, *args, **kwargs): # pylint: disable = unused-argument
        checkArgs(args, self.__class__.__name__)

    def __call__(self, fun, *args, **kwargs):
        services = container.get(ServicesResolver).resolve(fun, 0, _getPipelinePath()) # pylint: disable = no-member
        loadDataFrame(fun, services)

        return fun

class transformation:

    def __init__(self, *args, **kwargs): # pylint: disable = unused-argument
        self._sources = args # type: Tuple[callable]

    def __call__(self, fun, *args, **kwargs):
        startIndex = len(self._sources)
        services = container.get(ServicesResolver).resolve(fun, startIndex, _getPipelinePath()) # pylint: disable = no-member
        transform(fun, self._sources, services)

        return fun

class dataFrameSaver:

    def __init__(self, *args):
        self._sources = args # type: Tuple[callable]

    def __call__(self, fun, *args, **kwargs):
        services = container.get(ServicesResolver).resolve(fun, 1, _getPipelinePath()) # pylint: disable = no-member
        saveDataFrame(fun, self._sources, services)

        return fun
