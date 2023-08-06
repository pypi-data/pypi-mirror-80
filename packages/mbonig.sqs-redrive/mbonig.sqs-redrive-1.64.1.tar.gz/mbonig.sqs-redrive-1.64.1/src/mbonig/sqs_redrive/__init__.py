"""
# SQS Redrive

This construct creates a Lambda function that you can use to move SQS messages from one queue to another. This is often used for moving Dead Letter Queue messages back to the original queue for reprocessing.

# This is a pre-release!

This is a quick first-draft. All the options that will likely need to be added to accomodate a large
number of use-cases are still needed. If you'd like to make requests or help update this construct, please
open an [Issue](https://github.com/mbonig/cicd-spa-website/issues) or a [PR](https://github.com/mbonig/cicd-spa-website/pulls).

## What Gets Created

A Lambda function and related policy which moves SQS queue messages from one queue to another.

## Example

This creates two external queues and then creates the Lambda to move from the deadLetterQueue to the mainQueue

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
from ...lib.sqs_redrive import SqsRedrive
from aws_cdk.aws_sqs import Queue

app = cdk.App()
stack = cdk.Stack(app, "test-stack")

main_queue = Queue(stack, "main-queue")
dead_letter_queue = Queue(stack, "dlq-queue")
SqsRedrive(stack, "SqsRedriveConstructStack",
    main_queue=main_queue,
    dead_letter_queue=dead_letter_queue
)
```

*Note: this is the integration test (`cdk synth`).*

## Input Properties

What are the inputs to your constructs?

|property|description|example
|---|---|---
|mainQueue|The destination queue for the messages.|`new Queue(stack, 'main-queue')`
|deadLetterQueue|The source queue of the messages.|`new Queue(stack, 'dead-letter-queue')`

## Design Notes

This is early design and serves one very specific use-case. If you have suggestions on how to make this better, please open an [Issue in Github](https://github.com/mbonig/sqs-redrive/issues).

## Contributing

Please open Pull Requests and Issues on the [Github Repo](https://github.com/mbonig/sqs-redrive).

## License

MIT
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from ._jsii import *

import aws_cdk.aws_lambda
import aws_cdk.aws_lambda_nodejs
import aws_cdk.aws_sqs
import aws_cdk.core


class SqsRedrive(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@matthewbonig/sqs-redrive.SqsRedrive",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        dead_letter_queue: aws_cdk.aws_sqs.IQueue,
        main_queue: aws_cdk.aws_sqs.IQueue,
        lambda_props: typing.Optional[aws_cdk.aws_lambda_nodejs.NodejsFunctionProps] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param dead_letter_queue: -
        :param main_queue: -
        :param lambda_props: -
        """
        props = SqsRedriveProps(
            dead_letter_queue=dead_letter_queue,
            main_queue=main_queue,
            lambda_props=lambda_props,
        )

        jsii.create(SqsRedrive, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="lambda")
    def lambda_(self) -> aws_cdk.aws_lambda.IFunction:
        return jsii.get(self, "lambda")

    @lambda_.setter
    def lambda_(self, value: aws_cdk.aws_lambda.IFunction) -> None:
        jsii.set(self, "lambda", value)


@jsii.data_type(
    jsii_type="@matthewbonig/sqs-redrive.SqsRedriveProps",
    jsii_struct_bases=[],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "main_queue": "mainQueue",
        "lambda_props": "lambdaProps",
    },
)
class SqsRedriveProps:
    def __init__(
        self,
        *,
        dead_letter_queue: aws_cdk.aws_sqs.IQueue,
        main_queue: aws_cdk.aws_sqs.IQueue,
        lambda_props: typing.Optional[aws_cdk.aws_lambda_nodejs.NodejsFunctionProps] = None,
    ) -> None:
        """
        :param dead_letter_queue: -
        :param main_queue: -
        :param lambda_props: -
        """
        if isinstance(lambda_props, dict):
            lambda_props = aws_cdk.aws_lambda_nodejs.NodejsFunctionProps(**lambda_props)
        self._values = {
            "dead_letter_queue": dead_letter_queue,
            "main_queue": main_queue,
        }
        if lambda_props is not None:
            self._values["lambda_props"] = lambda_props

    @builtins.property
    def dead_letter_queue(self) -> aws_cdk.aws_sqs.IQueue:
        return self._values.get("dead_letter_queue")

    @builtins.property
    def main_queue(self) -> aws_cdk.aws_sqs.IQueue:
        return self._values.get("main_queue")

    @builtins.property
    def lambda_props(
        self,
    ) -> typing.Optional[aws_cdk.aws_lambda_nodejs.NodejsFunctionProps]:
        return self._values.get("lambda_props")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsRedriveProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SqsRedrive",
    "SqsRedriveProps",
]

publication.publish()
