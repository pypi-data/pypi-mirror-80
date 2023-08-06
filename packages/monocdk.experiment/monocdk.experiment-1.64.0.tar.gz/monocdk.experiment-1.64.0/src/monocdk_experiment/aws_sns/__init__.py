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
    CfnResource as _CfnResource_7760e8e4,
    CfnTag as _CfnTag_b4661f1a,
    Construct as _Construct_f50a3f53,
    Duration as _Duration_5170c158,
    IInspectable as _IInspectable_051e6ed8,
    IResolvable as _IResolvable_9ceae33e,
    IResource as _IResource_72f7ee7e,
    Resource as _Resource_884d0774,
    ResourceProps as _ResourceProps_92be6f66,
    TagManager as _TagManager_2508893f,
    TreeInspector as _TreeInspector_154f5999,
)
from ..aws_cloudwatch import (
    Metric as _Metric_53e89548,
    MetricOptions as _MetricOptions_ad2c4d5d,
    Unit as _Unit_e1b74f3c,
)
from ..aws_iam import (
    AddToResourcePolicyResult as _AddToResourcePolicyResult_d2a345d1,
    Grant as _Grant_96af6d2d,
    IGrantable as _IGrantable_0fcfc53a,
    PolicyDocument as _PolicyDocument_1d1bca11,
    PolicyStatement as _PolicyStatement_f75dc775,
)
from ..aws_kms import IKey as _IKey_3336c79d
from ..aws_sqs import IQueue as _IQueue_b743f559


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_sns.BetweenCondition",
    jsii_struct_bases=[],
    name_mapping={"start": "start", "stop": "stop"},
)
class BetweenCondition:
    def __init__(self, *, start: jsii.Number, stop: jsii.Number) -> None:
        """Between condition for a numeric attribute.

        :param start: The start value.
        :param stop: The stop value.

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "start": start,
            "stop": stop,
        }

    @builtins.property
    def start(self) -> jsii.Number:
        """The start value.

        stability
        :stability: experimental
        """
        result = self._values.get("start")
        assert result is not None, "Required property 'start' is missing"
        return result

    @builtins.property
    def stop(self) -> jsii.Number:
        """The stop value.

        stability
        :stability: experimental
        """
        result = self._values.get("stop")
        assert result is not None, "Required property 'stop' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BetweenCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnSubscription(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_sns.CfnSubscription",
):
    """A CloudFormation ``AWS::SNS::Subscription``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html
    cloudformationResource:
    :cloudformationResource:: AWS::SNS::Subscription
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        *,
        protocol: builtins.str,
        topic_arn: builtins.str,
        delivery_policy: typing.Any = None,
        endpoint: typing.Optional[builtins.str] = None,
        filter_policy: typing.Any = None,
        raw_message_delivery: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
        redrive_policy: typing.Any = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::SNS::Subscription``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param protocol: ``AWS::SNS::Subscription.Protocol``.
        :param topic_arn: ``AWS::SNS::Subscription.TopicArn``.
        :param delivery_policy: ``AWS::SNS::Subscription.DeliveryPolicy``.
        :param endpoint: ``AWS::SNS::Subscription.Endpoint``.
        :param filter_policy: ``AWS::SNS::Subscription.FilterPolicy``.
        :param raw_message_delivery: ``AWS::SNS::Subscription.RawMessageDelivery``.
        :param redrive_policy: ``AWS::SNS::Subscription.RedrivePolicy``.
        :param region: ``AWS::SNS::Subscription.Region``.
        """
        props = CfnSubscriptionProps(
            protocol=protocol,
            topic_arn=topic_arn,
            delivery_policy=delivery_policy,
            endpoint=endpoint,
            filter_policy=filter_policy,
            raw_message_delivery=raw_message_delivery,
            redrive_policy=redrive_policy,
            region=region,
        )

        jsii.create(CfnSubscription, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_154f5999) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="deliveryPolicy")
    def delivery_policy(self) -> typing.Any:
        """``AWS::SNS::Subscription.DeliveryPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-deliverypolicy
        """
        return jsii.get(self, "deliveryPolicy")

    @delivery_policy.setter # type: ignore
    def delivery_policy(self, value: typing.Any) -> None:
        jsii.set(self, "deliveryPolicy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="filterPolicy")
    def filter_policy(self) -> typing.Any:
        """``AWS::SNS::Subscription.FilterPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-filterpolicy
        """
        return jsii.get(self, "filterPolicy")

    @filter_policy.setter # type: ignore
    def filter_policy(self, value: typing.Any) -> None:
        jsii.set(self, "filterPolicy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        """``AWS::SNS::Subscription.Protocol``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-protocol
        """
        return jsii.get(self, "protocol")

    @protocol.setter # type: ignore
    def protocol(self, value: builtins.str) -> None:
        jsii.set(self, "protocol", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="redrivePolicy")
    def redrive_policy(self) -> typing.Any:
        """``AWS::SNS::Subscription.RedrivePolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-redrivepolicy
        """
        return jsii.get(self, "redrivePolicy")

    @redrive_policy.setter # type: ignore
    def redrive_policy(self, value: typing.Any) -> None:
        jsii.set(self, "redrivePolicy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> builtins.str:
        """``AWS::SNS::Subscription.TopicArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#topicarn
        """
        return jsii.get(self, "topicArn")

    @topic_arn.setter # type: ignore
    def topic_arn(self, value: builtins.str) -> None:
        jsii.set(self, "topicArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> typing.Optional[builtins.str]:
        """``AWS::SNS::Subscription.Endpoint``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-endpoint
        """
        return jsii.get(self, "endpoint")

    @endpoint.setter # type: ignore
    def endpoint(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "endpoint", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="rawMessageDelivery")
    def raw_message_delivery(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
        """``AWS::SNS::Subscription.RawMessageDelivery``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-rawmessagedelivery
        """
        return jsii.get(self, "rawMessageDelivery")

    @raw_message_delivery.setter # type: ignore
    def raw_message_delivery(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "rawMessageDelivery", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        """``AWS::SNS::Subscription.Region``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-region
        """
        return jsii.get(self, "region")

    @region.setter # type: ignore
    def region(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "region", value)


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_sns.CfnSubscriptionProps",
    jsii_struct_bases=[],
    name_mapping={
        "protocol": "protocol",
        "topic_arn": "topicArn",
        "delivery_policy": "deliveryPolicy",
        "endpoint": "endpoint",
        "filter_policy": "filterPolicy",
        "raw_message_delivery": "rawMessageDelivery",
        "redrive_policy": "redrivePolicy",
        "region": "region",
    },
)
class CfnSubscriptionProps:
    def __init__(
        self,
        *,
        protocol: builtins.str,
        topic_arn: builtins.str,
        delivery_policy: typing.Any = None,
        endpoint: typing.Optional[builtins.str] = None,
        filter_policy: typing.Any = None,
        raw_message_delivery: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
        redrive_policy: typing.Any = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::SNS::Subscription``.

        :param protocol: ``AWS::SNS::Subscription.Protocol``.
        :param topic_arn: ``AWS::SNS::Subscription.TopicArn``.
        :param delivery_policy: ``AWS::SNS::Subscription.DeliveryPolicy``.
        :param endpoint: ``AWS::SNS::Subscription.Endpoint``.
        :param filter_policy: ``AWS::SNS::Subscription.FilterPolicy``.
        :param raw_message_delivery: ``AWS::SNS::Subscription.RawMessageDelivery``.
        :param redrive_policy: ``AWS::SNS::Subscription.RedrivePolicy``.
        :param region: ``AWS::SNS::Subscription.Region``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "protocol": protocol,
            "topic_arn": topic_arn,
        }
        if delivery_policy is not None:
            self._values["delivery_policy"] = delivery_policy
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if filter_policy is not None:
            self._values["filter_policy"] = filter_policy
        if raw_message_delivery is not None:
            self._values["raw_message_delivery"] = raw_message_delivery
        if redrive_policy is not None:
            self._values["redrive_policy"] = redrive_policy
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def protocol(self) -> builtins.str:
        """``AWS::SNS::Subscription.Protocol``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-protocol
        """
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return result

    @builtins.property
    def topic_arn(self) -> builtins.str:
        """``AWS::SNS::Subscription.TopicArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#topicarn
        """
        result = self._values.get("topic_arn")
        assert result is not None, "Required property 'topic_arn' is missing"
        return result

    @builtins.property
    def delivery_policy(self) -> typing.Any:
        """``AWS::SNS::Subscription.DeliveryPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-deliverypolicy
        """
        result = self._values.get("delivery_policy")
        return result

    @builtins.property
    def endpoint(self) -> typing.Optional[builtins.str]:
        """``AWS::SNS::Subscription.Endpoint``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-endpoint
        """
        result = self._values.get("endpoint")
        return result

    @builtins.property
    def filter_policy(self) -> typing.Any:
        """``AWS::SNS::Subscription.FilterPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-filterpolicy
        """
        result = self._values.get("filter_policy")
        return result

    @builtins.property
    def raw_message_delivery(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
        """``AWS::SNS::Subscription.RawMessageDelivery``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-rawmessagedelivery
        """
        result = self._values.get("raw_message_delivery")
        return result

    @builtins.property
    def redrive_policy(self) -> typing.Any:
        """``AWS::SNS::Subscription.RedrivePolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-redrivepolicy
        """
        result = self._values.get("redrive_policy")
        return result

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        """``AWS::SNS::Subscription.Region``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-region
        """
        result = self._values.get("region")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSubscriptionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnTopic(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_sns.CfnTopic",
):
    """A CloudFormation ``AWS::SNS::Topic``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html
    cloudformationResource:
    :cloudformationResource:: AWS::SNS::Topic
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        *,
        content_based_deduplication: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
        display_name: typing.Optional[builtins.str] = None,
        kms_master_key_id: typing.Optional[builtins.str] = None,
        subscription: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["SubscriptionProperty", _IResolvable_9ceae33e]]]] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
        topic_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::SNS::Topic``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param content_based_deduplication: ``AWS::SNS::Topic.ContentBasedDeduplication``.
        :param display_name: ``AWS::SNS::Topic.DisplayName``.
        :param kms_master_key_id: ``AWS::SNS::Topic.KmsMasterKeyId``.
        :param subscription: ``AWS::SNS::Topic.Subscription``.
        :param tags: ``AWS::SNS::Topic.Tags``.
        :param topic_name: ``AWS::SNS::Topic.TopicName``.
        """
        props = CfnTopicProps(
            content_based_deduplication=content_based_deduplication,
            display_name=display_name,
            kms_master_key_id=kms_master_key_id,
            subscription=subscription,
            tags=tags,
            topic_name=topic_name,
        )

        jsii.create(CfnTopic, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_154f5999) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrTopicName")
    def attr_topic_name(self) -> builtins.str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: TopicName
        """
        return jsii.get(self, "attrTopicName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::SNS::Topic.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="contentBasedDeduplication")
    def content_based_deduplication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
        """``AWS::SNS::Topic.ContentBasedDeduplication``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-contentbaseddeduplication
        """
        return jsii.get(self, "contentBasedDeduplication")

    @content_based_deduplication.setter # type: ignore
    def content_based_deduplication(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "contentBasedDeduplication", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> typing.Optional[builtins.str]:
        """``AWS::SNS::Topic.DisplayName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-displayname
        """
        return jsii.get(self, "displayName")

    @display_name.setter # type: ignore
    def display_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "displayName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="kmsMasterKeyId")
    def kms_master_key_id(self) -> typing.Optional[builtins.str]:
        """``AWS::SNS::Topic.KmsMasterKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-kmsmasterkeyid
        """
        return jsii.get(self, "kmsMasterKeyId")

    @kms_master_key_id.setter # type: ignore
    def kms_master_key_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "kmsMasterKeyId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="subscription")
    def subscription(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["SubscriptionProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::SNS::Topic.Subscription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-subscription
        """
        return jsii.get(self, "subscription")

    @subscription.setter # type: ignore
    def subscription(
        self,
        value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["SubscriptionProperty", _IResolvable_9ceae33e]]]],
    ) -> None:
        jsii.set(self, "subscription", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> typing.Optional[builtins.str]:
        """``AWS::SNS::Topic.TopicName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-topicname
        """
        return jsii.get(self, "topicName")

    @topic_name.setter # type: ignore
    def topic_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "topicName", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_sns.CfnTopic.SubscriptionProperty",
        jsii_struct_bases=[],
        name_mapping={"endpoint": "endpoint", "protocol": "protocol"},
    )
    class SubscriptionProperty:
        def __init__(self, *, endpoint: builtins.str, protocol: builtins.str) -> None:
            """
            :param endpoint: ``CfnTopic.SubscriptionProperty.Endpoint``.
            :param protocol: ``CfnTopic.SubscriptionProperty.Protocol``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-subscription.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "endpoint": endpoint,
                "protocol": protocol,
            }

        @builtins.property
        def endpoint(self) -> builtins.str:
            """``CfnTopic.SubscriptionProperty.Endpoint``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-subscription.html#cfn-sns-topic-subscription-endpoint
            """
            result = self._values.get("endpoint")
            assert result is not None, "Required property 'endpoint' is missing"
            return result

        @builtins.property
        def protocol(self) -> builtins.str:
            """``CfnTopic.SubscriptionProperty.Protocol``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-subscription.html#cfn-sns-topic-subscription-protocol
            """
            result = self._values.get("protocol")
            assert result is not None, "Required property 'protocol' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubscriptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_051e6ed8)
class CfnTopicPolicy(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_sns.CfnTopicPolicy",
):
    """A CloudFormation ``AWS::SNS::TopicPolicy``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html
    cloudformationResource:
    :cloudformationResource:: AWS::SNS::TopicPolicy
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        *,
        policy_document: typing.Any,
        topics: typing.List[builtins.str],
    ) -> None:
        """Create a new ``AWS::SNS::TopicPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy_document: ``AWS::SNS::TopicPolicy.PolicyDocument``.
        :param topics: ``AWS::SNS::TopicPolicy.Topics``.
        """
        props = CfnTopicPolicyProps(policy_document=policy_document, topics=topics)

        jsii.create(CfnTopicPolicy, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_154f5999) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="policyDocument")
    def policy_document(self) -> typing.Any:
        """``AWS::SNS::TopicPolicy.PolicyDocument``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html#cfn-sns-topicpolicy-policydocument
        """
        return jsii.get(self, "policyDocument")

    @policy_document.setter # type: ignore
    def policy_document(self, value: typing.Any) -> None:
        jsii.set(self, "policyDocument", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="topics")
    def topics(self) -> typing.List[builtins.str]:
        """``AWS::SNS::TopicPolicy.Topics``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html#cfn-sns-topicpolicy-topics
        """
        return jsii.get(self, "topics")

    @topics.setter # type: ignore
    def topics(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "topics", value)


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_sns.CfnTopicPolicyProps",
    jsii_struct_bases=[],
    name_mapping={"policy_document": "policyDocument", "topics": "topics"},
)
class CfnTopicPolicyProps:
    def __init__(
        self,
        *,
        policy_document: typing.Any,
        topics: typing.List[builtins.str],
    ) -> None:
        """Properties for defining a ``AWS::SNS::TopicPolicy``.

        :param policy_document: ``AWS::SNS::TopicPolicy.PolicyDocument``.
        :param topics: ``AWS::SNS::TopicPolicy.Topics``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "policy_document": policy_document,
            "topics": topics,
        }

    @builtins.property
    def policy_document(self) -> typing.Any:
        """``AWS::SNS::TopicPolicy.PolicyDocument``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html#cfn-sns-topicpolicy-policydocument
        """
        result = self._values.get("policy_document")
        assert result is not None, "Required property 'policy_document' is missing"
        return result

    @builtins.property
    def topics(self) -> typing.List[builtins.str]:
        """``AWS::SNS::TopicPolicy.Topics``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html#cfn-sns-topicpolicy-topics
        """
        result = self._values.get("topics")
        assert result is not None, "Required property 'topics' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTopicPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_sns.CfnTopicProps",
    jsii_struct_bases=[],
    name_mapping={
        "content_based_deduplication": "contentBasedDeduplication",
        "display_name": "displayName",
        "kms_master_key_id": "kmsMasterKeyId",
        "subscription": "subscription",
        "tags": "tags",
        "topic_name": "topicName",
    },
)
class CfnTopicProps:
    def __init__(
        self,
        *,
        content_based_deduplication: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
        display_name: typing.Optional[builtins.str] = None,
        kms_master_key_id: typing.Optional[builtins.str] = None,
        subscription: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTopic.SubscriptionProperty", _IResolvable_9ceae33e]]]] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
        topic_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::SNS::Topic``.

        :param content_based_deduplication: ``AWS::SNS::Topic.ContentBasedDeduplication``.
        :param display_name: ``AWS::SNS::Topic.DisplayName``.
        :param kms_master_key_id: ``AWS::SNS::Topic.KmsMasterKeyId``.
        :param subscription: ``AWS::SNS::Topic.Subscription``.
        :param tags: ``AWS::SNS::Topic.Tags``.
        :param topic_name: ``AWS::SNS::Topic.TopicName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if content_based_deduplication is not None:
            self._values["content_based_deduplication"] = content_based_deduplication
        if display_name is not None:
            self._values["display_name"] = display_name
        if kms_master_key_id is not None:
            self._values["kms_master_key_id"] = kms_master_key_id
        if subscription is not None:
            self._values["subscription"] = subscription
        if tags is not None:
            self._values["tags"] = tags
        if topic_name is not None:
            self._values["topic_name"] = topic_name

    @builtins.property
    def content_based_deduplication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
        """``AWS::SNS::Topic.ContentBasedDeduplication``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-contentbaseddeduplication
        """
        result = self._values.get("content_based_deduplication")
        return result

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        """``AWS::SNS::Topic.DisplayName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-displayname
        """
        result = self._values.get("display_name")
        return result

    @builtins.property
    def kms_master_key_id(self) -> typing.Optional[builtins.str]:
        """``AWS::SNS::Topic.KmsMasterKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-kmsmasterkeyid
        """
        result = self._values.get("kms_master_key_id")
        return result

    @builtins.property
    def subscription(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTopic.SubscriptionProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::SNS::Topic.Subscription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-subscription
        """
        result = self._values.get("subscription")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::SNS::Topic.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def topic_name(self) -> typing.Optional[builtins.str]:
        """``AWS::SNS::Topic.TopicName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-topicname
        """
        result = self._values.get("topic_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTopicProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk-experiment.aws_sns.ITopic")
class ITopic(_IResource_72f7ee7e, typing_extensions.Protocol):
    """Represents an SNS topic.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ITopicProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> builtins.str:
        """The ARN of the topic.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> builtins.str:
        """The name of the topic.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @jsii.member(jsii_name="addSubscription")
    def add_subscription(self, subscription: "ITopicSubscription") -> None:
        """Subscribe some endpoint to this topic.

        :param subscription: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _PolicyStatement_f75dc775,
    ) -> _AddToResourcePolicyResult_d2a345d1:
        """Adds a statement to the IAM resource policy associated with this topic.

        If this topic was created in this stack (``new Topic``), a topic policy
        will be automatically created upon the first call to ``addToPolicy``. If
        the topic is imported (``Topic.import``), then this is a no-op.

        :param statement: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(self, identity: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grant topic publishing permissions to the given identity.

        :param identity: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """Return the given named metric for this Topic.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricNumberOfMessagesPublished")
    def metric_number_of_messages_published(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """The number of messages published to your Amazon SNS topics.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricNumberOfNotificationsDelivered")
    def metric_number_of_notifications_delivered(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """The number of messages successfully delivered from your Amazon SNS topics to subscribing endpoints.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricNumberOfNotificationsFailed")
    def metric_number_of_notifications_failed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """The number of messages that Amazon SNS failed to deliver.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOut")
    def metric_number_of_notifications_filtered_out(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """The number of messages that were rejected by subscription filter policies.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutInvalidAttributes")
    def metric_number_of_notifications_filtered_out_invalid_attributes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """The number of messages that were rejected by subscription filter policies because the messages' attributes are invalid.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutNoMessageAttributes")
    def metric_number_of_notifications_filtered_out_no_message_attributes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """The number of messages that were rejected by subscription filter policies because the messages have no attributes.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricPublishSize")
    def metric_publish_size(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """Metric for the size of messages published through this topic.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricSMSMonthToDateSpentUSD")
    def metric_sms_month_to_date_spent_usd(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """The charges you have accrued since the start of the current calendar month for sending SMS messages.

        Maximum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricSMSSuccessRate")
    def metric_sms_success_rate(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """The rate of successful SMS message deliveries.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        ...


class _ITopicProxy(
    jsii.proxy_for(_IResource_72f7ee7e) # type: ignore
):
    """Represents an SNS topic.

    stability
    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "monocdk-experiment.aws_sns.ITopic"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> builtins.str:
        """The ARN of the topic.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "topicArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> builtins.str:
        """The name of the topic.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "topicName")

    @jsii.member(jsii_name="addSubscription")
    def add_subscription(self, subscription: "ITopicSubscription") -> None:
        """Subscribe some endpoint to this topic.

        :param subscription: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addSubscription", [subscription])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _PolicyStatement_f75dc775,
    ) -> _AddToResourcePolicyResult_d2a345d1:
        """Adds a statement to the IAM resource policy associated with this topic.

        If this topic was created in this stack (``new Topic``), a topic policy
        will be automatically created upon the first call to ``addToPolicy``. If
        the topic is imported (``Topic.import``), then this is a no-op.

        :param statement: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(self, identity: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grant topic publishing permissions to the given identity.

        :param identity: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantPublish", [identity])

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """Return the given named metric for this Topic.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricNumberOfMessagesPublished")
    def metric_number_of_messages_published(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """The number of messages published to your Amazon SNS topics.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricNumberOfMessagesPublished", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsDelivered")
    def metric_number_of_notifications_delivered(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """The number of messages successfully delivered from your Amazon SNS topics to subscribing endpoints.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricNumberOfNotificationsDelivered", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFailed")
    def metric_number_of_notifications_failed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """The number of messages that Amazon SNS failed to deliver.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricNumberOfNotificationsFailed", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOut")
    def metric_number_of_notifications_filtered_out(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """The number of messages that were rejected by subscription filter policies.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricNumberOfNotificationsFilteredOut", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutInvalidAttributes")
    def metric_number_of_notifications_filtered_out_invalid_attributes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """The number of messages that were rejected by subscription filter policies because the messages' attributes are invalid.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricNumberOfNotificationsFilteredOutInvalidAttributes", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutNoMessageAttributes")
    def metric_number_of_notifications_filtered_out_no_message_attributes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """The number of messages that were rejected by subscription filter policies because the messages have no attributes.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricNumberOfNotificationsFilteredOutNoMessageAttributes", [props])

    @jsii.member(jsii_name="metricPublishSize")
    def metric_publish_size(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """Metric for the size of messages published through this topic.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricPublishSize", [props])

    @jsii.member(jsii_name="metricSMSMonthToDateSpentUSD")
    def metric_sms_month_to_date_spent_usd(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """The charges you have accrued since the start of the current calendar month for sending SMS messages.

        Maximum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricSMSMonthToDateSpentUSD", [props])

    @jsii.member(jsii_name="metricSMSSuccessRate")
    def metric_sms_success_rate(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """The rate of successful SMS message deliveries.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricSMSSuccessRate", [props])


@jsii.interface(jsii_type="monocdk-experiment.aws_sns.ITopicSubscription")
class ITopicSubscription(typing_extensions.Protocol):
    """Topic subscription.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ITopicSubscriptionProxy

    @jsii.member(jsii_name="bind")
    def bind(self, topic: "ITopic") -> "TopicSubscriptionConfig":
        """Returns a configuration used to subscribe to an SNS topic.

        :param topic: topic for which subscription will be configured.

        stability
        :stability: experimental
        """
        ...


class _ITopicSubscriptionProxy:
    """Topic subscription.

    stability
    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "monocdk-experiment.aws_sns.ITopicSubscription"

    @jsii.member(jsii_name="bind")
    def bind(self, topic: "ITopic") -> "TopicSubscriptionConfig":
        """Returns a configuration used to subscribe to an SNS topic.

        :param topic: topic for which subscription will be configured.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [topic])


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_sns.NumericConditions",
    jsii_struct_bases=[],
    name_mapping={
        "between": "between",
        "between_strict": "betweenStrict",
        "greater_than": "greaterThan",
        "greater_than_or_equal_to": "greaterThanOrEqualTo",
        "less_than": "lessThan",
        "less_than_or_equal_to": "lessThanOrEqualTo",
        "whitelist": "whitelist",
    },
)
class NumericConditions:
    def __init__(
        self,
        *,
        between: typing.Optional["BetweenCondition"] = None,
        between_strict: typing.Optional["BetweenCondition"] = None,
        greater_than: typing.Optional[jsii.Number] = None,
        greater_than_or_equal_to: typing.Optional[jsii.Number] = None,
        less_than: typing.Optional[jsii.Number] = None,
        less_than_or_equal_to: typing.Optional[jsii.Number] = None,
        whitelist: typing.Optional[typing.List[jsii.Number]] = None,
    ) -> None:
        """Conditions that can be applied to numeric attributes.

        :param between: Match values that are between the specified values. Default: - None
        :param between_strict: Match values that are strictly between the specified values. Default: - None
        :param greater_than: Match values that are greater than the specified value. Default: - None
        :param greater_than_or_equal_to: Match values that are greater than or equal to the specified value. Default: - None
        :param less_than: Match values that are less than the specified value. Default: - None
        :param less_than_or_equal_to: Match values that are less than or equal to the specified value. Default: - None
        :param whitelist: Match one or more values. Default: - None

        stability
        :stability: experimental
        """
        if isinstance(between, dict):
            between = BetweenCondition(**between)
        if isinstance(between_strict, dict):
            between_strict = BetweenCondition(**between_strict)
        self._values: typing.Dict[str, typing.Any] = {}
        if between is not None:
            self._values["between"] = between
        if between_strict is not None:
            self._values["between_strict"] = between_strict
        if greater_than is not None:
            self._values["greater_than"] = greater_than
        if greater_than_or_equal_to is not None:
            self._values["greater_than_or_equal_to"] = greater_than_or_equal_to
        if less_than is not None:
            self._values["less_than"] = less_than
        if less_than_or_equal_to is not None:
            self._values["less_than_or_equal_to"] = less_than_or_equal_to
        if whitelist is not None:
            self._values["whitelist"] = whitelist

    @builtins.property
    def between(self) -> typing.Optional["BetweenCondition"]:
        """Match values that are between the specified values.

        default
        :default: - None

        stability
        :stability: experimental
        """
        result = self._values.get("between")
        return result

    @builtins.property
    def between_strict(self) -> typing.Optional["BetweenCondition"]:
        """Match values that are strictly between the specified values.

        default
        :default: - None

        stability
        :stability: experimental
        """
        result = self._values.get("between_strict")
        return result

    @builtins.property
    def greater_than(self) -> typing.Optional[jsii.Number]:
        """Match values that are greater than the specified value.

        default
        :default: - None

        stability
        :stability: experimental
        """
        result = self._values.get("greater_than")
        return result

    @builtins.property
    def greater_than_or_equal_to(self) -> typing.Optional[jsii.Number]:
        """Match values that are greater than or equal to the specified value.

        default
        :default: - None

        stability
        :stability: experimental
        """
        result = self._values.get("greater_than_or_equal_to")
        return result

    @builtins.property
    def less_than(self) -> typing.Optional[jsii.Number]:
        """Match values that are less than the specified value.

        default
        :default: - None

        stability
        :stability: experimental
        """
        result = self._values.get("less_than")
        return result

    @builtins.property
    def less_than_or_equal_to(self) -> typing.Optional[jsii.Number]:
        """Match values that are less than or equal to the specified value.

        default
        :default: - None

        stability
        :stability: experimental
        """
        result = self._values.get("less_than_or_equal_to")
        return result

    @builtins.property
    def whitelist(self) -> typing.Optional[typing.List[jsii.Number]]:
        """Match one or more values.

        default
        :default: - None

        stability
        :stability: experimental
        """
        result = self._values.get("whitelist")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NumericConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_sns.StringConditions",
    jsii_struct_bases=[],
    name_mapping={
        "blacklist": "blacklist",
        "match_prefixes": "matchPrefixes",
        "whitelist": "whitelist",
    },
)
class StringConditions:
    def __init__(
        self,
        *,
        blacklist: typing.Optional[typing.List[builtins.str]] = None,
        match_prefixes: typing.Optional[typing.List[builtins.str]] = None,
        whitelist: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Conditions that can be applied to string attributes.

        :param blacklist: Match any value that doesn't include any of the specified values. Default: - None
        :param match_prefixes: Matches values that begins with the specified prefixes. Default: - None
        :param whitelist: Match one or more values. Default: - None

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if blacklist is not None:
            self._values["blacklist"] = blacklist
        if match_prefixes is not None:
            self._values["match_prefixes"] = match_prefixes
        if whitelist is not None:
            self._values["whitelist"] = whitelist

    @builtins.property
    def blacklist(self) -> typing.Optional[typing.List[builtins.str]]:
        """Match any value that doesn't include any of the specified values.

        default
        :default: - None

        stability
        :stability: experimental
        """
        result = self._values.get("blacklist")
        return result

    @builtins.property
    def match_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        """Matches values that begins with the specified prefixes.

        default
        :default: - None

        stability
        :stability: experimental
        """
        result = self._values.get("match_prefixes")
        return result

    @builtins.property
    def whitelist(self) -> typing.Optional[typing.List[builtins.str]]:
        """Match one or more values.

        default
        :default: - None

        stability
        :stability: experimental
        """
        result = self._values.get("whitelist")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StringConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Subscription(
    _Resource_884d0774,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_sns.Subscription",
):
    """A new subscription.

    Prefer to use the ``ITopic.addSubscription()`` methods to create instances of
    this class.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        *,
        topic: "ITopic",
        endpoint: builtins.str,
        protocol: "SubscriptionProtocol",
        dead_letter_queue: typing.Optional[_IQueue_b743f559] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, "SubscriptionFilter"]] = None,
        raw_message_delivery: typing.Optional[builtins.bool] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param topic: The topic to subscribe to.
        :param endpoint: The subscription endpoint. The meaning of this value depends on the value for 'protocol'.
        :param protocol: What type of subscription to add.
        :param dead_letter_queue: Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: The filter policy. Default: - all messages are delivered
        :param raw_message_delivery: true if raw message delivery is enabled for the subscription. Raw messages are free of JSON formatting and can be sent to HTTP/S and Amazon SQS endpoints. For more information, see GetSubscriptionAttributes in the Amazon Simple Notification Service API Reference. Default: false
        :param region: The region where the topic resides, in the case of cross-region subscriptions. Default: - the region where the CloudFormation stack is being deployed.

        stability
        :stability: experimental
        """
        props = SubscriptionProps(
            topic=topic,
            endpoint=endpoint,
            protocol=protocol,
            dead_letter_queue=dead_letter_queue,
            filter_policy=filter_policy,
            raw_message_delivery=raw_message_delivery,
            region=region,
        )

        jsii.create(Subscription, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="deadLetterQueue")
    def dead_letter_queue(self) -> typing.Optional[_IQueue_b743f559]:
        """The DLQ associated with this subscription if present.

        stability
        :stability: experimental
        """
        return jsii.get(self, "deadLetterQueue")


class SubscriptionFilter(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_sns.SubscriptionFilter",
):
    """A subscription filter for an attribute.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        conditions: typing.Optional[typing.List[typing.Any]] = None,
    ) -> None:
        """
        :param conditions: conditions that specify the message attributes that should be included, excluded, matched, etc.

        stability
        :stability: experimental
        """
        jsii.create(SubscriptionFilter, self, [conditions])

    @jsii.member(jsii_name="existsFilter")
    @builtins.classmethod
    def exists_filter(cls) -> "SubscriptionFilter":
        """Returns a subscription filter for attribute key matching.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "existsFilter", [])

    @jsii.member(jsii_name="numericFilter")
    @builtins.classmethod
    def numeric_filter(
        cls,
        *,
        between: typing.Optional["BetweenCondition"] = None,
        between_strict: typing.Optional["BetweenCondition"] = None,
        greater_than: typing.Optional[jsii.Number] = None,
        greater_than_or_equal_to: typing.Optional[jsii.Number] = None,
        less_than: typing.Optional[jsii.Number] = None,
        less_than_or_equal_to: typing.Optional[jsii.Number] = None,
        whitelist: typing.Optional[typing.List[jsii.Number]] = None,
    ) -> "SubscriptionFilter":
        """Returns a subscription filter for a numeric attribute.

        :param between: Match values that are between the specified values. Default: - None
        :param between_strict: Match values that are strictly between the specified values. Default: - None
        :param greater_than: Match values that are greater than the specified value. Default: - None
        :param greater_than_or_equal_to: Match values that are greater than or equal to the specified value. Default: - None
        :param less_than: Match values that are less than the specified value. Default: - None
        :param less_than_or_equal_to: Match values that are less than or equal to the specified value. Default: - None
        :param whitelist: Match one or more values. Default: - None

        stability
        :stability: experimental
        """
        numeric_conditions = NumericConditions(
            between=between,
            between_strict=between_strict,
            greater_than=greater_than,
            greater_than_or_equal_to=greater_than_or_equal_to,
            less_than=less_than,
            less_than_or_equal_to=less_than_or_equal_to,
            whitelist=whitelist,
        )

        return jsii.sinvoke(cls, "numericFilter", [numeric_conditions])

    @jsii.member(jsii_name="stringFilter")
    @builtins.classmethod
    def string_filter(
        cls,
        *,
        blacklist: typing.Optional[typing.List[builtins.str]] = None,
        match_prefixes: typing.Optional[typing.List[builtins.str]] = None,
        whitelist: typing.Optional[typing.List[builtins.str]] = None,
    ) -> "SubscriptionFilter":
        """Returns a subscription filter for a string attribute.

        :param blacklist: Match any value that doesn't include any of the specified values. Default: - None
        :param match_prefixes: Matches values that begins with the specified prefixes. Default: - None
        :param whitelist: Match one or more values. Default: - None

        stability
        :stability: experimental
        """
        string_conditions = StringConditions(
            blacklist=blacklist, match_prefixes=match_prefixes, whitelist=whitelist
        )

        return jsii.sinvoke(cls, "stringFilter", [string_conditions])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> typing.List[typing.Any]:
        """conditions that specify the message attributes that should be included, excluded, matched, etc.

        stability
        :stability: experimental
        """
        return jsii.get(self, "conditions")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_sns.SubscriptionOptions",
    jsii_struct_bases=[],
    name_mapping={
        "endpoint": "endpoint",
        "protocol": "protocol",
        "dead_letter_queue": "deadLetterQueue",
        "filter_policy": "filterPolicy",
        "raw_message_delivery": "rawMessageDelivery",
        "region": "region",
    },
)
class SubscriptionOptions:
    def __init__(
        self,
        *,
        endpoint: builtins.str,
        protocol: "SubscriptionProtocol",
        dead_letter_queue: typing.Optional[_IQueue_b743f559] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, "SubscriptionFilter"]] = None,
        raw_message_delivery: typing.Optional[builtins.bool] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        """Options for creating a new subscription.

        :param endpoint: The subscription endpoint. The meaning of this value depends on the value for 'protocol'.
        :param protocol: What type of subscription to add.
        :param dead_letter_queue: Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: The filter policy. Default: - all messages are delivered
        :param raw_message_delivery: true if raw message delivery is enabled for the subscription. Raw messages are free of JSON formatting and can be sent to HTTP/S and Amazon SQS endpoints. For more information, see GetSubscriptionAttributes in the Amazon Simple Notification Service API Reference. Default: false
        :param region: The region where the topic resides, in the case of cross-region subscriptions. Default: - the region where the CloudFormation stack is being deployed.

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "endpoint": endpoint,
            "protocol": protocol,
        }
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None:
            self._values["filter_policy"] = filter_policy
        if raw_message_delivery is not None:
            self._values["raw_message_delivery"] = raw_message_delivery
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def endpoint(self) -> builtins.str:
        """The subscription endpoint.

        The meaning of this value depends on the value for 'protocol'.

        stability
        :stability: experimental
        """
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return result

    @builtins.property
    def protocol(self) -> "SubscriptionProtocol":
        """What type of subscription to add.

        stability
        :stability: experimental
        """
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return result

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_b743f559]:
        """Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        default
        :default: - No dead letter queue enabled.

        stability
        :stability: experimental
        """
        result = self._values.get("dead_letter_queue")
        return result

    @builtins.property
    def filter_policy(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "SubscriptionFilter"]]:
        """The filter policy.

        default
        :default: - all messages are delivered

        stability
        :stability: experimental
        """
        result = self._values.get("filter_policy")
        return result

    @builtins.property
    def raw_message_delivery(self) -> typing.Optional[builtins.bool]:
        """true if raw message delivery is enabled for the subscription.

        Raw messages are free of JSON formatting and can be
        sent to HTTP/S and Amazon SQS endpoints. For more information, see GetSubscriptionAttributes in the Amazon Simple
        Notification Service API Reference.

        default
        :default: false

        stability
        :stability: experimental
        """
        result = self._values.get("raw_message_delivery")
        return result

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        """The region where the topic resides, in the case of cross-region subscriptions.

        default
        :default: - the region where the CloudFormation stack is being deployed.

        stability
        :stability: experimental
        link:
        :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-region
        """
        result = self._values.get("region")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubscriptionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_sns.SubscriptionProps",
    jsii_struct_bases=[SubscriptionOptions],
    name_mapping={
        "endpoint": "endpoint",
        "protocol": "protocol",
        "dead_letter_queue": "deadLetterQueue",
        "filter_policy": "filterPolicy",
        "raw_message_delivery": "rawMessageDelivery",
        "region": "region",
        "topic": "topic",
    },
)
class SubscriptionProps(SubscriptionOptions):
    def __init__(
        self,
        *,
        endpoint: builtins.str,
        protocol: "SubscriptionProtocol",
        dead_letter_queue: typing.Optional[_IQueue_b743f559] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, "SubscriptionFilter"]] = None,
        raw_message_delivery: typing.Optional[builtins.bool] = None,
        region: typing.Optional[builtins.str] = None,
        topic: "ITopic",
    ) -> None:
        """Properties for creating a new subscription.

        :param endpoint: The subscription endpoint. The meaning of this value depends on the value for 'protocol'.
        :param protocol: What type of subscription to add.
        :param dead_letter_queue: Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: The filter policy. Default: - all messages are delivered
        :param raw_message_delivery: true if raw message delivery is enabled for the subscription. Raw messages are free of JSON formatting and can be sent to HTTP/S and Amazon SQS endpoints. For more information, see GetSubscriptionAttributes in the Amazon Simple Notification Service API Reference. Default: false
        :param region: The region where the topic resides, in the case of cross-region subscriptions. Default: - the region where the CloudFormation stack is being deployed.
        :param topic: The topic to subscribe to.

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "endpoint": endpoint,
            "protocol": protocol,
            "topic": topic,
        }
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None:
            self._values["filter_policy"] = filter_policy
        if raw_message_delivery is not None:
            self._values["raw_message_delivery"] = raw_message_delivery
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def endpoint(self) -> builtins.str:
        """The subscription endpoint.

        The meaning of this value depends on the value for 'protocol'.

        stability
        :stability: experimental
        """
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return result

    @builtins.property
    def protocol(self) -> "SubscriptionProtocol":
        """What type of subscription to add.

        stability
        :stability: experimental
        """
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return result

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_b743f559]:
        """Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        default
        :default: - No dead letter queue enabled.

        stability
        :stability: experimental
        """
        result = self._values.get("dead_letter_queue")
        return result

    @builtins.property
    def filter_policy(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "SubscriptionFilter"]]:
        """The filter policy.

        default
        :default: - all messages are delivered

        stability
        :stability: experimental
        """
        result = self._values.get("filter_policy")
        return result

    @builtins.property
    def raw_message_delivery(self) -> typing.Optional[builtins.bool]:
        """true if raw message delivery is enabled for the subscription.

        Raw messages are free of JSON formatting and can be
        sent to HTTP/S and Amazon SQS endpoints. For more information, see GetSubscriptionAttributes in the Amazon Simple
        Notification Service API Reference.

        default
        :default: false

        stability
        :stability: experimental
        """
        result = self._values.get("raw_message_delivery")
        return result

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        """The region where the topic resides, in the case of cross-region subscriptions.

        default
        :default: - the region where the CloudFormation stack is being deployed.

        stability
        :stability: experimental
        link:
        :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-region
        """
        result = self._values.get("region")
        return result

    @builtins.property
    def topic(self) -> "ITopic":
        """The topic to subscribe to.

        stability
        :stability: experimental
        """
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubscriptionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk-experiment.aws_sns.SubscriptionProtocol")
class SubscriptionProtocol(enum.Enum):
    """The type of subscription, controlling the type of the endpoint parameter.

    stability
    :stability: experimental
    """

    HTTP = "HTTP"
    """JSON-encoded message is POSTED to an HTTP url.

    stability
    :stability: experimental
    """
    HTTPS = "HTTPS"
    """JSON-encoded message is POSTed to an HTTPS url.

    stability
    :stability: experimental
    """
    EMAIL = "EMAIL"
    """Notifications are sent via email.

    stability
    :stability: experimental
    """
    EMAIL_JSON = "EMAIL_JSON"
    """Notifications are JSON-encoded and sent via mail.

    stability
    :stability: experimental
    """
    SMS = "SMS"
    """Notification is delivered by SMS.

    stability
    :stability: experimental
    """
    SQS = "SQS"
    """Notifications are enqueued into an SQS queue.

    stability
    :stability: experimental
    """
    APPLICATION = "APPLICATION"
    """JSON-encoded notifications are sent to a mobile app endpoint.

    stability
    :stability: experimental
    """
    LAMBDA = "LAMBDA"
    """Notifications trigger a Lambda function.

    stability
    :stability: experimental
    """


