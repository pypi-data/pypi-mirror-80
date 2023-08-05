# pylint: disable = unused-import
import sys
from databricksbundle.detector import isDatabricks
from databricksbundle.notebook.helpers import isNotebookEnvironment

if isDatabricks() and isNotebookEnvironment():
    from databricksbundle.pipeline.decorator.environment.databricks import pipelineFunction, dataFrameLoader, transformation, dataFrameSaver
elif 'unittest' in sys.modules:
    from databricksbundle.pipeline.decorator.environment.unittest import pipelineFunction, dataFrameLoader, transformation, dataFrameSaver
else:
    from databricksbundle.pipeline.decorator.environment.pyscript import pipelineFunction, dataFrameLoader, transformation, dataFrameSaver
