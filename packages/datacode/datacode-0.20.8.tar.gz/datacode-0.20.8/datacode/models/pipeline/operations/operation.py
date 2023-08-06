import datetime
from copy import deepcopy
from typing import Sequence, Callable, Optional, Type, TYPE_CHECKING, Dict, Any

from mixins.repr import ReprMixin

from datacode.logger import logger

if TYPE_CHECKING:
    from datacode.models.analysis import AnalysisResult
    from datacode.models.pipeline.base import DataPipeline

from datacode.models.source import DataSource
import datacode.hooks as hooks


class DataOperation(ReprMixin):
    """
    Base class for a singlar data process that takes one or more DataSources as inputs and has one DataSource
    as the output.
    """
    repr_cols = ['options', 'output_name', 'pipeline', 'data_sources']
    num_required_sources: int = 1

    def __init__(self, pipeline: 'DataPipeline',
                 data_sources: Sequence[DataSource], options: 'OperationOptions',
                 output_name: Optional[str] = None, include_pipeline_in_result: bool = False,
                 **result_kwargs):
        if output_name is None:
            names = [ds.name if ds.name is not None else 'unnamed' for ds in data_sources]
            output_name = ' & '.join(names) + ' Post-Operation'
        self.options = options
        self.data_sources = data_sources
        self.output_name = output_name
        self.pipeline = pipeline
        self.include_pipeline_in_result = include_pipeline_in_result
        self.result = None
        self.result_kwargs = result_kwargs
        self._set_result(**result_kwargs)
        self._has_been_executed = False

    def execute(self):
        logger.debug(f'Checking whether {self} should be executed')
        if self._has_been_executed and not self.options.always_rerun:
            return

        logger.debug(f'Starting to execute {self}')
        hooks.on_begin_execute_operation(self)
        self._execute()
        self._has_been_executed = True
        hooks.on_end_execute_operation(self)
        logger.debug(f'Finished executing {self}')

    def _execute(self):
        raise NotImplementedError('must implement _execute in subclass of DataOperation')

    def summary(self, *summary_args, summary_method: str=None, summary_function: Callable=None,
                             summary_attr: str=None, **summary_method_kwargs):
        raise NotImplementedError('must implement summary in subclass of DataOperation')

    def describe(self):
        raise NotImplementedError('must implement describe in subclass of DataOperation')

    @property
    def last_modified(self) -> Optional[datetime.datetime]:
        return self.options.last_modified

    @last_modified.setter
    def last_modified(self, value: Optional[datetime.datetime]):
        self.options.last_modified = value

    def _set_result(self, **kwargs):
        config = dict(
            name=self.output_name,
            location=self.options.out_path,
            last_modified=self.last_modified,
            **kwargs
        )

        if self.include_pipeline_in_result:
            config['pipeline'] = self.pipeline

        self.result = self.options.result_class(**config)

    def __repr__(self):
        return f'<DataOperation(data_sources={self.data_sources}, result={self.result})>'


class OperationOptions(ReprMixin):
    """
    Base class for options passed to DataOperations
    """
    op_class: Type[DataOperation] = DataOperation
    result_class: Type = DataSource
    result_kwargs: Optional[Dict[str, Any]] = None
    out_path: Optional[str] = None
    last_modified: Optional[datetime.datetime] = None
    allow_modifying_result: bool = True
    analysis_output_func: Optional[Callable[['AnalysisResult', str], None]] = None
    always_rerun: bool = False
    repr_cols = [
        'out_path',
        'last_modified',
        'allow_modifying_result',
        'analysis_output_func'
    ]

    def copy(self):
        return deepcopy(self)

    @property
    def can_output(self) -> bool:
        return self.out_path is not None

    def get_operation(self, pipeline: 'DataPipeline', *args, include_pipeline_in_result: bool = False, **kwargs) -> DataOperation:
        logger.debug(f'Getting operation from options {self}')
        all_kwargs = {}
        if self.result_kwargs is not None:
            all_kwargs.update(self.result_kwargs)
        all_kwargs.update(kwargs)
        return self.op_class(pipeline, *args, include_pipeline_in_result=include_pipeline_in_result, **all_kwargs)
