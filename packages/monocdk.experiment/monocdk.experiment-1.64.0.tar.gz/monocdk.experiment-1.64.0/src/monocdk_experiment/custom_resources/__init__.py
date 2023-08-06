import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

from .. import (
    Construct as _Construct_f50a3f53,
    Duration as _Duration_5170c158,
    Reference as _Reference_d68b1ce5,
)
from ..aws_cloudformation import (
    CustomResourceProviderConfig as _CustomResourceProviderConfig_8f2bd7a0,
    ICustomResourceProvider as _ICustomResourceProvider_6c6f53c6,
)
from ..aws_iam import (
    IGrantable as _IGrantable_0fcfc53a,
    IPrincipal as _IPrincipal_97126874,
    IRole as _IRole_e69bbae4,
    PolicyStatement as _PolicyStatement_f75dc775,
)
from ..aws_lambda import IFunction as _IFunction_1c1de0bc
from ..aws_logs import RetentionDays as _RetentionDays_bdc7ad1f


@jsii.implements(_IGrantable_0fcfc53a)
class AwsCustomResource(
    _Construct_f50a3f53,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.custom_resources.AwsCustomResource",
):
    """Defines a custom resource that is materialized using specific AWS API calls.

    Use this to bridge any gap that might exist in the CloudFormation Coverage.
    You can specify exactly which calls are invoked for the 'CREATE', 'UPDATE' and 'DELETE' life cycle events.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        *,
        policy: "AwsCustomResourcePolicy",
        function_name: typing.Optional[builtins.str] = None,
        install_latest_aws_sdk: typing.Optional[builtins.bool] = None,
        log_retention: typing.Optional[_RetentionDays_bdc7ad1f] = None,
        on_create: typing.Optional["AwsSdkCall"] = None,
        on_delete: typing.Optional["AwsSdkCall"] = None,
        on_update: typing.Optional["AwsSdkCall"] = None,
        resource_type: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        timeout: typing.Optional[_Duration_5170c158] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param policy: The policy that will be added to the execution role of the Lambda function implementing this custom resource provider. The custom resource also implements ``iam.IGrantable``, making it possible to use the ``grantXxx()`` methods. As this custom resource uses a singleton Lambda function, it's important to note the that function's role will eventually accumulate the permissions/grants from all resources.
        :param function_name: A name for the Lambda function implementing this custom resource. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param install_latest_aws_sdk: Whether to install the latest AWS SDK v2. Allows to use the latest API calls documented at https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html. The installation takes around 60 seconds. Default: true
        :param log_retention: The number of days log events of the Lambda function implementing this custom resource are kept in CloudWatch Logs. Default: logs.RetentionDays.INFINITE
        :param on_create: The AWS SDK call to make when the resource is created. Default: - the call when the resource is updated
        :param on_delete: The AWS SDK call to make when the resource is deleted. Default: - no call
        :param on_update: The AWS SDK call to make when the resource is updated. Default: - no call
        :param resource_type: Cloudformation Resource type. Default: - Custom::AWS
        :param role: The execution role for the Lambda function implementing this custom resource provider. This role will apply to all ``AwsCustomResource`` instances in the stack. The role must be assumable by the ``lambda.amazonaws.com`` service principal. Default: - a new role is created
        :param timeout: The timeout for the Lambda function implementing this custom resource. Default: Duration.minutes(2)

        stability
        :stability: experimental
        """
        props = AwsCustomResourceProps(
            policy=policy,
            function_name=function_name,
            install_latest_aws_sdk=install_latest_aws_sdk,
            log_retention=log_retention,
            on_create=on_create,
            on_delete=on_delete,
            on_update=on_update,
            resource_type=resource_type,
            role=role,
            timeout=timeout,
        )

        jsii.create(AwsCustomResource, self, [scope, id, props])

    @jsii.member(jsii_name="getResponseField")
    def get_response_field(self, data_path: builtins.str) -> builtins.str:
        """Returns response data for the AWS SDK call as string.

        Example for S3 / listBucket : 'Buckets.0.Name'

        Note that you cannot use this method if ``ignoreErrorCodesMatching``
        is configured for any of the SDK calls. This is because in such a case,
        the response data might not exist, and will cause a CloudFormation deploy time error.

        :param data_path: the path to the data.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getResponseField", [data_path])

    @jsii.member(jsii_name="getResponseFieldReference")
    def get_response_field_reference(
        self,
        data_path: builtins.str,
    ) -> _Reference_d68b1ce5:
        """Returns response data for the AWS SDK call.

        Example for S3 / listBucket : 'Buckets.0.Name'

        Use ``Token.asXxx`` to encode the returned ``Reference`` as a specific type or
        use the convenience ``getDataString`` for string attributes.

        Note that you cannot use this method if ``ignoreErrorCodesMatching``
        is configured for any of the SDK calls. This is because in such a case,
        the response data might not exist, and will cause a CloudFormation deploy time error.

        :param data_path: the path to the data.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getResponseFieldReference", [data_path])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _IPrincipal_97126874:
        """The principal to grant permissions to.

        stability
        :stability: experimental
        """
        return jsii.get(self, "grantPrincipal")


