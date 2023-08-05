# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['Connection']


class Connection(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bandwidth: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides a Connection of Direct Connect.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        hoge = aws.directconnect.Connection("hoge",
            bandwidth="1Gbps",
            location="EqDC2")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bandwidth: The bandwidth of the connection. Valid values for dedicated connections: 1Gbps, 10Gbps. Valid values for hosted connections: 50Mbps, 100Mbps, 200Mbps, 300Mbps, 400Mbps, 500Mbps, 1Gbps, 2Gbps, 5Gbps and 10Gbps. Case sensitive.
        :param pulumi.Input[str] location: The AWS Direct Connect location where the connection is located. See [DescribeLocations](https://docs.aws.amazon.com/directconnect/latest/APIReference/API_DescribeLocations.html) for the list of AWS Direct Connect locations. Use `locationCode`.
        :param pulumi.Input[str] name: The name of the connection.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            if bandwidth is None:
                raise TypeError("Missing required property 'bandwidth'")
            __props__['bandwidth'] = bandwidth
            if location is None:
                raise TypeError("Missing required property 'location'")
            __props__['location'] = location
            __props__['name'] = name
            __props__['tags'] = tags
            __props__['arn'] = None
            __props__['aws_device'] = None
            __props__['has_logical_redundancy'] = None
            __props__['jumbo_frame_capable'] = None
        super(Connection, __self__).__init__(
            'aws:directconnect/connection:Connection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            aws_device: Optional[pulumi.Input[str]] = None,
            bandwidth: Optional[pulumi.Input[str]] = None,
            has_logical_redundancy: Optional[pulumi.Input[str]] = None,
            jumbo_frame_capable: Optional[pulumi.Input[bool]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'Connection':
        """
        Get an existing Connection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the connection.
        :param pulumi.Input[str] aws_device: The Direct Connect endpoint on which the physical connection terminates.
        :param pulumi.Input[str] bandwidth: The bandwidth of the connection. Valid values for dedicated connections: 1Gbps, 10Gbps. Valid values for hosted connections: 50Mbps, 100Mbps, 200Mbps, 300Mbps, 400Mbps, 500Mbps, 1Gbps, 2Gbps, 5Gbps and 10Gbps. Case sensitive.
        :param pulumi.Input[str] has_logical_redundancy: Indicates whether the connection supports a secondary BGP peer in the same address family (IPv4/IPv6).
        :param pulumi.Input[bool] jumbo_frame_capable: Boolean value representing if jumbo frames have been enabled for this connection.
        :param pulumi.Input[str] location: The AWS Direct Connect location where the connection is located. See [DescribeLocations](https://docs.aws.amazon.com/directconnect/latest/APIReference/API_DescribeLocations.html) for the list of AWS Direct Connect locations. Use `locationCode`.
        :param pulumi.Input[str] name: The name of the connection.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["aws_device"] = aws_device
        __props__["bandwidth"] = bandwidth
        __props__["has_logical_redundancy"] = has_logical_redundancy
        __props__["jumbo_frame_capable"] = jumbo_frame_capable
        __props__["location"] = location
        __props__["name"] = name
        __props__["tags"] = tags
        return Connection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the connection.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="awsDevice")
    def aws_device(self) -> pulumi.Output[str]:
        """
        The Direct Connect endpoint on which the physical connection terminates.
        """
        return pulumi.get(self, "aws_device")

    @property
    @pulumi.getter
    def bandwidth(self) -> pulumi.Output[str]:
        """
        The bandwidth of the connection. Valid values for dedicated connections: 1Gbps, 10Gbps. Valid values for hosted connections: 50Mbps, 100Mbps, 200Mbps, 300Mbps, 400Mbps, 500Mbps, 1Gbps, 2Gbps, 5Gbps and 10Gbps. Case sensitive.
        """
        return pulumi.get(self, "bandwidth")

    @property
    @pulumi.getter(name="hasLogicalRedundancy")
    def has_logical_redundancy(self) -> pulumi.Output[str]:
        """
        Indicates whether the connection supports a secondary BGP peer in the same address family (IPv4/IPv6).
        """
        return pulumi.get(self, "has_logical_redundancy")

    @property
    @pulumi.getter(name="jumboFrameCapable")
    def jumbo_frame_capable(self) -> pulumi.Output[bool]:
        """
        Boolean value representing if jumbo frames have been enabled for this connection.
        """
        return pulumi.get(self, "jumbo_frame_capable")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The AWS Direct Connect location where the connection is located. See [DescribeLocations](https://docs.aws.amazon.com/directconnect/latest/APIReference/API_DescribeLocations.html) for the list of AWS Direct Connect locations. Use `locationCode`.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the connection.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

