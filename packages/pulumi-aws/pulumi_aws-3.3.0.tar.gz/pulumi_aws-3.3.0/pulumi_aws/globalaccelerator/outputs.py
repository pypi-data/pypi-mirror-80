# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = [
    'AcceleratorAttributes',
    'AcceleratorIpSet',
    'EndpointGroupEndpointConfiguration',
    'ListenerPortRange',
]

@pulumi.output_type
class AcceleratorAttributes(dict):
    def __init__(__self__, *,
                 flow_logs_enabled: Optional[bool] = None,
                 flow_logs_s3_bucket: Optional[str] = None,
                 flow_logs_s3_prefix: Optional[str] = None):
        """
        :param bool flow_logs_enabled: Indicates whether flow logs are enabled.
        :param str flow_logs_s3_bucket: The name of the Amazon S3 bucket for the flow logs.
        :param str flow_logs_s3_prefix: The prefix for the location in the Amazon S3 bucket for the flow logs.
        """
        if flow_logs_enabled is not None:
            pulumi.set(__self__, "flow_logs_enabled", flow_logs_enabled)
        if flow_logs_s3_bucket is not None:
            pulumi.set(__self__, "flow_logs_s3_bucket", flow_logs_s3_bucket)
        if flow_logs_s3_prefix is not None:
            pulumi.set(__self__, "flow_logs_s3_prefix", flow_logs_s3_prefix)

    @property
    @pulumi.getter(name="flowLogsEnabled")
    def flow_logs_enabled(self) -> Optional[bool]:
        """
        Indicates whether flow logs are enabled.
        """
        return pulumi.get(self, "flow_logs_enabled")

    @property
    @pulumi.getter(name="flowLogsS3Bucket")
    def flow_logs_s3_bucket(self) -> Optional[str]:
        """
        The name of the Amazon S3 bucket for the flow logs.
        """
        return pulumi.get(self, "flow_logs_s3_bucket")

    @property
    @pulumi.getter(name="flowLogsS3Prefix")
    def flow_logs_s3_prefix(self) -> Optional[str]:
        """
        The prefix for the location in the Amazon S3 bucket for the flow logs.
        """
        return pulumi.get(self, "flow_logs_s3_prefix")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class AcceleratorIpSet(dict):
    def __init__(__self__, *,
                 ip_addresses: Optional[Sequence[str]] = None,
                 ip_family: Optional[str] = None):
        """
        :param Sequence[str] ip_addresses: A list of IP addresses in the IP address set.
        :param str ip_family: The types of IP addresses included in this IP set.
        """
        if ip_addresses is not None:
            pulumi.set(__self__, "ip_addresses", ip_addresses)
        if ip_family is not None:
            pulumi.set(__self__, "ip_family", ip_family)

    @property
    @pulumi.getter(name="ipAddresses")
    def ip_addresses(self) -> Optional[Sequence[str]]:
        """
        A list of IP addresses in the IP address set.
        """
        return pulumi.get(self, "ip_addresses")

    @property
    @pulumi.getter(name="ipFamily")
    def ip_family(self) -> Optional[str]:
        """
        The types of IP addresses included in this IP set.
        """
        return pulumi.get(self, "ip_family")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class EndpointGroupEndpointConfiguration(dict):
    def __init__(__self__, *,
                 client_ip_preservation_enabled: Optional[bool] = None,
                 endpoint_id: Optional[str] = None,
                 weight: Optional[int] = None):
        """
        :param str endpoint_id: An ID for the endpoint. If the endpoint is a Network Load Balancer or Application Load Balancer, this is the Amazon Resource Name (ARN) of the resource. If the endpoint is an Elastic IP address, this is the Elastic IP address allocation ID.
        :param int weight: The weight associated with the endpoint. When you add weights to endpoints, you configure AWS Global Accelerator to route traffic based on proportions that you specify.
        """
        if client_ip_preservation_enabled is not None:
            pulumi.set(__self__, "client_ip_preservation_enabled", client_ip_preservation_enabled)
        if endpoint_id is not None:
            pulumi.set(__self__, "endpoint_id", endpoint_id)
        if weight is not None:
            pulumi.set(__self__, "weight", weight)

    @property
    @pulumi.getter(name="clientIpPreservationEnabled")
    def client_ip_preservation_enabled(self) -> Optional[bool]:
        return pulumi.get(self, "client_ip_preservation_enabled")

    @property
    @pulumi.getter(name="endpointId")
    def endpoint_id(self) -> Optional[str]:
        """
        An ID for the endpoint. If the endpoint is a Network Load Balancer or Application Load Balancer, this is the Amazon Resource Name (ARN) of the resource. If the endpoint is an Elastic IP address, this is the Elastic IP address allocation ID.
        """
        return pulumi.get(self, "endpoint_id")

    @property
    @pulumi.getter
    def weight(self) -> Optional[int]:
        """
        The weight associated with the endpoint. When you add weights to endpoints, you configure AWS Global Accelerator to route traffic based on proportions that you specify.
        """
        return pulumi.get(self, "weight")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ListenerPortRange(dict):
    def __init__(__self__, *,
                 from_port: Optional[int] = None,
                 to_port: Optional[int] = None):
        """
        :param int from_port: The first port in the range of ports, inclusive.
        :param int to_port: The last port in the range of ports, inclusive.
        """
        if from_port is not None:
            pulumi.set(__self__, "from_port", from_port)
        if to_port is not None:
            pulumi.set(__self__, "to_port", to_port)

    @property
    @pulumi.getter(name="fromPort")
    def from_port(self) -> Optional[int]:
        """
        The first port in the range of ports, inclusive.
        """
        return pulumi.get(self, "from_port")

    @property
    @pulumi.getter(name="toPort")
    def to_port(self) -> Optional[int]:
        """
        The last port in the range of ports, inclusive.
        """
        return pulumi.get(self, "to_port")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