class AwsCustomResourcePolicy(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.custom_resources.AwsCustomResourcePolicy",
):
    """The IAM Policy that will be applied to the different calls.

    stability
    :stability: experimental
    """

    @jsii.member(jsii_name="fromSdkCalls")
    @builtins.classmethod
    def from_sdk_calls(
        cls,
        *,
        resources: typing.List[builtins.str],
    ) -> "AwsCustomResourcePolicy":
        """Generate IAM Policy Statements from the configured SDK calls.

        Each SDK call with be translated to an IAM Policy Statement in the form of: ``call.service:call.action`` (e.g ``s3:PutObject``).

        :param resources: The resources that the calls will have access to. It is best to use specific resource ARN's when possible. However, you can also use ``AwsCustomResourcePolicy.ANY_RESOURCE`` to allow access to all resources. For example, when ``onCreate`` is used to create a resource which you don't know the physical name of in advance. Note that will apply to ALL SDK calls.

        stability
        :stability: experimental
        """
        options = SdkCallsPolicyOptions(resources=resources)

        return jsii.sinvoke(cls, "fromSdkCalls", [options])

    @jsii.member(jsii_name="fromStatements")
    @builtins.classmethod
    def from_statements(
        cls,
        statements: typing.List[_PolicyStatement_f75dc775],
    ) -> "AwsCustomResourcePolicy":
        """Explicit IAM Policy Statements.

        :param statements: the statements to propagate to the SDK calls.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromStatements", [statements])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="ANY_RESOURCE")
    def ANY_RESOURCE(cls) -> typing.List[builtins.str]:
        """Use this constant to configure access to any resource.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "ANY_RESOURCE")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="statements")
    def statements(self) -> typing.List[_PolicyStatement_f75dc775]:
        """statements for explicit policy.

        stability
        :stability: experimental
        """
        return jsii.get(self, "statements")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        """resources for auto-generated from SDK calls.

        stability
        :stability: experimental
        """
        return jsii.get(self, "resources")


