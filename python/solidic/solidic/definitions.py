import inspect
import keyword
import re

import check

from .errors import SolidInvalidDefinition
from .types import (SolidType, SolidPath)

DISALLOWED_NAMES = set(
    [
        'context',
        'meta',
        'arg_dict',
        'dict',
        'input_arg_dict',
        'output_arg_dict',
        'int',
        'str',
        'float',
        'bool',
        'input',
        'output',
        'result',
    ] + keyword.kwlist  # just disallow all python keywords
)


def has_context_argument(fn):
    check.callable_param(fn, 'fn')

    argspec = inspect.getfullargspec(fn)
    return 'context' in argspec[0]


def check_valid_name(name):
    check.str_param(name, 'name')
    if name in DISALLOWED_NAMES:
        raise SolidInvalidDefinition('{name} is not allowed'.format(name=name))

    regex = r'^[A-Za-z0-9_]+$'
    if not re.match(regex, name):
        raise SolidInvalidDefinition(
            '{name} must be in regex {regex}'.format(name=name, regex=regex)
        )
    return name


class SolidExpectationResult:
    def __init__(self, success, message=None, result_context=None):
        self.success = check.bool_param(success, 'success')
        self.message = check.opt_str_param(message, 'message')
        self.result_context = check.opt_dict_param(result_context, 'result_context')


class SolidExpectationDefinition:
    def __init__(self, name, expectation_fn):
        self.name = check_valid_name(name)
        self.expectation_fn = check.callable_param(expectation_fn, 'expectation_fn')


def _contextify_fn(fn):
    check.callable_param(fn, 'fn')

    if not has_context_argument(fn):

        def wrapper_with_context(*args, context, **kwargs):
            check.not_none_param(context, 'context')
            return fn(*args, **kwargs)

        return wrapper_with_context
    else:
        return fn


# The computation which translates an arbitrary set of key value pairs
# to the native programming abstraction
# Input expectations that execute *before* the core transform
class SolidInputDefinition:
    def __init__(self, name, input_fn, argument_def_dict, expectations=None, depends_on=None):
        self.name = check_valid_name(name)
        self.input_fn = _contextify_fn(check.callable_param(input_fn, 'input_fn'))
        self.argument_def_dict = check.dict_param(
            argument_def_dict, 'argument_def_dict', key_type=str, value_type=SolidType
        )
        self.expectations = check.opt_list_param(
            expectations, 'expectations', of_type=SolidExpectationDefinition
        )
        self.depends_on = check.opt_inst_param(depends_on, 'depends_on', Solid)

    @property
    def is_external(self):
        return self.depends_on is None


def create_solidic_single_file_input(name, single_file_fn):
    check.str_param(name, 'name')
    return SolidInputDefinition(
        name=name,
        input_fn=lambda context, arg_dict: single_file_fn(
            context=context,
            path=check.str_elem(arg_dict, 'path')
        ),
        argument_def_dict={'path': SolidPath}
    )


# Output expectations that execute before the output computation
# The output computation itself
class SolidOutputDefinition:
    def __init__(self, name, output_fn, argument_def_dict):
        self.name = check_valid_name(name)
        self.output_fn = _contextify_fn(check.callable_param(output_fn, 'output_fn'))
        self.argument_def_dict = check.dict_param(
            argument_def_dict, 'argument_def_dict', key_type=str, value_type=SolidType
        )


# One or more inputs
# The core computation in the native kernel abstraction
# The output
class Solid:
    def __init__(self, name, inputs, transform_fn, outputs, output_expectations=None):
        self.name = check_valid_name(name)
        self.inputs = check.list_param(inputs, 'inputs', of_type=SolidInputDefinition)
        self.transform_fn = _contextify_fn(check.callable_param(transform_fn, 'transform'))
        self.outputs = check.list_param(outputs, 'supported_outputs', of_type=SolidOutputDefinition)
        self.output_expectations = check.opt_list_param(
            output_expectations, 'output_expectations', of_type=SolidExpectationDefinition
        )

    @property
    def input_names(self):
        return [inp.name for inp in self.inputs]

    def input_def_named(self, name):
        check.str_param(name, 'name')
        for input_ in self.inputs:
            if input_.name == name:
                return input_

        check.failed('Not found')

    def output_def_named(self, name):
        check.str_param(name, 'name')
        for output_def in self.outputs:
            if output_def.name == name:
                return output_def

        check.failed('Not found')
