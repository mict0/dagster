import pytest

from dagster import (
    ArgumentDefinition,
    ExecutionContext,
    OutputDefinition,
    PipelineDefinition,
    PipelineContextDefinition,
    config,
    execute_pipeline,
    solid,
    types,
    with_context,
)
from dagster.core.errors import (DagsterTypeError, DagsterInvariantViolationError)


def test_default_context():
    @solid(
        inputs=[],
        output=OutputDefinition(),
    )
    @with_context
    def default_context_transform(context):
        assert context.log_level == 'ERROR'

    pipeline = PipelineDefinition(solids=[default_context_transform])
    execute_pipeline(
        pipeline, environment=config.Environment(sources={}, context=config.Context('default', {}))
    )


def test_default_context_with_log_level():
    @solid(
        inputs=[],
        output=OutputDefinition(),
    )
    @with_context
    def default_context_transform(context):
        assert context.log_level == 'ERROR'

    pipeline = PipelineDefinition(solids=[default_context_transform])
    execute_pipeline(
        pipeline,
        environment=config.Environment(
            sources={}, context=config.Context('default', {'log_level': 'ERROR'})
        )
    )

    with pytest.raises(DagsterTypeError, message='Argument mismatch in context default'):
        execute_pipeline(
            pipeline,
            environment=config.Environment(
                sources={}, context=config.Context('default', {'log_level': 2})
            )
        )


def test_default_value():
    def _get_args_test_solid(arg_name, arg_value):
        @solid(
            inputs=[],
            output=OutputDefinition(),
        )
        @with_context
        def args_test(context):
            assert context.user_context == {arg_name: arg_value}

        return args_test

    pipeline = PipelineDefinition(
        solids=[_get_args_test_solid('arg_one', 'heyo')],
        context_definitions={
            'custom_one':
            PipelineContextDefinition(
                argument_def_dict={
                    'arg_one':
                    ArgumentDefinition(
                        dagster_type=types.String,
                        is_optional=True,
                        default_value='heyo',
                    )
                },
                context_fn=lambda args: ExecutionContext(user_context=args),
            ),
        }
    )

    execute_pipeline(
        pipeline,
        environment=config.Environment(sources={}, context=config.Context('custom_one', {}))
    )


def test_custom_contexts():
    @solid(
        inputs=[],
        output=OutputDefinition(),
    )
    @with_context
    def custom_context_transform(context):
        assert context.user_context == {'arg_one': 'value_two'}

    pipeline = PipelineDefinition(
        solids=[custom_context_transform],
        context_definitions={
            'custom_one':
            PipelineContextDefinition(
                argument_def_dict={'arg_one': ArgumentDefinition(dagster_type=types.String)},
                context_fn=lambda args: ExecutionContext(user_context=args),
            ),
            'custom_two':
            PipelineContextDefinition(
                argument_def_dict={'arg_one': ArgumentDefinition(dagster_type=types.String)},
                context_fn=lambda args: ExecutionContext(user_context=args),
            )
        },
    )

    environment_one = config.Environment(
        sources={}, context=config.Context('custom_one', {'arg_one': 'value_two'})
    )

    execute_pipeline(pipeline, environment=environment_one)

    environment_two = config.Environment(
        sources={}, context=config.Context('custom_two', {'arg_one': 'value_two'})
    )

    execute_pipeline(pipeline, environment=environment_two)


# TODO: reenable pending the ability to specific optional arguments
# https://github.com/dagster-io/dagster/issues/56
def test_invalid_context():
    @solid(
        inputs=[],
        output=OutputDefinition(),
    )
    def never_transform():
        raise Exception('should never execute')

    default_context_pipeline = PipelineDefinition(solids=[never_transform])

    environment_context_not_found = config.Environment(
        sources={}, context=config.Context('not_found', {})
    )

    with pytest.raises(DagsterInvariantViolationError, message='Context not_found not found'):
        execute_pipeline(
            default_context_pipeline,
            environment=environment_context_not_found,
            throw_on_error=True
        )

    environment_arg_name_mismatch = config.Environment(
        sources={}, context=config.Context('default', {'unexpected': 'value'})
    )

    with pytest.raises(DagsterTypeError, message='Argument mismatch in context default'):
        execute_pipeline(
            default_context_pipeline,
            environment=environment_arg_name_mismatch,
            throw_on_error=True
        )

    with_argful_context_pipeline = PipelineDefinition(
        solids=[never_transform],
        context_definitions={
            'default':
            PipelineContextDefinition(
                argument_def_dict={'string_arg': ArgumentDefinition(types.String)},
                context_fn=lambda _args: _args
            )
        }
    )

    environment_no_args_error = config.Environment(
        sources={}, context=config.Context('default', {})
    )

    with pytest.raises(DagsterTypeError, message='Argument mismatch in context default'):
        execute_pipeline(
            with_argful_context_pipeline,
            environment=environment_no_args_error,
            throw_on_error=True
        )

    environment_type_mismatch_error = config.Environment(
        sources={}, context=config.Context('default', {'string_arg': 1})
    )

    with pytest.raises(DagsterTypeError, message='Argument mismatch in context default'):
        execute_pipeline(
            with_argful_context_pipeline,
            environment=environment_type_mismatch_error,
            throw_on_error=True
        )