@jsii.data_type(
    jsii_type="monocdk-experiment.custom_resources.AwsCustomResourceProps",
    jsii_struct_bases=[],
    name_mapping={
        "policy": "policy",
        "function_name": "functionName",
        "install_latest_aws_sdk": "installLatestAwsSdk",
        "log_retention": "logRetention",
        "on_create": "onCreate",
        "on_delete": "onDelete",
        "on_update": "onUpdate",
        "resource_type": "resourceType",
        "role": "role",
        "timeout": "timeout",
    },
)
class AwsCustomResourceProps:
    def __init__(
        self,
        *,
        policy: "AwsCustomResourcePolicy",
        function_name: typing.Optional[builtins.str] = None,
        install_latest_aws_sdk: typing.Optional[builtins.bool] = None,
        log_retention: typing.Optional[_RetentionDays_bdc7ad1f] = None,
        on_create: typing.Optional["AwsSdkCall"] = None,
        on_delete: typing.Optional["AwsSdkCall"] = None,
        on_update: typing.Optional["AwsSdkCall"] = None,
        resource_type: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        timeout: typing.Optional[_Duration_5170c158] = None,
    ) -> None:
        """Properties for AwsCustomResource.

        Note that at least onCreate, onUpdate or onDelete must be specified.

        :param policy: The policy that will be added to the execution role of the Lambda function implementing this custom resource provider. The custom resource also implements ``iam.IGrantable``, making it possible to use the ``grantXxx()`` methods. As this custom resource uses a singleton Lambda function, it's important to note the that function's role will eventually accumulate the permissions/grants from all resources.
        :param function_name: A name for the Lambda function implementing this custom resource. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param install_latest_aws_sdk: Whether to install the latest AWS SDK v2. Allows to use the latest API calls documented at https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html. The installation takes around 60 seconds. Default: true
        :param log_retention: The number of days log events of the Lambda function implementing this custom resource are kept in CloudWatch Logs. Default: logs.RetentionDays.INFINITE
        :param on_create: The AWS SDK call to make when the resource is created. Default: - the call when the resource is updated
        :param on_delete: The AWS SDK call to make when the resource is deleted. Default: - no call
        :param on_update: The AWS SDK call to make when the resource is updated. Default: - no call
        :param resource_type: Cloudformation Resource type. Default: - Custom::AWS
        :param role: The execution role for the Lambda function implementing this custom resource provider. This role will apply to all ``AwsCustomResource`` instances in the stack. The role must be assumable by the ``lambda.amazonaws.com`` service principal. Default: - a new role is created
        :param timeout: The timeout for the Lambda function implementing this custom resource. Default: Duration.minutes(2)

        stability
        :stability: experimental
        """
        if isinstance(on_create, dict):
            on_create = AwsSdkCall(**on_create)
        if isinstance(on_delete, dict):
            on_delete = AwsSdkCall(**on_delete)
        if isinstance(on_update, dict):
            on_update = AwsSdkCall(**on_update)
        self._values: typing.Dict[str, typing.Any] = {
            "policy": policy,
        }
        if function_name is not None:
            self._values["function_name"] = function_name
        if install_latest_aws_sdk is not None:
            self._values["install_latest_aws_sdk"] = install_latest_aws_sdk
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if on_create is not None:
            self._values["on_create"] = on_create
        if on_delete is not None:
            self._values["on_delete"] = on_delete
        if on_update is not None:
            self._values["on_update"] = on_update
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if role is not None:
            self._values["role"] = role
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def policy(self) -> "AwsCustomResourcePolicy":
        """The policy that will be added to the execution role of the Lambda function implementing this custom resource provider.

        The custom resource also implements ``iam.IGrantable``, making it possible
        to use the ``grantXxx()`` methods.

        As this custom resource uses a singleton Lambda function, it's important
        to note the that function's role will eventually accumulate the
        permissions/grants from all resources.

        see
        :see: Policy.fromSdkCalls
        stability
        :stability: experimental
        """
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return result

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        """A name for the Lambda function implementing this custom resource.

        default
        :default:

        - AWS CloudFormation generates a unique physical ID and uses that
          ID for the function's name. For more information, see Name Type.

        stability
        :stability: experimental
        """
        result = self._values.get("function_name")
        return result

    @builtins.property
    def install_latest_aws_sdk(self) -> typing.Optional[builtins.bool]:
        """Whether to install the latest AWS SDK v2. Allows to use the latest API calls documented at https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html.

        The installation takes around 60 seconds.

        default
        :default: true

        stability
        :stability: experimental
        """
        result = self._values.get("install_latest_aws_sdk")
        return result

    @builtins.property
    def log_retention(self) -> typing.Optional[_RetentionDays_bdc7ad1f]:
        """The number of days log events of the Lambda function implementing this custom resource are kept in CloudWatch Logs.

        default
        :default: logs.RetentionDays.INFINITE

        stability
        :stability: experimental
        """
        result = self._values.get("log_retention")
        return result

    @builtins.property
    def on_create(self) -> typing.Optional["AwsSdkCall"]:
        """The AWS SDK call to make when the resource is created.

        default
        :default: - the call when the resource is updated

        stability
        :stability: experimental
        """
        result = self._values.get("on_create")
        return result

    @builtins.property
    def on_delete(self) -> typing.Optional["AwsSdkCall"]:
        """The AWS SDK call to make when the resource is deleted.

        default
        :default: - no call

        stability
        :stability: experimental
        """
        result = self._values.get("on_delete")
        return result

    @builtins.property
    def on_update(self) -> typing.Optional["AwsSdkCall"]:
        """The AWS SDK call to make when the resource is updated.

        default
        :default: - no call

        stability
        :stability: experimental
        """
        result = self._values.get("on_update")
        return result

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        """Cloudformation Resource type.

        default
        :default: - Custom::AWS

        stability
        :stability: experimental
        """
        result = self._values.get("resource_type")
        return result

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The execution role for the Lambda function implementing this custom resource provider.

        This role will apply to all ``AwsCustomResource``
        instances in the stack. The role must be assumable by the
        ``lambda.amazonaws.com`` service principal.

        default
        :default: - a new role is created

        stability
        :stability: experimental
        """
        result = self._values.get("role")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[_Duration_5170c158]:
        """The timeout for the Lambda function implementing this custom resource.

        default
        :default: Duration.minutes(2)

        stability
        :stability: experimental
        """
        result = self._values.get("timeout")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsCustomResourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.custom_resources.AwsSdkCall",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "service": "service",
        "api_version": "apiVersion",
        "ignore_error_codes_matching": "ignoreErrorCodesMatching",
        "output_path": "outputPath",
        "parameters": "parameters",
        "physical_resource_id": "physicalResourceId",
        "region": "region",
    },
)
class AwsSdkCall:
    def __init__(
        self,
        *,
        action: builtins.str,
        service: builtins.str,
        api_version: typing.Optional[builtins.str] = None,
        ignore_error_codes_matching: typing.Optional[builtins.str] = None,
        output_path: typing.Optional[builtins.str] = None,
        parameters: typing.Any = None,
        physical_resource_id: typing.Optional["PhysicalResourceId"] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        """An AWS SDK call.

        :param action: The service action to call.
        :param service: The service to call.
        :param api_version: API version to use for the service. Default: - use latest available API version
        :param ignore_error_codes_matching: The regex pattern to use to catch API errors. The ``code`` property of the ``Error`` object will be tested against this pattern. If there is a match an error will not be thrown. Default: - do not catch errors
        :param output_path: Restrict the data returned by the custom resource to a specific path in the API response. Use this to limit the data returned by the custom resource if working with API calls that could potentially result in custom response objects exceeding the hard limit of 4096 bytes. Example for ECS / updateService: 'service.deploymentConfiguration.maximumPercent' Default: - return all data
        :param parameters: The parameters for the service action. Default: - no parameters
        :param physical_resource_id: The physical resource id of the custom resource for this call. Mandatory for onCreate or onUpdate calls. Default: - no physical resource id
        :param region: The region to send service requests to. **Note: Cross-region operations are generally considered an anti-pattern.** **Consider first deploying a stack in that region.** Default: - the region where this custom resource is deployed

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "action": action,
            "service": service,
        }
        if api_version is not None:
            self._values["api_version"] = api_version
        if ignore_error_codes_matching is not None:
            self._values["ignore_error_codes_matching"] = ignore_error_codes_matching
        if output_path is not None:
            self._values["output_path"] = output_path
        if parameters is not None:
            self._values["parameters"] = parameters
        if physical_resource_id is not None:
            self._values["physical_resource_id"] = physical_resource_id
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def action(self) -> builtins.str:
        """The service action to call.

        see
        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        stability
        :stability: experimental
        """
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return result

    @builtins.property
    def service(self) -> builtins.str:
        """The service to call.

        see
        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        stability
        :stability: experimental
        """
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return result

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        """API version to use for the service.

        default
        :default: - use latest available API version

        see
        :see: https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/locking-api-versions.html
        stability
        :stability: experimental
        """
        result = self._values.get("api_version")
        return result

    @builtins.property
    def ignore_error_codes_matching(self) -> typing.Optional[builtins.str]:
        """The regex pattern to use to catch API errors.

        The ``code`` property of the
        ``Error`` object will be tested against this pattern. If there is a match an
        error will not be thrown.

        default
        :default: - do not catch errors

        stability
        :stability: experimental
        """
        result = self._values.get("ignore_error_codes_matching")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """Restrict the data returned by the custom resource to a specific path in the API response.

        Use this to limit the data returned by the custom
        resource if working with API calls that could potentially result in custom
        response objects exceeding the hard limit of 4096 bytes.

        Example for ECS / updateService: 'service.deploymentConfiguration.maximumPercent'

        default
        :default: - return all data

        stability
        :stability: experimental
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def parameters(self) -> typing.Any:
        """The parameters for the service action.

        default
        :default: - no parameters

        see
        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        stability
        :stability: experimental
        """
        result = self._values.get("parameters")
        return result

    @builtins.property
    def physical_resource_id(self) -> typing.Optional["PhysicalResourceId"]:
        """The physical resource id of the custom resource for this call.

        Mandatory for onCreate or onUpdate calls.

        default
        :default: - no physical resource id

        stability
        :stability: experimental
        """
        result = self._values.get("physical_resource_id")
        return result

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        """The region to send service requests to.

        **Note: Cross-region operations are generally considered an anti-pattern.**
        **Consider first deploying a stack in that region.**

        default
        :default: - the region where this custom resource is deployed

        stability
        :stability: experimental
        """
        result = self._values.get("region")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsSdkCall(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PhysicalResourceId(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.custom_resources.PhysicalResourceId",
):
    """Physical ID of the custom resource.

    stability
    :stability: experimental
    """

    @jsii.member(jsii_name="fromResponse")
    @builtins.classmethod
    def from_response(cls, response_path: builtins.str) -> "PhysicalResourceId":
        """Extract the physical resource id from the path (dot notation) to the data in the API call response.

        :param response_path: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromResponse", [response_path])

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, id: builtins.str) -> "PhysicalResourceId":
        """Explicit physical resource id.

        :param id: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "of", [id])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[builtins.str]:
        """Literal string to be used as the physical id.

        stability
        :stability: experimental
        """
        return jsii.get(self, "id")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="responsePath")
    def response_path(self) -> typing.Optional[builtins.str]:
        """Path to a response data element to be used as the physical id.

        stability
        :stability: experimental
        """
        return jsii.get(self, "responsePath")


class PhysicalResourceIdReference(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.custom_resources.PhysicalResourceIdReference",
):
    """Reference to the physical resource id that can be passed to the AWS operation as a parameter.

    stability
    :stability: experimental
    """

    def __init__(self) -> None:
        """
        stability
        :stability: experimental
        """
        jsii.create(PhysicalResourceIdReference, self, [])

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> builtins.str:
        """toJSON serialization to replace ``PhysicalResourceIdReference`` with a magic string.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toJSON", [])