@jsii.implements(ITopic)
class TopicBase(
    _Resource_884d0774,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk-experiment.aws_sns.TopicBase",
):
    """Either a new or imported Topic.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _TopicBaseProxy

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to

        stability
        :stability: experimental
        """
        props = _ResourceProps_92be6f66(
            account=account, physical_name=physical_name, region=region
        )

        jsii.create(TopicBase, self, [scope, id, props])

    @jsii.member(jsii_name="addSubscription")
    def add_subscription(self, subscription: "ITopicSubscription") -> None:
        """Subscribe some endpoint to this topic.

        :param subscription: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addSubscription", [subscription])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _PolicyStatement_f75dc775,
    ) -> _AddToResourcePolicyResult_d2a345d1:
        """Adds a statement to the IAM resource policy associated with this topic.

        If this topic was created in this stack (``new Topic``), a topic policy
        will be automatically created upon the first call to ``addToPolicy``. If
        the topic is imported (``Topic.import``), then this is a no-op.

        :param statement: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grant topic publishing permissions to the given identity.

        :param grantee: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantPublish", [grantee])

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """Return the given named metric for this Topic.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricNumberOfMessagesPublished")
    def metric_number_of_messages_published(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """The number of messages published to your Amazon SNS topics.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricNumberOfMessagesPublished", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsDelivered")
    def metric_number_of_notifications_delivered(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """The number of messages successfully delivered from your Amazon SNS topics to subscribing endpoints.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricNumberOfNotificationsDelivered", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFailed")
    def metric_number_of_notifications_failed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """The number of messages that Amazon SNS failed to deliver.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricNumberOfNotificationsFailed", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOut")
    def metric_number_of_notifications_filtered_out(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """The number of messages that were rejected by subscription filter policies.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricNumberOfNotificationsFilteredOut", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutInvalidAttributes")
    def metric_number_of_notifications_filtered_out_invalid_attributes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """The number of messages that were rejected by subscription filter policies because the messages' attributes are invalid.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricNumberOfNotificationsFilteredOutInvalidAttributes", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutNoMessageAttributes")
    def metric_number_of_notifications_filtered_out_no_message_attributes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """The number of messages that were rejected by subscription filter policies because the messages have no attributes.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricNumberOfNotificationsFilteredOutNoMessageAttributes", [props])

    @jsii.member(jsii_name="metricPublishSize")
    def metric_publish_size(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """Metric for the size of messages published through this topic.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricPublishSize", [props])

    @jsii.member(jsii_name="metricSMSMonthToDateSpentUSD")
    def metric_sms_month_to_date_spent_usd(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """The charges you have accrued since the start of the current calendar month for sending SMS messages.

        Maximum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricSMSMonthToDateSpentUSD", [props])

    @jsii.member(jsii_name="metricSMSSuccessRate")
    def metric_sms_success_rate(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """The rate of successful SMS message deliveries.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricSMSSuccessRate", [props])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="autoCreatePolicy")
    @abc.abstractmethod
    def _auto_create_policy(self) -> builtins.bool:
        """Controls automatic creation of policy objects.

        Set by subclasses.

        stability
        :stability: experimental
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="topicArn")
    @abc.abstractmethod
    def topic_arn(self) -> builtins.str:
        """The ARN of the topic.

        stability
        :stability: experimental
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="topicName")
    @abc.abstractmethod
    def topic_name(self) -> builtins.str:
        """The name of the topic.

        stability
        :stability: experimental
        """
        ...


class _TopicBaseProxy(
    TopicBase, jsii.proxy_for(_Resource_884d0774) # type: ignore
):
    @builtins.property # type: ignore
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> builtins.bool:
        """Controls automatic creation of policy objects.

        Set by subclasses.

        stability
        :stability: experimental
        """
        return jsii.get(self, "autoCreatePolicy")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> builtins.str:
        """The ARN of the topic.

        stability
        :stability: experimental
        """
        return jsii.get(self, "topicArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> builtins.str:
        """The name of the topic.

        stability
        :stability: experimental
        """
        return jsii.get(self, "topicName")


class TopicPolicy(
    _Resource_884d0774,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_sns.TopicPolicy",
):
    """Applies a policy to SNS topics.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        *,
        topics: typing.List["ITopic"],
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param topics: The set of topics this policy applies to.

        stability
        :stability: experimental
        """
        props = TopicPolicyProps(topics=topics)

        jsii.create(TopicPolicy, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="document")
    def document(self) -> _PolicyDocument_1d1bca11:
        """The IAM policy document for this policy.

        stability
        :stability: experimental
        """
        return jsii.get(self, "document")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_sns.TopicPolicyProps",
    jsii_struct_bases=[],
    name_mapping={"topics": "topics"},
)
class TopicPolicyProps:
    def __init__(self, *, topics: typing.List["ITopic"]) -> None:
        """Properties to associate SNS topics with a policy.

        :param topics: The set of topics this policy applies to.

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "topics": topics,
        }

    @builtins.property
    def topics(self) -> typing.List["ITopic"]:
        """The set of topics this policy applies to.

        stability
        :stability: experimental
        """
        result = self._values.get("topics")
        assert result is not None, "Required property 'topics' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TopicPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_sns.TopicProps",
    jsii_struct_bases=[],
    name_mapping={
        "display_name": "displayName",
        "master_key": "masterKey",
        "topic_name": "topicName",
    },
)
class TopicProps:
    def __init__(
        self,
        *,
        display_name: typing.Optional[builtins.str] = None,
        master_key: typing.Optional[_IKey_3336c79d] = None,
        topic_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for a new SNS topic.

        :param display_name: A developer-defined string that can be used to identify this SNS topic. Default: None
        :param master_key: A KMS Key, either managed by this CDK app, or imported. Default: None
        :param topic_name: A name for the topic. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the topic name. For more information, see Name Type. Default: Generated name

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if display_name is not None:
            self._values["display_name"] = display_name
        if master_key is not None:
            self._values["master_key"] = master_key
        if topic_name is not None:
            self._values["topic_name"] = topic_name

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        """A developer-defined string that can be used to identify this SNS topic.

        default
        :default: None

        stability
        :stability: experimental
        """
        result = self._values.get("display_name")
        return result

    @builtins.property
    def master_key(self) -> typing.Optional[_IKey_3336c79d]:
        """A KMS Key, either managed by this CDK app, or imported.

        default
        :default: None

        stability
        :stability: experimental
        """
        result = self._values.get("master_key")
        return result

    @builtins.property
    def topic_name(self) -> typing.Optional[builtins.str]:
        """A name for the topic.

        If you don't specify a name, AWS CloudFormation generates a unique
        physical ID and uses that ID for the topic name. For more information,
        see Name Type.

        default
        :default: Generated name

        stability
        :stability: experimental
        """
        result = self._values.get("topic_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TopicProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_sns.TopicSubscriptionConfig",
    jsii_struct_bases=[SubscriptionOptions],
    name_mapping={
        "endpoint": "endpoint",
        "protocol": "protocol",
        "dead_letter_queue": "deadLetterQueue",
        "filter_policy": "filterPolicy",
        "raw_message_delivery": "rawMessageDelivery",
        "region": "region",
        "subscriber_id": "subscriberId",
        "subscriber_scope": "subscriberScope",
    },
)
class TopicSubscriptionConfig(SubscriptionOptions):
    def __init__(
        self,
        *,
        endpoint: builtins.str,
        protocol: "SubscriptionProtocol",
        dead_letter_queue: typing.Optional[_IQueue_b743f559] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, "SubscriptionFilter"]] = None,
        raw_message_delivery: typing.Optional[builtins.bool] = None,
        region: typing.Optional[builtins.str] = None,
        subscriber_id: builtins.str,
        subscriber_scope: typing.Optional[_Construct_f50a3f53] = None,
    ) -> None:
        """Subscription configuration.

        :param endpoint: The subscription endpoint. The meaning of this value depends on the value for 'protocol'.
        :param protocol: What type of subscription to add.
        :param dead_letter_queue: Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: The filter policy. Default: - all messages are delivered
        :param raw_message_delivery: true if raw message delivery is enabled for the subscription. Raw messages are free of JSON formatting and can be sent to HTTP/S and Amazon SQS endpoints. For more information, see GetSubscriptionAttributes in the Amazon Simple Notification Service API Reference. Default: false
        :param region: The region where the topic resides, in the case of cross-region subscriptions. Default: - the region where the CloudFormation stack is being deployed.
        :param subscriber_id: The id of the SNS subscription resource created under ``scope``. In most cases, it is recommended to use the ``uniqueId`` of the topic you are subscribing to.
        :param subscriber_scope: The scope in which to create the SNS subscription resource. Normally you'd want the subscription to be created on the consuming stack because the topic is usually referenced by the consumer's resource policy (e.g. SQS queue policy). Otherwise, it will cause a cyclic reference. If this is undefined, the subscription will be created on the topic's stack. Default: - use the topic as the scope of the subscription, in which case ``subscriberId`` must be defined.

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "endpoint": endpoint,
            "protocol": protocol,
            "subscriber_id": subscriber_id,
        }
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None:
            self._values["filter_policy"] = filter_policy
        if raw_message_delivery is not None:
            self._values["raw_message_delivery"] = raw_message_delivery
        if region is not None:
            self._values["region"] = region
        if subscriber_scope is not None:
            self._values["subscriber_scope"] = subscriber_scope

    @builtins.property
    def endpoint(self) -> builtins.str:
        """The subscription endpoint.

        The meaning of this value depends on the value for 'protocol'.

        stability
        :stability: experimental
        """
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return result

    @builtins.property
    def protocol(self) -> "SubscriptionProtocol":
        """What type of subscription to add.

        stability
        :stability: experimental
        """
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return result

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_b743f559]:
        """Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        default
        :default: - No dead letter queue enabled.

        stability
        :stability: experimental
        """
        result = self._values.get("dead_letter_queue")
        return result

    @builtins.property
    def filter_policy(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "SubscriptionFilter"]]:
        """The filter policy.

        default
        :default: - all messages are delivered

        stability
        :stability: experimental
        """
        result = self._values.get("filter_policy")
        return result

    @builtins.property
    def raw_message_delivery(self) -> typing.Optional[builtins.bool]:
        """true if raw message delivery is enabled for the subscription.

        Raw messages are free of JSON formatting and can be
        sent to HTTP/S and Amazon SQS endpoints. For more information, see GetSubscriptionAttributes in the Amazon Simple
        Notification Service API Reference.

        default
        :default: false

        stability
        :stability: experimental
        """
        result = self._values.get("raw_message_delivery")
        return result

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        """The region where the topic resides, in the case of cross-region subscriptions.

        default
        :default: - the region where the CloudFormation stack is being deployed.

        stability
        :stability: experimental
        link:
        :link:: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-region
        """
        result = self._values.get("region")
        return result

    @builtins.property
    def subscriber_id(self) -> builtins.str:
        """The id of the SNS subscription resource created under ``scope``.

        In most
        cases, it is recommended to use the ``uniqueId`` of the topic you are
        subscribing to.

        stability
        :stability: experimental
        """
        result = self._values.get("subscriber_id")
        assert result is not None, "Required property 'subscriber_id' is missing"
        return result

    @builtins.property
    def subscriber_scope(self) -> typing.Optional[_Construct_f50a3f53]:
        """The scope in which to create the SNS subscription resource.

        Normally you'd
        want the subscription to be created on the consuming stack because the
        topic is usually referenced by the consumer's resource policy (e.g. SQS
        queue policy). Otherwise, it will cause a cyclic reference.

        If this is undefined, the subscription will be created on the topic's stack.

        default
        :default: - use the topic as the scope of the subscription, in which case ``subscriberId`` must be defined.

        stability
        :stability: experimental
        """
        result = self._values.get("subscriber_scope")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TopicSubscriptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Topic(
    TopicBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_sns.Topic",
):
    """A new SNS topic.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        *,
        display_name: typing.Optional[builtins.str] = None,
        master_key: typing.Optional[_IKey_3336c79d] = None,
        topic_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param display_name: A developer-defined string that can be used to identify this SNS topic. Default: None
        :param master_key: A KMS Key, either managed by this CDK app, or imported. Default: None
        :param topic_name: A name for the topic. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the topic name. For more information, see Name Type. Default: Generated name

        stability
        :stability: experimental
        """
        props = TopicProps(
            display_name=display_name, master_key=master_key, topic_name=topic_name
        )

        jsii.create(Topic, self, [scope, id, props])

    @jsii.member(jsii_name="fromTopicArn")
    @builtins.classmethod
    def from_topic_arn(
        cls,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        topic_arn: builtins.str,
    ) -> "ITopic":
        """Import an existing SNS topic provided an ARN.

        :param scope: The parent creating construct.
        :param id: The construct's name.
        :param topic_arn: topic ARN (i.e. arn:aws:sns:us-east-2:444455556666:MyTopic).

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromTopicArn", [scope, id, topic_arn])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> builtins.bool:
        """Controls automatic creation of policy objects.

        Set by subclasses.

        stability
        :stability: experimental
        """
        return jsii.get(self, "autoCreatePolicy")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> builtins.str:
        """The ARN of the topic.

        stability
        :stability: experimental
        """
        return jsii.get(self, "topicArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> builtins.str:
        """The name of the topic.

        stability
        :stability: experimental
        """
        return jsii.get(self, "topicName")


__all__ = [
    "BetweenCondition",
    "CfnSubscription",
    "CfnSubscriptionProps",
    "CfnTopic",
    "CfnTopicPolicy",
    "CfnTopicPolicyProps",
    "CfnTopicProps",
    "ITopic",
    "ITopicSubscription",
    "NumericConditions",
    "StringConditions",
    "Subscription",
    "SubscriptionFilter",
    "SubscriptionOptions",
    "SubscriptionProps",
    "SubscriptionProtocol",
    "Topic",
    "TopicBase",
    "TopicPolicy",
    "TopicPolicyProps",
    "TopicProps",
    "TopicSubscriptionConfig",
]

publication.publish()
