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
    IInspectable as _IInspectable_051e6ed8,
    IResolvable as _IResolvable_9ceae33e,
    TagManager as _TagManager_2508893f,
    TreeInspector as _TreeInspector_154f5999,
)


@jsii.implements(_IInspectable_051e6ed8)
class CfnDomain(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_elasticsearch.CfnDomain",
):
    """A CloudFormation ``AWS::Elasticsearch::Domain``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html
    cloudformationResource:
    :cloudformationResource:: AWS::Elasticsearch::Domain
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        *,
        access_policies: typing.Any = None,
        advanced_options: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[builtins.str, builtins.str]]] = None,
        advanced_security_options: typing.Optional[typing.Union["AdvancedSecurityOptionsInputProperty", _IResolvable_9ceae33e]] = None,
        cognito_options: typing.Optional[typing.Union["CognitoOptionsProperty", _IResolvable_9ceae33e]] = None,
        domain_endpoint_options: typing.Optional[typing.Union["DomainEndpointOptionsProperty", _IResolvable_9ceae33e]] = None,
        domain_name: typing.Optional[builtins.str] = None,
        ebs_options: typing.Optional[typing.Union["EBSOptionsProperty", _IResolvable_9ceae33e]] = None,
        elasticsearch_cluster_config: typing.Optional[typing.Union["ElasticsearchClusterConfigProperty", _IResolvable_9ceae33e]] = None,
        elasticsearch_version: typing.Optional[builtins.str] = None,
        encryption_at_rest_options: typing.Optional[typing.Union["EncryptionAtRestOptionsProperty", _IResolvable_9ceae33e]] = None,
        log_publishing_options: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[builtins.str, typing.Union["LogPublishingOptionProperty", _IResolvable_9ceae33e]]]] = None,
        node_to_node_encryption_options: typing.Optional[typing.Union["NodeToNodeEncryptionOptionsProperty", _IResolvable_9ceae33e]] = None,
        snapshot_options: typing.Optional[typing.Union["SnapshotOptionsProperty", _IResolvable_9ceae33e]] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
        vpc_options: typing.Optional[typing.Union["VPCOptionsProperty", _IResolvable_9ceae33e]] = None,
    ) -> None:
        """Create a new ``AWS::Elasticsearch::Domain``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param access_policies: ``AWS::Elasticsearch::Domain.AccessPolicies``.
        :param advanced_options: ``AWS::Elasticsearch::Domain.AdvancedOptions``.
        :param advanced_security_options: ``AWS::Elasticsearch::Domain.AdvancedSecurityOptions``.
        :param cognito_options: ``AWS::Elasticsearch::Domain.CognitoOptions``.
        :param domain_endpoint_options: ``AWS::Elasticsearch::Domain.DomainEndpointOptions``.
        :param domain_name: ``AWS::Elasticsearch::Domain.DomainName``.
        :param ebs_options: ``AWS::Elasticsearch::Domain.EBSOptions``.
        :param elasticsearch_cluster_config: ``AWS::Elasticsearch::Domain.ElasticsearchClusterConfig``.
        :param elasticsearch_version: ``AWS::Elasticsearch::Domain.ElasticsearchVersion``.
        :param encryption_at_rest_options: ``AWS::Elasticsearch::Domain.EncryptionAtRestOptions``.
        :param log_publishing_options: ``AWS::Elasticsearch::Domain.LogPublishingOptions``.
        :param node_to_node_encryption_options: ``AWS::Elasticsearch::Domain.NodeToNodeEncryptionOptions``.
        :param snapshot_options: ``AWS::Elasticsearch::Domain.SnapshotOptions``.
        :param tags: ``AWS::Elasticsearch::Domain.Tags``.
        :param vpc_options: ``AWS::Elasticsearch::Domain.VPCOptions``.
        """
        props = CfnDomainProps(
            access_policies=access_policies,
            advanced_options=advanced_options,
            advanced_security_options=advanced_security_options,
            cognito_options=cognito_options,
            domain_endpoint_options=domain_endpoint_options,
            domain_name=domain_name,
            ebs_options=ebs_options,
            elasticsearch_cluster_config=elasticsearch_cluster_config,
            elasticsearch_version=elasticsearch_version,
            encryption_at_rest_options=encryption_at_rest_options,
            log_publishing_options=log_publishing_options,
            node_to_node_encryption_options=node_to_node_encryption_options,
            snapshot_options=snapshot_options,
            tags=tags,
            vpc_options=vpc_options,
        )

        jsii.create(CfnDomain, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrDomainEndpoint")
    def attr_domain_endpoint(self) -> builtins.str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: DomainEndpoint
        """
        return jsii.get(self, "attrDomainEndpoint")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::Elasticsearch::Domain.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="accessPolicies")
    def access_policies(self) -> typing.Any:
        """``AWS::Elasticsearch::Domain.AccessPolicies``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-accesspolicies
        """
        return jsii.get(self, "accessPolicies")

    @access_policies.setter # type: ignore
    def access_policies(self, value: typing.Any) -> None:
        jsii.set(self, "accessPolicies", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="advancedOptions")
    def advanced_options(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[builtins.str, builtins.str]]]:
        """``AWS::Elasticsearch::Domain.AdvancedOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-advancedoptions
        """
        return jsii.get(self, "advancedOptions")

    @advanced_options.setter # type: ignore
    def advanced_options(
        self,
        value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        jsii.set(self, "advancedOptions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="advancedSecurityOptions")
    def advanced_security_options(
        self,
    ) -> typing.Optional[typing.Union["AdvancedSecurityOptionsInputProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.AdvancedSecurityOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-advancedsecurityoptions
        """
        return jsii.get(self, "advancedSecurityOptions")

    @advanced_security_options.setter # type: ignore
    def advanced_security_options(
        self,
        value: typing.Optional[typing.Union["AdvancedSecurityOptionsInputProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "advancedSecurityOptions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cognitoOptions")
    def cognito_options(
        self,
    ) -> typing.Optional[typing.Union["CognitoOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.CognitoOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-cognitooptions
        """
        return jsii.get(self, "cognitoOptions")

    @cognito_options.setter # type: ignore
    def cognito_options(
        self,
        value: typing.Optional[typing.Union["CognitoOptionsProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "cognitoOptions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="domainEndpointOptions")
    def domain_endpoint_options(
        self,
    ) -> typing.Optional[typing.Union["DomainEndpointOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.DomainEndpointOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-domainendpointoptions
        """
        return jsii.get(self, "domainEndpointOptions")

    @domain_endpoint_options.setter # type: ignore
    def domain_endpoint_options(
        self,
        value: typing.Optional[typing.Union["DomainEndpointOptionsProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "domainEndpointOptions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Elasticsearch::Domain.DomainName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-domainname
        """
        return jsii.get(self, "domainName")

    @domain_name.setter # type: ignore
    def domain_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "domainName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ebsOptions")
    def ebs_options(
        self,
    ) -> typing.Optional[typing.Union["EBSOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.EBSOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-ebsoptions
        """
        return jsii.get(self, "ebsOptions")

    @ebs_options.setter # type: ignore
    def ebs_options(
        self,
        value: typing.Optional[typing.Union["EBSOptionsProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "ebsOptions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="elasticsearchClusterConfig")
    def elasticsearch_cluster_config(
        self,
    ) -> typing.Optional[typing.Union["ElasticsearchClusterConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.ElasticsearchClusterConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-elasticsearchclusterconfig
        """
        return jsii.get(self, "elasticsearchClusterConfig")

    @elasticsearch_cluster_config.setter # type: ignore
    def elasticsearch_cluster_config(
        self,
        value: typing.Optional[typing.Union["ElasticsearchClusterConfigProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "elasticsearchClusterConfig", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="elasticsearchVersion")
    def elasticsearch_version(self) -> typing.Optional[builtins.str]:
        """``AWS::Elasticsearch::Domain.ElasticsearchVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-elasticsearchversion
        """
        return jsii.get(self, "elasticsearchVersion")

    @elasticsearch_version.setter # type: ignore
    def elasticsearch_version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "elasticsearchVersion", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="encryptionAtRestOptions")
    def encryption_at_rest_options(
        self,
    ) -> typing.Optional[typing.Union["EncryptionAtRestOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.EncryptionAtRestOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-encryptionatrestoptions
        """
        return jsii.get(self, "encryptionAtRestOptions")

    @encryption_at_rest_options.setter # type: ignore
    def encryption_at_rest_options(
        self,
        value: typing.Optional[typing.Union["EncryptionAtRestOptionsProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "encryptionAtRestOptions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="logPublishingOptions")
    def log_publishing_options(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[builtins.str, typing.Union["LogPublishingOptionProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::Elasticsearch::Domain.LogPublishingOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-logpublishingoptions
        """
        return jsii.get(self, "logPublishingOptions")

    @log_publishing_options.setter # type: ignore
    def log_publishing_options(
        self,
        value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[builtins.str, typing.Union["LogPublishingOptionProperty", _IResolvable_9ceae33e]]]],
    ) -> None:
        jsii.set(self, "logPublishingOptions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="nodeToNodeEncryptionOptions")
    def node_to_node_encryption_options(
        self,
    ) -> typing.Optional[typing.Union["NodeToNodeEncryptionOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.NodeToNodeEncryptionOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-nodetonodeencryptionoptions
        """
        return jsii.get(self, "nodeToNodeEncryptionOptions")

    @node_to_node_encryption_options.setter # type: ignore
    def node_to_node_encryption_options(
        self,
        value: typing.Optional[typing.Union["NodeToNodeEncryptionOptionsProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "nodeToNodeEncryptionOptions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="snapshotOptions")
    def snapshot_options(
        self,
    ) -> typing.Optional[typing.Union["SnapshotOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.SnapshotOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-snapshotoptions
        """
        return jsii.get(self, "snapshotOptions")

    @snapshot_options.setter # type: ignore
    def snapshot_options(
        self,
        value: typing.Optional[typing.Union["SnapshotOptionsProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "snapshotOptions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpcOptions")
    def vpc_options(
        self,
    ) -> typing.Optional[typing.Union["VPCOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.VPCOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-vpcoptions
        """
        return jsii.get(self, "vpcOptions")

    @vpc_options.setter # type: ignore
    def vpc_options(
        self,
        value: typing.Optional[typing.Union["VPCOptionsProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "vpcOptions", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_elasticsearch.CfnDomain.AdvancedSecurityOptionsInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "internal_user_database_enabled": "internalUserDatabaseEnabled",
            "master_user_options": "masterUserOptions",
        },
    )
    class AdvancedSecurityOptionsInputProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
            internal_user_database_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
            master_user_options: typing.Optional[typing.Union["CfnDomain.MasterUserOptionsProperty", _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param enabled: ``CfnDomain.AdvancedSecurityOptionsInputProperty.Enabled``.
            :param internal_user_database_enabled: ``CfnDomain.AdvancedSecurityOptionsInputProperty.InternalUserDatabaseEnabled``.
            :param master_user_options: ``CfnDomain.AdvancedSecurityOptionsInputProperty.MasterUserOptions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-advancedsecurityoptionsinput.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if internal_user_database_enabled is not None:
                self._values["internal_user_database_enabled"] = internal_user_database_enabled
            if master_user_options is not None:
                self._values["master_user_options"] = master_user_options

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
            """``CfnDomain.AdvancedSecurityOptionsInputProperty.Enabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-advancedsecurityoptionsinput.html#cfn-elasticsearch-domain-advancedsecurityoptionsinput-enabled
            """
            result = self._values.get("enabled")
            return result

        @builtins.property
        def internal_user_database_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
            """``CfnDomain.AdvancedSecurityOptionsInputProperty.InternalUserDatabaseEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-advancedsecurityoptionsinput.html#cfn-elasticsearch-domain-advancedsecurityoptionsinput-internaluserdatabaseenabled
            """
            result = self._values.get("internal_user_database_enabled")
            return result

        @builtins.property
        def master_user_options(
            self,
        ) -> typing.Optional[typing.Union["CfnDomain.MasterUserOptionsProperty", _IResolvable_9ceae33e]]:
            """``CfnDomain.AdvancedSecurityOptionsInputProperty.MasterUserOptions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-advancedsecurityoptionsinput.html#cfn-elasticsearch-domain-advancedsecurityoptionsinput-masteruseroptions
            """
            result = self._values.get("master_user_options")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdvancedSecurityOptionsInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_elasticsearch.CfnDomain.CognitoOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "identity_pool_id": "identityPoolId",
            "role_arn": "roleArn",
            "user_pool_id": "userPoolId",
        },
    )
    class CognitoOptionsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
            identity_pool_id: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            user_pool_id: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param enabled: ``CfnDomain.CognitoOptionsProperty.Enabled``.
            :param identity_pool_id: ``CfnDomain.CognitoOptionsProperty.IdentityPoolId``.
            :param role_arn: ``CfnDomain.CognitoOptionsProperty.RoleArn``.
            :param user_pool_id: ``CfnDomain.CognitoOptionsProperty.UserPoolId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-cognitooptions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if identity_pool_id is not None:
                self._values["identity_pool_id"] = identity_pool_id
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if user_pool_id is not None:
                self._values["user_pool_id"] = user_pool_id

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
            """``CfnDomain.CognitoOptionsProperty.Enabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-cognitooptions.html#cfn-elasticsearch-domain-cognitooptions-enabled
            """
            result = self._values.get("enabled")
            return result

        @builtins.property
        def identity_pool_id(self) -> typing.Optional[builtins.str]:
            """``CfnDomain.CognitoOptionsProperty.IdentityPoolId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-cognitooptions.html#cfn-elasticsearch-domain-cognitooptions-identitypoolid
            """
            result = self._values.get("identity_pool_id")
            return result

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            """``CfnDomain.CognitoOptionsProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-cognitooptions.html#cfn-elasticsearch-domain-cognitooptions-rolearn
            """
            result = self._values.get("role_arn")
            return result

        @builtins.property
        def user_pool_id(self) -> typing.Optional[builtins.str]:
            """``CfnDomain.CognitoOptionsProperty.UserPoolId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-cognitooptions.html#cfn-elasticsearch-domain-cognitooptions-userpoolid
            """
            result = self._values.get("user_pool_id")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CognitoOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_elasticsearch.CfnDomain.DomainEndpointOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enforce_https": "enforceHttps",
            "tls_security_policy": "tlsSecurityPolicy",
        },
    )
    class DomainEndpointOptionsProperty:
        def __init__(
            self,
            *,
            enforce_https: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
            tls_security_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param enforce_https: ``CfnDomain.DomainEndpointOptionsProperty.EnforceHTTPS``.
            :param tls_security_policy: ``CfnDomain.DomainEndpointOptionsProperty.TLSSecurityPolicy``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-domainendpointoptions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if enforce_https is not None:
                self._values["enforce_https"] = enforce_https
            if tls_security_policy is not None:
                self._values["tls_security_policy"] = tls_security_policy

        @builtins.property
        def enforce_https(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
            """``CfnDomain.DomainEndpointOptionsProperty.EnforceHTTPS``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-domainendpointoptions.html#cfn-elasticsearch-domain-domainendpointoptions-enforcehttps
            """
            result = self._values.get("enforce_https")
            return result

        @builtins.property
        def tls_security_policy(self) -> typing.Optional[builtins.str]:
            """``CfnDomain.DomainEndpointOptionsProperty.TLSSecurityPolicy``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-domainendpointoptions.html#cfn-elasticsearch-domain-domainendpointoptions-tlssecuritypolicy
            """
            result = self._values.get("tls_security_policy")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainEndpointOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_elasticsearch.CfnDomain.EBSOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ebs_enabled": "ebsEnabled",
            "iops": "iops",
            "volume_size": "volumeSize",
            "volume_type": "volumeType",
        },
    )
    class EBSOptionsProperty:
        def __init__(
            self,
            *,
            ebs_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
            iops: typing.Optional[jsii.Number] = None,
            volume_size: typing.Optional[jsii.Number] = None,
            volume_type: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param ebs_enabled: ``CfnDomain.EBSOptionsProperty.EBSEnabled``.
            :param iops: ``CfnDomain.EBSOptionsProperty.Iops``.
            :param volume_size: ``CfnDomain.EBSOptionsProperty.VolumeSize``.
            :param volume_type: ``CfnDomain.EBSOptionsProperty.VolumeType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-ebsoptions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if ebs_enabled is not None:
                self._values["ebs_enabled"] = ebs_enabled
            if iops is not None:
                self._values["iops"] = iops
            if volume_size is not None:
                self._values["volume_size"] = volume_size
            if volume_type is not None:
                self._values["volume_type"] = volume_type

        @builtins.property
        def ebs_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
            """``CfnDomain.EBSOptionsProperty.EBSEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-ebsoptions.html#cfn-elasticsearch-domain-ebsoptions-ebsenabled
            """
            result = self._values.get("ebs_enabled")
            return result

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            """``CfnDomain.EBSOptionsProperty.Iops``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-ebsoptions.html#cfn-elasticsearch-domain-ebsoptions-iops
            """
            result = self._values.get("iops")
            return result

        @builtins.property
        def volume_size(self) -> typing.Optional[jsii.Number]:
            """``CfnDomain.EBSOptionsProperty.VolumeSize``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-ebsoptions.html#cfn-elasticsearch-domain-ebsoptions-volumesize
            """
            result = self._values.get("volume_size")
            return result

        @builtins.property
        def volume_type(self) -> typing.Optional[builtins.str]:
            """``CfnDomain.EBSOptionsProperty.VolumeType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-ebsoptions.html#cfn-elasticsearch-domain-ebsoptions-volumetype
            """
            result = self._values.get("volume_type")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EBSOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_elasticsearch.CfnDomain.ElasticsearchClusterConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dedicated_master_count": "dedicatedMasterCount",
            "dedicated_master_enabled": "dedicatedMasterEnabled",
            "dedicated_master_type": "dedicatedMasterType",
            "instance_count": "instanceCount",
            "instance_type": "instanceType",
            "zone_awareness_config": "zoneAwarenessConfig",
            "zone_awareness_enabled": "zoneAwarenessEnabled",
        },
    )
    class ElasticsearchClusterConfigProperty:
        def __init__(
            self,
            *,
            dedicated_master_count: typing.Optional[jsii.Number] = None,
            dedicated_master_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
            dedicated_master_type: typing.Optional[builtins.str] = None,
            instance_count: typing.Optional[jsii.Number] = None,
            instance_type: typing.Optional[builtins.str] = None,
            zone_awareness_config: typing.Optional[typing.Union["CfnDomain.ZoneAwarenessConfigProperty", _IResolvable_9ceae33e]] = None,
            zone_awareness_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param dedicated_master_count: ``CfnDomain.ElasticsearchClusterConfigProperty.DedicatedMasterCount``.
            :param dedicated_master_enabled: ``CfnDomain.ElasticsearchClusterConfigProperty.DedicatedMasterEnabled``.
            :param dedicated_master_type: ``CfnDomain.ElasticsearchClusterConfigProperty.DedicatedMasterType``.
            :param instance_count: ``CfnDomain.ElasticsearchClusterConfigProperty.InstanceCount``.
            :param instance_type: ``CfnDomain.ElasticsearchClusterConfigProperty.InstanceType``.
            :param zone_awareness_config: ``CfnDomain.ElasticsearchClusterConfigProperty.ZoneAwarenessConfig``.
            :param zone_awareness_enabled: ``CfnDomain.ElasticsearchClusterConfigProperty.ZoneAwarenessEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if dedicated_master_count is not None:
                self._values["dedicated_master_count"] = dedicated_master_count
            if dedicated_master_enabled is not None:
                self._values["dedicated_master_enabled"] = dedicated_master_enabled
            if dedicated_master_type is not None:
                self._values["dedicated_master_type"] = dedicated_master_type
            if instance_count is not None:
                self._values["instance_count"] = instance_count
            if instance_type is not None:
                self._values["instance_type"] = instance_type
            if zone_awareness_config is not None:
                self._values["zone_awareness_config"] = zone_awareness_config
            if zone_awareness_enabled is not None:
                self._values["zone_awareness_enabled"] = zone_awareness_enabled

        @builtins.property
        def dedicated_master_count(self) -> typing.Optional[jsii.Number]:
            """``CfnDomain.ElasticsearchClusterConfigProperty.DedicatedMasterCount``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticseachclusterconfig-dedicatedmastercount
            """
            result = self._values.get("dedicated_master_count")
            return result

        @builtins.property
        def dedicated_master_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
            """``CfnDomain.ElasticsearchClusterConfigProperty.DedicatedMasterEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticseachclusterconfig-dedicatedmasterenabled
            """
            result = self._values.get("dedicated_master_enabled")
            return result

        @builtins.property
        def dedicated_master_type(self) -> typing.Optional[builtins.str]:
            """``CfnDomain.ElasticsearchClusterConfigProperty.DedicatedMasterType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticseachclusterconfig-dedicatedmastertype
            """
            result = self._values.get("dedicated_master_type")
            return result

        @builtins.property
        def instance_count(self) -> typing.Optional[jsii.Number]:
            """``CfnDomain.ElasticsearchClusterConfigProperty.InstanceCount``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticseachclusterconfig-instancecount
            """
            result = self._values.get("instance_count")
            return result

        @builtins.property
        def instance_type(self) -> typing.Optional[builtins.str]:
            """``CfnDomain.ElasticsearchClusterConfigProperty.InstanceType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticseachclusterconfig-instnacetype
            """
            result = self._values.get("instance_type")
            return result

        @builtins.property
        def zone_awareness_config(
            self,
        ) -> typing.Optional[typing.Union["CfnDomain.ZoneAwarenessConfigProperty", _IResolvable_9ceae33e]]:
            """``CfnDomain.ElasticsearchClusterConfigProperty.ZoneAwarenessConfig``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticsearchclusterconfig-zoneawarenessconfig
            """
            result = self._values.get("zone_awareness_config")
            return result

        @builtins.property
        def zone_awareness_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
            """``CfnDomain.ElasticsearchClusterConfigProperty.ZoneAwarenessEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticseachclusterconfig-zoneawarenessenabled
            """
            result = self._values.get("zone_awareness_enabled")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ElasticsearchClusterConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_elasticsearch.CfnDomain.EncryptionAtRestOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "kms_key_id": "kmsKeyId"},
    )
    class EncryptionAtRestOptionsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
            kms_key_id: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param enabled: ``CfnDomain.EncryptionAtRestOptionsProperty.Enabled``.
            :param kms_key_id: ``CfnDomain.EncryptionAtRestOptionsProperty.KmsKeyId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-encryptionatrestoptions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
            """``CfnDomain.EncryptionAtRestOptionsProperty.Enabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-encryptionatrestoptions.html#cfn-elasticsearch-domain-encryptionatrestoptions-enabled
            """
            result = self._values.get("enabled")
            return result

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            """``CfnDomain.EncryptionAtRestOptionsProperty.KmsKeyId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-encryptionatrestoptions.html#cfn-elasticsearch-domain-encryptionatrestoptions-kmskeyid
            """
            result = self._values.get("kms_key_id")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionAtRestOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_elasticsearch.CfnDomain.LogPublishingOptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_logs_log_group_arn": "cloudWatchLogsLogGroupArn",
            "enabled": "enabled",
        },
    )
    class LogPublishingOptionProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs_log_group_arn: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param cloud_watch_logs_log_group_arn: ``CfnDomain.LogPublishingOptionProperty.CloudWatchLogsLogGroupArn``.
            :param enabled: ``CfnDomain.LogPublishingOptionProperty.Enabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-logpublishingoption.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if cloud_watch_logs_log_group_arn is not None:
                self._values["cloud_watch_logs_log_group_arn"] = cloud_watch_logs_log_group_arn
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def cloud_watch_logs_log_group_arn(self) -> typing.Optional[builtins.str]:
            """``CfnDomain.LogPublishingOptionProperty.CloudWatchLogsLogGroupArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-logpublishingoption.html#cfn-elasticsearch-domain-logpublishingoption-cloudwatchlogsloggrouparn
            """
            result = self._values.get("cloud_watch_logs_log_group_arn")
            return result

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
            """``CfnDomain.LogPublishingOptionProperty.Enabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-logpublishingoption.html#cfn-elasticsearch-domain-logpublishingoption-enabled
            """
            result = self._values.get("enabled")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogPublishingOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_elasticsearch.CfnDomain.MasterUserOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "master_user_arn": "masterUserArn",
            "master_user_name": "masterUserName",
            "master_user_password": "masterUserPassword",
        },
    )
    class MasterUserOptionsProperty:
        def __init__(
            self,
            *,
            master_user_arn: typing.Optional[builtins.str] = None,
            master_user_name: typing.Optional[builtins.str] = None,
            master_user_password: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param master_user_arn: ``CfnDomain.MasterUserOptionsProperty.MasterUserARN``.
            :param master_user_name: ``CfnDomain.MasterUserOptionsProperty.MasterUserName``.
            :param master_user_password: ``CfnDomain.MasterUserOptionsProperty.MasterUserPassword``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-masteruseroptions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if master_user_arn is not None:
                self._values["master_user_arn"] = master_user_arn
            if master_user_name is not None:
                self._values["master_user_name"] = master_user_name
            if master_user_password is not None:
                self._values["master_user_password"] = master_user_password

        @builtins.property
        def master_user_arn(self) -> typing.Optional[builtins.str]:
            """``CfnDomain.MasterUserOptionsProperty.MasterUserARN``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-masteruseroptions.html#cfn-elasticsearch-domain-masteruseroptions-masteruserarn
            """
            result = self._values.get("master_user_arn")
            return result

        @builtins.property
        def master_user_name(self) -> typing.Optional[builtins.str]:
            """``CfnDomain.MasterUserOptionsProperty.MasterUserName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-masteruseroptions.html#cfn-elasticsearch-domain-masteruseroptions-masterusername
            """
            result = self._values.get("master_user_name")
            return result

        @builtins.property
        def master_user_password(self) -> typing.Optional[builtins.str]:
            """``CfnDomain.MasterUserOptionsProperty.MasterUserPassword``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-masteruseroptions.html#cfn-elasticsearch-domain-masteruseroptions-masteruserpassword
            """
            result = self._values.get("master_user_password")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MasterUserOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_elasticsearch.CfnDomain.NodeToNodeEncryptionOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class NodeToNodeEncryptionOptionsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param enabled: ``CfnDomain.NodeToNodeEncryptionOptionsProperty.Enabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-nodetonodeencryptionoptions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
            """``CfnDomain.NodeToNodeEncryptionOptionsProperty.Enabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-nodetonodeencryptionoptions.html#cfn-elasticsearch-domain-nodetonodeencryptionoptions-enabled
            """
            result = self._values.get("enabled")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodeToNodeEncryptionOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_elasticsearch.CfnDomain.SnapshotOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"automated_snapshot_start_hour": "automatedSnapshotStartHour"},
    )
    class SnapshotOptionsProperty:
        def __init__(
            self,
            *,
            automated_snapshot_start_hour: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param automated_snapshot_start_hour: ``CfnDomain.SnapshotOptionsProperty.AutomatedSnapshotStartHour``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-snapshotoptions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if automated_snapshot_start_hour is not None:
                self._values["automated_snapshot_start_hour"] = automated_snapshot_start_hour

        @builtins.property
        def automated_snapshot_start_hour(self) -> typing.Optional[jsii.Number]:
            """``CfnDomain.SnapshotOptionsProperty.AutomatedSnapshotStartHour``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-snapshotoptions.html#cfn-elasticsearch-domain-snapshotoptions-automatedsnapshotstarthour
            """
            result = self._values.get("automated_snapshot_start_hour")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnapshotOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_elasticsearch.CfnDomain.VPCOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class VPCOptionsProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.List[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param security_group_ids: ``CfnDomain.VPCOptionsProperty.SecurityGroupIds``.
            :param subnet_ids: ``CfnDomain.VPCOptionsProperty.SubnetIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-vpcoptions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnDomain.VPCOptionsProperty.SecurityGroupIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-vpcoptions.html#cfn-elasticsearch-domain-vpcoptions-securitygroupids
            """
            result = self._values.get("security_group_ids")
            return result

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnDomain.VPCOptionsProperty.SubnetIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-vpcoptions.html#cfn-elasticsearch-domain-vpcoptions-subnetids
            """
            result = self._values.get("subnet_ids")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VPCOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_elasticsearch.CfnDomain.ZoneAwarenessConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"availability_zone_count": "availabilityZoneCount"},
    )
    class ZoneAwarenessConfigProperty:
        def __init__(
            self,
            *,
            availability_zone_count: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param availability_zone_count: ``CfnDomain.ZoneAwarenessConfigProperty.AvailabilityZoneCount``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-zoneawarenessconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if availability_zone_count is not None:
                self._values["availability_zone_count"] = availability_zone_count

        @builtins.property
        def availability_zone_count(self) -> typing.Optional[jsii.Number]:
            """``CfnDomain.ZoneAwarenessConfigProperty.AvailabilityZoneCount``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-zoneawarenessconfig.html#cfn-elasticsearch-domain-zoneawarenessconfig-availabilityzonecount
            """
            result = self._values.get("availability_zone_count")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ZoneAwarenessConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_elasticsearch.CfnDomainProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_policies": "accessPolicies",
        "advanced_options": "advancedOptions",
        "advanced_security_options": "advancedSecurityOptions",
        "cognito_options": "cognitoOptions",
        "domain_endpoint_options": "domainEndpointOptions",
        "domain_name": "domainName",
        "ebs_options": "ebsOptions",
        "elasticsearch_cluster_config": "elasticsearchClusterConfig",
        "elasticsearch_version": "elasticsearchVersion",
        "encryption_at_rest_options": "encryptionAtRestOptions",
        "log_publishing_options": "logPublishingOptions",
        "node_to_node_encryption_options": "nodeToNodeEncryptionOptions",
        "snapshot_options": "snapshotOptions",
        "tags": "tags",
        "vpc_options": "vpcOptions",
    },
)
class CfnDomainProps:
    def __init__(
        self,
        *,
        access_policies: typing.Any = None,
        advanced_options: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[builtins.str, builtins.str]]] = None,
        advanced_security_options: typing.Optional[typing.Union["CfnDomain.AdvancedSecurityOptionsInputProperty", _IResolvable_9ceae33e]] = None,
        cognito_options: typing.Optional[typing.Union["CfnDomain.CognitoOptionsProperty", _IResolvable_9ceae33e]] = None,
        domain_endpoint_options: typing.Optional[typing.Union["CfnDomain.DomainEndpointOptionsProperty", _IResolvable_9ceae33e]] = None,
        domain_name: typing.Optional[builtins.str] = None,
        ebs_options: typing.Optional[typing.Union["CfnDomain.EBSOptionsProperty", _IResolvable_9ceae33e]] = None,
        elasticsearch_cluster_config: typing.Optional[typing.Union["CfnDomain.ElasticsearchClusterConfigProperty", _IResolvable_9ceae33e]] = None,
        elasticsearch_version: typing.Optional[builtins.str] = None,
        encryption_at_rest_options: typing.Optional[typing.Union["CfnDomain.EncryptionAtRestOptionsProperty", _IResolvable_9ceae33e]] = None,
        log_publishing_options: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[builtins.str, typing.Union["CfnDomain.LogPublishingOptionProperty", _IResolvable_9ceae33e]]]] = None,
        node_to_node_encryption_options: typing.Optional[typing.Union["CfnDomain.NodeToNodeEncryptionOptionsProperty", _IResolvable_9ceae33e]] = None,
        snapshot_options: typing.Optional[typing.Union["CfnDomain.SnapshotOptionsProperty", _IResolvable_9ceae33e]] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
        vpc_options: typing.Optional[typing.Union["CfnDomain.VPCOptionsProperty", _IResolvable_9ceae33e]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Elasticsearch::Domain``.

        :param access_policies: ``AWS::Elasticsearch::Domain.AccessPolicies``.
        :param advanced_options: ``AWS::Elasticsearch::Domain.AdvancedOptions``.
        :param advanced_security_options: ``AWS::Elasticsearch::Domain.AdvancedSecurityOptions``.
        :param cognito_options: ``AWS::Elasticsearch::Domain.CognitoOptions``.
        :param domain_endpoint_options: ``AWS::Elasticsearch::Domain.DomainEndpointOptions``.
        :param domain_name: ``AWS::Elasticsearch::Domain.DomainName``.
        :param ebs_options: ``AWS::Elasticsearch::Domain.EBSOptions``.
        :param elasticsearch_cluster_config: ``AWS::Elasticsearch::Domain.ElasticsearchClusterConfig``.
        :param elasticsearch_version: ``AWS::Elasticsearch::Domain.ElasticsearchVersion``.
        :param encryption_at_rest_options: ``AWS::Elasticsearch::Domain.EncryptionAtRestOptions``.
        :param log_publishing_options: ``AWS::Elasticsearch::Domain.LogPublishingOptions``.
        :param node_to_node_encryption_options: ``AWS::Elasticsearch::Domain.NodeToNodeEncryptionOptions``.
        :param snapshot_options: ``AWS::Elasticsearch::Domain.SnapshotOptions``.
        :param tags: ``AWS::Elasticsearch::Domain.Tags``.
        :param vpc_options: ``AWS::Elasticsearch::Domain.VPCOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if access_policies is not None:
            self._values["access_policies"] = access_policies
        if advanced_options is not None:
            self._values["advanced_options"] = advanced_options
        if advanced_security_options is not None:
            self._values["advanced_security_options"] = advanced_security_options
        if cognito_options is not None:
            self._values["cognito_options"] = cognito_options
        if domain_endpoint_options is not None:
            self._values["domain_endpoint_options"] = domain_endpoint_options
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if ebs_options is not None:
            self._values["ebs_options"] = ebs_options
        if elasticsearch_cluster_config is not None:
            self._values["elasticsearch_cluster_config"] = elasticsearch_cluster_config
        if elasticsearch_version is not None:
            self._values["elasticsearch_version"] = elasticsearch_version
        if encryption_at_rest_options is not None:
            self._values["encryption_at_rest_options"] = encryption_at_rest_options
        if log_publishing_options is not None:
            self._values["log_publishing_options"] = log_publishing_options
        if node_to_node_encryption_options is not None:
            self._values["node_to_node_encryption_options"] = node_to_node_encryption_options
        if snapshot_options is not None:
            self._values["snapshot_options"] = snapshot_options
        if tags is not None:
            self._values["tags"] = tags
        if vpc_options is not None:
            self._values["vpc_options"] = vpc_options

    @builtins.property
    def access_policies(self) -> typing.Any:
        """``AWS::Elasticsearch::Domain.AccessPolicies``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-accesspolicies
        """
        result = self._values.get("access_policies")
        return result

    @builtins.property
    def advanced_options(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[builtins.str, builtins.str]]]:
        """``AWS::Elasticsearch::Domain.AdvancedOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-advancedoptions
        """
        result = self._values.get("advanced_options")
        return result

    @builtins.property
    def advanced_security_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.AdvancedSecurityOptionsInputProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.AdvancedSecurityOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-advancedsecurityoptions
        """
        result = self._values.get("advanced_security_options")
        return result

    @builtins.property
    def cognito_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.CognitoOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.CognitoOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-cognitooptions
        """
        result = self._values.get("cognito_options")
        return result

    @builtins.property
    def domain_endpoint_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.DomainEndpointOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.DomainEndpointOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-domainendpointoptions
        """
        result = self._values.get("domain_endpoint_options")
        return result

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Elasticsearch::Domain.DomainName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-domainname
        """
        result = self._values.get("domain_name")
        return result

    @builtins.property
    def ebs_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.EBSOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.EBSOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-ebsoptions
        """
        result = self._values.get("ebs_options")
        return result

    @builtins.property
    def elasticsearch_cluster_config(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.ElasticsearchClusterConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.ElasticsearchClusterConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-elasticsearchclusterconfig
        """
        result = self._values.get("elasticsearch_cluster_config")
        return result

    @builtins.property
    def elasticsearch_version(self) -> typing.Optional[builtins.str]:
        """``AWS::Elasticsearch::Domain.ElasticsearchVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-elasticsearchversion
        """
        result = self._values.get("elasticsearch_version")
        return result

    @builtins.property
    def encryption_at_rest_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.EncryptionAtRestOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.EncryptionAtRestOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-encryptionatrestoptions
        """
        result = self._values.get("encryption_at_rest_options")
        return result

    @builtins.property
    def log_publishing_options(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[builtins.str, typing.Union["CfnDomain.LogPublishingOptionProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::Elasticsearch::Domain.LogPublishingOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-logpublishingoptions
        """
        result = self._values.get("log_publishing_options")
        return result

    @builtins.property
    def node_to_node_encryption_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.NodeToNodeEncryptionOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.NodeToNodeEncryptionOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-nodetonodeencryptionoptions
        """
        result = self._values.get("node_to_node_encryption_options")
        return result

    @builtins.property
    def snapshot_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.SnapshotOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.SnapshotOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-snapshotoptions
        """
        result = self._values.get("snapshot_options")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::Elasticsearch::Domain.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def vpc_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.VPCOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.VPCOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-vpcoptions
        """
        result = self._values.get("vpc_options")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDomain",
    "CfnDomainProps",
]

publication.publish()