@jsii.implements(_ICustomResourceProvider_6c6f53c6)
class Provider(
    _Construct_f50a3f53,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.custom_resources.Provider",
):
    """Defines an AWS CloudFormation custom resource provider.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        *,
        on_event_handler: _IFunction_1c1de0bc,
        is_complete_handler: typing.Optional[_IFunction_1c1de0bc] = None,
        log_retention: typing.Optional[_RetentionDays_bdc7ad1f] = None,
        query_interval: typing.Optional[_Duration_5170c158] = None,
        total_timeout: typing.Optional[_Duration_5170c158] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param on_event_handler: The AWS Lambda function to invoke for all resource lifecycle operations (CREATE/UPDATE/DELETE). This function is responsible to begin the requested resource operation (CREATE/UPDATE/DELETE) and return any additional properties to add to the event, which will later be passed to ``isComplete``. The ``PhysicalResourceId`` property must be included in the response.
        :param is_complete_handler: The AWS Lambda function to invoke in order to determine if the operation is complete. This function will be called immediately after ``onEvent`` and then periodically based on the configured query interval as long as it returns ``false``. If the function still returns ``false`` and the alloted timeout has passed, the operation will fail. Default: - provider is synchronous. This means that the ``onEvent`` handler is expected to finish all lifecycle operations within the initial invocation.
        :param log_retention: The number of days framework log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param query_interval: Time between calls to the ``isComplete`` handler which determines if the resource has been stabilized. The first ``isComplete`` will be called immediately after ``handler`` and then every ``queryInterval`` seconds, and until ``timeout`` has been reached or until ``isComplete`` returns ``true``. Default: Duration.seconds(5)
        :param total_timeout: Total timeout for the entire operation. The maximum timeout is 2 hours (yes, it can exceed the AWS Lambda 15 minutes) Default: Duration.minutes(30)

        stability
        :stability: experimental
        """
        props = ProviderProps(
            on_event_handler=on_event_handler,
            is_complete_handler=is_complete_handler,
            log_retention=log_retention,
            query_interval=query_interval,
            total_timeout=total_timeout,
        )

        jsii.create(Provider, self, [scope, id, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _: _Construct_f50a3f53) -> _CustomResourceProviderConfig_8f2bd7a0:
        """Called by ``CustomResource`` which uses this provider.

        :param _: -

        deprecated
        :deprecated: use ``provider.serviceToken`` instead

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "bind", [_])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="onEventHandler")
    def on_event_handler(self) -> _IFunction_1c1de0bc:
        """The user-defined AWS Lambda function which is invoked for all resource lifecycle operations (CREATE/UPDATE/DELETE).

        stability
        :stability: experimental
        """
        return jsii.get(self, "onEventHandler")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="serviceToken")
    def service_token(self) -> builtins.str:
        """The service token to use in order to define custom resources that are backed by this provider.

        stability
        :stability: experimental
        """
        return jsii.get(self, "serviceToken")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="isCompleteHandler")
    def is_complete_handler(self) -> typing.Optional[_IFunction_1c1de0bc]:
        """The user-defined AWS Lambda function which is invoked asynchronously in order to determine if the operation is complete.

        stability
        :stability: experimental
        """
        return jsii.get(self, "isCompleteHandler")


@jsii.data_type(
    jsii_type="monocdk-experiment.custom_resources.ProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "on_event_handler": "onEventHandler",
        "is_complete_handler": "isCompleteHandler",
        "log_retention": "logRetention",
        "query_interval": "queryInterval",
        "total_timeout": "totalTimeout",
    },
)
class ProviderProps:
    def __init__(
        self,
        *,
        on_event_handler: _IFunction_1c1de0bc,
        is_complete_handler: typing.Optional[_IFunction_1c1de0bc] = None,
        log_retention: typing.Optional[_RetentionDays_bdc7ad1f] = None,
        query_interval: typing.Optional[_Duration_5170c158] = None,
        total_timeout: typing.Optional[_Duration_5170c158] = None,
    ) -> None:
        """Initialization properties for the ``Provider`` construct.

        :param on_event_handler: The AWS Lambda function to invoke for all resource lifecycle operations (CREATE/UPDATE/DELETE). This function is responsible to begin the requested resource operation (CREATE/UPDATE/DELETE) and return any additional properties to add to the event, which will later be passed to ``isComplete``. The ``PhysicalResourceId`` property must be included in the response.
        :param is_complete_handler: The AWS Lambda function to invoke in order to determine if the operation is complete. This function will be called immediately after ``onEvent`` and then periodically based on the configured query interval as long as it returns ``false``. If the function still returns ``false`` and the alloted timeout has passed, the operation will fail. Default: - provider is synchronous. This means that the ``onEvent`` handler is expected to finish all lifecycle operations within the initial invocation.
        :param log_retention: The number of days framework log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param query_interval: Time between calls to the ``isComplete`` handler which determines if the resource has been stabilized. The first ``isComplete`` will be called immediately after ``handler`` and then every ``queryInterval`` seconds, and until ``timeout`` has been reached or until ``isComplete`` returns ``true``. Default: Duration.seconds(5)
        :param total_timeout: Total timeout for the entire operation. The maximum timeout is 2 hours (yes, it can exceed the AWS Lambda 15 minutes) Default: Duration.minutes(30)

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "on_event_handler": on_event_handler,
        }
        if is_complete_handler is not None:
            self._values["is_complete_handler"] = is_complete_handler
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if query_interval is not None:
            self._values["query_interval"] = query_interval
        if total_timeout is not None:
            self._values["total_timeout"] = total_timeout

    @builtins.property
    def on_event_handler(self) -> _IFunction_1c1de0bc:
        """The AWS Lambda function to invoke for all resource lifecycle operations (CREATE/UPDATE/DELETE).

        This function is responsible to begin the requested resource operation
        (CREATE/UPDATE/DELETE) and return any additional properties to add to the
        event, which will later be passed to ``isComplete``. The ``PhysicalResourceId``
        property must be included in the response.

        stability
        :stability: experimental
        """
        result = self._values.get("on_event_handler")
        assert result is not None, "Required property 'on_event_handler' is missing"
        return result

    @builtins.property
    def is_complete_handler(self) -> typing.Optional[_IFunction_1c1de0bc]:
        """The AWS Lambda function to invoke in order to determine if the operation is complete.

        This function will be called immediately after ``onEvent`` and then
        periodically based on the configured query interval as long as it returns
        ``false``. If the function still returns ``false`` and the alloted timeout has
        passed, the operation will fail.

        default
        :default:

        - provider is synchronous. This means that the ``onEvent`` handler
          is expected to finish all lifecycle operations within the initial invocation.

        stability
        :stability: experimental
        """
        result = self._values.get("is_complete_handler")
        return result

    @builtins.property
    def log_retention(self) -> typing.Optional[_RetentionDays_bdc7ad1f]:
        """The number of days framework log events are kept in CloudWatch Logs.

        When
        updating this property, unsetting it doesn't remove the log retention policy.
        To remove the retention policy, set the value to ``INFINITE``.

        default
        :default: logs.RetentionDays.INFINITE

        stability
        :stability: experimental
        """
        result = self._values.get("log_retention")
        return result

    @builtins.property
    def query_interval(self) -> typing.Optional[_Duration_5170c158]:
        """Time between calls to the ``isComplete`` handler which determines if the resource has been stabilized.

        The first ``isComplete`` will be called immediately after ``handler`` and then
        every ``queryInterval`` seconds, and until ``timeout`` has been reached or until
        ``isComplete`` returns ``true``.

        default
        :default: Duration.seconds(5)

        stability
        :stability: experimental
        """
        result = self._values.get("query_interval")
        return result

    @builtins.property
    def total_timeout(self) -> typing.Optional[_Duration_5170c158]:
        """Total timeout for the entire operation.

        The maximum timeout is 2 hours (yes, it can exceed the AWS Lambda 15 minutes)

        default
        :default: Duration.minutes(30)

        stability
        :stability: experimental
        """
        result = self._values.get("total_timeout")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.custom_resources.SdkCallsPolicyOptions",
    jsii_struct_bases=[],
    name_mapping={"resources": "resources"},
)
class SdkCallsPolicyOptions:
    def __init__(self, *, resources: typing.List[builtins.str]) -> None:
        """Options for the auto-generation of policies based on the configured SDK calls.

        :param resources: The resources that the calls will have access to. It is best to use specific resource ARN's when possible. However, you can also use ``AwsCustomResourcePolicy.ANY_RESOURCE`` to allow access to all resources. For example, when ``onCreate`` is used to create a resource which you don't know the physical name of in advance. Note that will apply to ALL SDK calls.

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "resources": resources,
        }

    @builtins.property
    def resources(self) -> typing.List[builtins.str]:
        """The resources that the calls will have access to.

        It is best to use specific resource ARN's when possible. However, you can also use ``AwsCustomResourcePolicy.ANY_RESOURCE``
        to allow access to all resources. For example, when ``onCreate`` is used to create a resource which you don't
        know the physical name of in advance.

        Note that will apply to ALL SDK calls.

        stability
        :stability: experimental
        """
        result = self._values.get("resources")
        assert result is not None, "Required property 'resources' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SdkCallsPolicyOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AwsCustomResource",
    "AwsCustomResourcePolicy",
    "AwsCustomResourceProps",
    "AwsSdkCall",
    "PhysicalResourceId",
    "PhysicalResourceIdReference",
    "Provider",
    "ProviderProps",
    "SdkCallsPolicyOptions",
]

publication.publish()
