# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['CustomerGateway']


class CustomerGateway(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bgp_asn: Optional[pulumi.Input[str]] = None,
                 ip_address: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides a customer gateway inside a VPC. These objects can be connected to VPN gateways via VPN connections, and allow you to establish tunnels between your network and the VPC.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        main = aws.ec2.CustomerGateway("main",
            bgp_asn="65000",
            ip_address="172.83.124.10",
            tags={
                "Name": "main-customer-gateway",
            },
            type="ipsec.1")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bgp_asn: The gateway's Border Gateway Protocol (BGP) Autonomous System Number (ASN).
        :param pulumi.Input[str] ip_address: The IP address of the gateway's Internet-routable external interface.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags to apply to the gateway.
        :param pulumi.Input[str] type: The type of customer gateway. The only type AWS
               supports at this time is "ipsec.1".
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

            if bgp_asn is None:
                raise TypeError("Missing required property 'bgp_asn'")
            __props__['bgp_asn'] = bgp_asn
            if ip_address is None:
                raise TypeError("Missing required property 'ip_address'")
            __props__['ip_address'] = ip_address
            __props__['tags'] = tags
            if type is None:
                raise TypeError("Missing required property 'type'")
            __props__['type'] = type
            __props__['arn'] = None
        super(CustomerGateway, __self__).__init__(
            'aws:ec2/customerGateway:CustomerGateway',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            bgp_asn: Optional[pulumi.Input[str]] = None,
            ip_address: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            type: Optional[pulumi.Input[str]] = None) -> 'CustomerGateway':
        """
        Get an existing CustomerGateway resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the customer gateway.
        :param pulumi.Input[str] bgp_asn: The gateway's Border Gateway Protocol (BGP) Autonomous System Number (ASN).
        :param pulumi.Input[str] ip_address: The IP address of the gateway's Internet-routable external interface.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags to apply to the gateway.
        :param pulumi.Input[str] type: The type of customer gateway. The only type AWS
               supports at this time is "ipsec.1".
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["bgp_asn"] = bgp_asn
        __props__["ip_address"] = ip_address
        __props__["tags"] = tags
        __props__["type"] = type
        return CustomerGateway(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the customer gateway.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="bgpAsn")
    def bgp_asn(self) -> pulumi.Output[str]:
        """
        The gateway's Border Gateway Protocol (BGP) Autonomous System Number (ASN).
        """
        return pulumi.get(self, "bgp_asn")

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> pulumi.Output[str]:
        """
        The IP address of the gateway's Internet-routable external interface.
        """
        return pulumi.get(self, "ip_address")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Tags to apply to the gateway.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of customer gateway. The only type AWS
        supports at this time is "ipsec.1".
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

