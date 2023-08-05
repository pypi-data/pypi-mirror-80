# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from . import outputs

__all__ = [
    'ClusterCertificateAuthority',
    'ClusterEncryptionConfig',
    'ClusterEncryptionConfigProvider',
    'ClusterIdentity',
    'ClusterIdentityOidc',
    'ClusterVpcConfig',
    'FargateProfileSelector',
    'NodeGroupLaunchTemplate',
    'NodeGroupRemoteAccess',
    'NodeGroupResource',
    'NodeGroupResourceAutoscalingGroup',
    'NodeGroupScalingConfig',
    'GetClusterCertificateAuthorityResult',
    'GetClusterIdentityResult',
    'GetClusterIdentityOidcResult',
    'GetClusterVpcConfigResult',
]

@pulumi.output_type
class ClusterCertificateAuthority(dict):
    def __init__(__self__, *,
                 data: Optional[str] = None):
        """
        :param str data: The base64 encoded certificate data required to communicate with your cluster. Add this to the `certificate-authority-data` section of the `kubeconfig` file for your cluster.
        """
        if data is not None:
            pulumi.set(__self__, "data", data)

    @property
    @pulumi.getter
    def data(self) -> Optional[str]:
        """
        The base64 encoded certificate data required to communicate with your cluster. Add this to the `certificate-authority-data` section of the `kubeconfig` file for your cluster.
        """
        return pulumi.get(self, "data")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ClusterEncryptionConfig(dict):
    def __init__(__self__, *,
                 provider: 'outputs.ClusterEncryptionConfigProvider',
                 resources: Sequence[str]):
        """
        :param 'ClusterEncryptionConfigProviderArgs' provider: Configuration block with provider for encryption. Detailed below.
        :param Sequence[str] resources: List of strings with resources to be encrypted. Valid values: `secrets`
        """
        pulumi.set(__self__, "provider", provider)
        pulumi.set(__self__, "resources", resources)

    @property
    @pulumi.getter
    def provider(self) -> 'outputs.ClusterEncryptionConfigProvider':
        """
        Configuration block with provider for encryption. Detailed below.
        """
        return pulumi.get(self, "provider")

    @property
    @pulumi.getter
    def resources(self) -> Sequence[str]:
        """
        List of strings with resources to be encrypted. Valid values: `secrets`
        """
        return pulumi.get(self, "resources")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ClusterEncryptionConfigProvider(dict):
    def __init__(__self__, *,
                 key_arn: str):
        """
        :param str key_arn: Amazon Resource Name (ARN) of the Key Management Service (KMS) customer master key (CMK). The CMK must be symmetric, created in the same region as the cluster, and if the CMK was created in a different account, the user must have access to the CMK. For more information, see [Allowing Users in Other Accounts to Use a CMK in the AWS Key Management Service Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html).
        """
        pulumi.set(__self__, "key_arn", key_arn)

    @property
    @pulumi.getter(name="keyArn")
    def key_arn(self) -> str:
        """
        Amazon Resource Name (ARN) of the Key Management Service (KMS) customer master key (CMK). The CMK must be symmetric, created in the same region as the cluster, and if the CMK was created in a different account, the user must have access to the CMK. For more information, see [Allowing Users in Other Accounts to Use a CMK in the AWS Key Management Service Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html).
        """
        return pulumi.get(self, "key_arn")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ClusterIdentity(dict):
    def __init__(__self__, *,
                 oidcs: Optional[Sequence['outputs.ClusterIdentityOidc']] = None):
        """
        :param Sequence['ClusterIdentityOidcArgs'] oidcs: Nested attribute containing [OpenID Connect](https://openid.net/connect/) identity provider information for the cluster.
        """
        if oidcs is not None:
            pulumi.set(__self__, "oidcs", oidcs)

    @property
    @pulumi.getter
    def oidcs(self) -> Optional[Sequence['outputs.ClusterIdentityOidc']]:
        """
        Nested attribute containing [OpenID Connect](https://openid.net/connect/) identity provider information for the cluster.
        """
        return pulumi.get(self, "oidcs")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ClusterIdentityOidc(dict):
    def __init__(__self__, *,
                 issuer: Optional[str] = None):
        """
        :param str issuer: Issuer URL for the OpenID Connect identity provider.
        """
        if issuer is not None:
            pulumi.set(__self__, "issuer", issuer)

    @property
    @pulumi.getter
    def issuer(self) -> Optional[str]:
        """
        Issuer URL for the OpenID Connect identity provider.
        """
        return pulumi.get(self, "issuer")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ClusterVpcConfig(dict):
    def __init__(__self__, *,
                 subnet_ids: Sequence[str],
                 cluster_security_group_id: Optional[str] = None,
                 endpoint_private_access: Optional[bool] = None,
                 endpoint_public_access: Optional[bool] = None,
                 public_access_cidrs: Optional[Sequence[str]] = None,
                 security_group_ids: Optional[Sequence[str]] = None,
                 vpc_id: Optional[str] = None):
        """
        :param Sequence[str] subnet_ids: List of subnet IDs. Must be in at least two different availability zones. Amazon EKS creates cross-account elastic network interfaces in these subnets to allow communication between your worker nodes and the Kubernetes control plane.
        :param str cluster_security_group_id: The cluster security group that was created by Amazon EKS for the cluster.
        :param bool endpoint_private_access: Indicates whether or not the Amazon EKS private API server endpoint is enabled. Default is `false`.
        :param bool endpoint_public_access: Indicates whether or not the Amazon EKS public API server endpoint is enabled. Default is `true`.
        :param Sequence[str] public_access_cidrs: List of CIDR blocks. Indicates which CIDR blocks can access the Amazon EKS public API server endpoint when enabled. EKS defaults this to a list with `0.0.0.0/0`. This provider will only perform drift detection of its value when present in a configuration.
        :param Sequence[str] security_group_ids: List of security group IDs for the cross-account elastic network interfaces that Amazon EKS creates to use to allow communication between your worker nodes and the Kubernetes control plane.
        :param str vpc_id: The VPC associated with your cluster.
        """
        pulumi.set(__self__, "subnet_ids", subnet_ids)
        if cluster_security_group_id is not None:
            pulumi.set(__self__, "cluster_security_group_id", cluster_security_group_id)
        if endpoint_private_access is not None:
            pulumi.set(__self__, "endpoint_private_access", endpoint_private_access)
        if endpoint_public_access is not None:
            pulumi.set(__self__, "endpoint_public_access", endpoint_public_access)
        if public_access_cidrs is not None:
            pulumi.set(__self__, "public_access_cidrs", public_access_cidrs)
        if security_group_ids is not None:
            pulumi.set(__self__, "security_group_ids", security_group_ids)
        if vpc_id is not None:
            pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Sequence[str]:
        """
        List of subnet IDs. Must be in at least two different availability zones. Amazon EKS creates cross-account elastic network interfaces in these subnets to allow communication between your worker nodes and the Kubernetes control plane.
        """
        return pulumi.get(self, "subnet_ids")

    @property
    @pulumi.getter(name="clusterSecurityGroupId")
    def cluster_security_group_id(self) -> Optional[str]:
        """
        The cluster security group that was created by Amazon EKS for the cluster.
        """
        return pulumi.get(self, "cluster_security_group_id")

    @property
    @pulumi.getter(name="endpointPrivateAccess")
    def endpoint_private_access(self) -> Optional[bool]:
        """
        Indicates whether or not the Amazon EKS private API server endpoint is enabled. Default is `false`.
        """
        return pulumi.get(self, "endpoint_private_access")

    @property
    @pulumi.getter(name="endpointPublicAccess")
    def endpoint_public_access(self) -> Optional[bool]:
        """
        Indicates whether or not the Amazon EKS public API server endpoint is enabled. Default is `true`.
        """
        return pulumi.get(self, "endpoint_public_access")

    @property
    @pulumi.getter(name="publicAccessCidrs")
    def public_access_cidrs(self) -> Optional[Sequence[str]]:
        """
        List of CIDR blocks. Indicates which CIDR blocks can access the Amazon EKS public API server endpoint when enabled. EKS defaults this to a list with `0.0.0.0/0`. This provider will only perform drift detection of its value when present in a configuration.
        """
        return pulumi.get(self, "public_access_cidrs")

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Optional[Sequence[str]]:
        """
        List of security group IDs for the cross-account elastic network interfaces that Amazon EKS creates to use to allow communication between your worker nodes and the Kubernetes control plane.
        """
        return pulumi.get(self, "security_group_ids")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[str]:
        """
        The VPC associated with your cluster.
        """
        return pulumi.get(self, "vpc_id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class FargateProfileSelector(dict):
    def __init__(__self__, *,
                 namespace: str,
                 labels: Optional[Mapping[str, str]] = None):
        """
        :param str namespace: Kubernetes namespace for selection.
        :param Mapping[str, str] labels: Key-value map of Kubernetes labels for selection.
        """
        pulumi.set(__self__, "namespace", namespace)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)

    @property
    @pulumi.getter
    def namespace(self) -> str:
        """
        Kubernetes namespace for selection.
        """
        return pulumi.get(self, "namespace")

    @property
    @pulumi.getter
    def labels(self) -> Optional[Mapping[str, str]]:
        """
        Key-value map of Kubernetes labels for selection.
        """
        return pulumi.get(self, "labels")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class NodeGroupLaunchTemplate(dict):
    def __init__(__self__, *,
                 version: str,
                 id: Optional[str] = None,
                 name: Optional[str] = None):
        """
        :param str id: Identifier of the EC2 Launch Template. Conflicts with `name`.
        :param str name: Name of the EC2 Launch Template. Conflicts with `id`.
        """
        pulumi.set(__self__, "version", version)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def version(self) -> str:
        return pulumi.get(self, "version")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Identifier of the EC2 Launch Template. Conflicts with `name`.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Name of the EC2 Launch Template. Conflicts with `id`.
        """
        return pulumi.get(self, "name")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class NodeGroupRemoteAccess(dict):
    def __init__(__self__, *,
                 ec2_ssh_key: Optional[str] = None,
                 source_security_group_ids: Optional[Sequence[str]] = None):
        """
        :param str ec2_ssh_key: EC2 Key Pair name that provides access for SSH communication with the worker nodes in the EKS Node Group. If you specify this configuration, but do not specify `source_security_group_ids` when you create an EKS Node Group, port 22 on the worker nodes is opened to the Internet (0.0.0.0/0).
        :param Sequence[str] source_security_group_ids: Set of EC2 Security Group IDs to allow SSH access (port 22) from on the worker nodes. If you specify `ec2_ssh_key`, but do not specify this configuration when you create an EKS Node Group, port 22 on the worker nodes is opened to the Internet (0.0.0.0/0).
        """
        if ec2_ssh_key is not None:
            pulumi.set(__self__, "ec2_ssh_key", ec2_ssh_key)
        if source_security_group_ids is not None:
            pulumi.set(__self__, "source_security_group_ids", source_security_group_ids)

    @property
    @pulumi.getter(name="ec2SshKey")
    def ec2_ssh_key(self) -> Optional[str]:
        """
        EC2 Key Pair name that provides access for SSH communication with the worker nodes in the EKS Node Group. If you specify this configuration, but do not specify `source_security_group_ids` when you create an EKS Node Group, port 22 on the worker nodes is opened to the Internet (0.0.0.0/0).
        """
        return pulumi.get(self, "ec2_ssh_key")

    @property
    @pulumi.getter(name="sourceSecurityGroupIds")
    def source_security_group_ids(self) -> Optional[Sequence[str]]:
        """
        Set of EC2 Security Group IDs to allow SSH access (port 22) from on the worker nodes. If you specify `ec2_ssh_key`, but do not specify this configuration when you create an EKS Node Group, port 22 on the worker nodes is opened to the Internet (0.0.0.0/0).
        """
        return pulumi.get(self, "source_security_group_ids")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class NodeGroupResource(dict):
    def __init__(__self__, *,
                 autoscaling_groups: Optional[Sequence['outputs.NodeGroupResourceAutoscalingGroup']] = None,
                 remote_access_security_group_id: Optional[str] = None):
        """
        :param Sequence['NodeGroupResourceAutoscalingGroupArgs'] autoscaling_groups: List of objects containing information about AutoScaling Groups.
        :param str remote_access_security_group_id: Identifier of the remote access EC2 Security Group.
        """
        if autoscaling_groups is not None:
            pulumi.set(__self__, "autoscaling_groups", autoscaling_groups)
        if remote_access_security_group_id is not None:
            pulumi.set(__self__, "remote_access_security_group_id", remote_access_security_group_id)

    @property
    @pulumi.getter(name="autoscalingGroups")
    def autoscaling_groups(self) -> Optional[Sequence['outputs.NodeGroupResourceAutoscalingGroup']]:
        """
        List of objects containing information about AutoScaling Groups.
        """
        return pulumi.get(self, "autoscaling_groups")

    @property
    @pulumi.getter(name="remoteAccessSecurityGroupId")
    def remote_access_security_group_id(self) -> Optional[str]:
        """
        Identifier of the remote access EC2 Security Group.
        """
        return pulumi.get(self, "remote_access_security_group_id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class NodeGroupResourceAutoscalingGroup(dict):
    def __init__(__self__, *,
                 name: Optional[str] = None):
        """
        :param str name: Name of the EC2 Launch Template. Conflicts with `id`.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Name of the EC2 Launch Template. Conflicts with `id`.
        """
        return pulumi.get(self, "name")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class NodeGroupScalingConfig(dict):
    def __init__(__self__, *,
                 desired_size: int,
                 max_size: int,
                 min_size: int):
        """
        :param int desired_size: Desired number of worker nodes.
        :param int max_size: Maximum number of worker nodes.
        :param int min_size: Minimum number of worker nodes.
        """
        pulumi.set(__self__, "desired_size", desired_size)
        pulumi.set(__self__, "max_size", max_size)
        pulumi.set(__self__, "min_size", min_size)

    @property
    @pulumi.getter(name="desiredSize")
    def desired_size(self) -> int:
        """
        Desired number of worker nodes.
        """
        return pulumi.get(self, "desired_size")

    @property
    @pulumi.getter(name="maxSize")
    def max_size(self) -> int:
        """
        Maximum number of worker nodes.
        """
        return pulumi.get(self, "max_size")

    @property
    @pulumi.getter(name="minSize")
    def min_size(self) -> int:
        """
        Minimum number of worker nodes.
        """
        return pulumi.get(self, "min_size")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class GetClusterCertificateAuthorityResult(dict):
    def __init__(__self__, *,
                 data: str):
        """
        :param str data: The base64 encoded certificate data required to communicate with your cluster. Add this to the `certificate-authority-data` section of the `kubeconfig` file for your cluster.
        """
        pulumi.set(__self__, "data", data)

    @property
    @pulumi.getter
    def data(self) -> str:
        """
        The base64 encoded certificate data required to communicate with your cluster. Add this to the `certificate-authority-data` section of the `kubeconfig` file for your cluster.
        """
        return pulumi.get(self, "data")


@pulumi.output_type
class GetClusterIdentityResult(dict):
    def __init__(__self__, *,
                 oidcs: Sequence['outputs.GetClusterIdentityOidcResult']):
        """
        :param Sequence['GetClusterIdentityOidcArgs'] oidcs: Nested attribute containing [OpenID Connect](https://openid.net/connect/) identity provider information for the cluster.
        """
        pulumi.set(__self__, "oidcs", oidcs)

    @property
    @pulumi.getter
    def oidcs(self) -> Sequence['outputs.GetClusterIdentityOidcResult']:
        """
        Nested attribute containing [OpenID Connect](https://openid.net/connect/) identity provider information for the cluster.
        """
        return pulumi.get(self, "oidcs")


@pulumi.output_type
class GetClusterIdentityOidcResult(dict):
    def __init__(__self__, *,
                 issuer: str):
        """
        :param str issuer: Issuer URL for the OpenID Connect identity provider.
        """
        pulumi.set(__self__, "issuer", issuer)

    @property
    @pulumi.getter
    def issuer(self) -> str:
        """
        Issuer URL for the OpenID Connect identity provider.
        """
        return pulumi.get(self, "issuer")


@pulumi.output_type
class GetClusterVpcConfigResult(dict):
    def __init__(__self__, *,
                 cluster_security_group_id: str,
                 endpoint_private_access: bool,
                 endpoint_public_access: bool,
                 public_access_cidrs: Sequence[str],
                 security_group_ids: Sequence[str],
                 subnet_ids: Sequence[str],
                 vpc_id: str):
        """
        :param str cluster_security_group_id: The cluster security group that was created by Amazon EKS for the cluster.
        :param bool endpoint_private_access: Indicates whether or not the Amazon EKS private API server endpoint is enabled.
        :param bool endpoint_public_access: Indicates whether or not the Amazon EKS public API server endpoint is enabled.
        :param Sequence[str] public_access_cidrs: List of CIDR blocks. Indicates which CIDR blocks can access the Amazon EKS public API server endpoint.
        :param Sequence[str] security_group_ids: List of security group IDs
        :param Sequence[str] subnet_ids: List of subnet IDs
        :param str vpc_id: The VPC associated with your cluster.
        """
        pulumi.set(__self__, "cluster_security_group_id", cluster_security_group_id)
        pulumi.set(__self__, "endpoint_private_access", endpoint_private_access)
        pulumi.set(__self__, "endpoint_public_access", endpoint_public_access)
        pulumi.set(__self__, "public_access_cidrs", public_access_cidrs)
        pulumi.set(__self__, "security_group_ids", security_group_ids)
        pulumi.set(__self__, "subnet_ids", subnet_ids)
        pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="clusterSecurityGroupId")
    def cluster_security_group_id(self) -> str:
        """
        The cluster security group that was created by Amazon EKS for the cluster.
        """
        return pulumi.get(self, "cluster_security_group_id")

    @property
    @pulumi.getter(name="endpointPrivateAccess")
    def endpoint_private_access(self) -> bool:
        """
        Indicates whether or not the Amazon EKS private API server endpoint is enabled.
        """
        return pulumi.get(self, "endpoint_private_access")

    @property
    @pulumi.getter(name="endpointPublicAccess")
    def endpoint_public_access(self) -> bool:
        """
        Indicates whether or not the Amazon EKS public API server endpoint is enabled.
        """
        return pulumi.get(self, "endpoint_public_access")

    @property
    @pulumi.getter(name="publicAccessCidrs")
    def public_access_cidrs(self) -> Sequence[str]:
        """
        List of CIDR blocks. Indicates which CIDR blocks can access the Amazon EKS public API server endpoint.
        """
        return pulumi.get(self, "public_access_cidrs")

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Sequence[str]:
        """
        List of security group IDs
        """
        return pulumi.get(self, "security_group_ids")

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Sequence[str]:
        """
        List of subnet IDs
        """
        return pulumi.get(self, "subnet_ids")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> str:
        """
        The VPC associated with your cluster.
        """
        return pulumi.get(self, "vpc_id")


