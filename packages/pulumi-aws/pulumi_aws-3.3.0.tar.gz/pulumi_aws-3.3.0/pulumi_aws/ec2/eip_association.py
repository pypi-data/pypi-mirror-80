# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['EipAssociation']


class EipAssociation(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allocation_id: Optional[pulumi.Input[str]] = None,
                 allow_reassociation: Optional[pulumi.Input[bool]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 network_interface_id: Optional[pulumi.Input[str]] = None,
                 private_ip_address: Optional[pulumi.Input[str]] = None,
                 public_ip: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides an AWS EIP Association as a top level resource, to associate and
        disassociate Elastic IPs from AWS Instances and Network Interfaces.

        > **NOTE:** Do not use this resource to associate an EIP to `lb.LoadBalancer` or `ec2.NatGateway` resources. Instead use the `allocation_id` available in those resources to allow AWS to manage the association, otherwise you will see `AuthFailure` errors.

        > **NOTE:** `ec2.EipAssociation` is useful in scenarios where EIPs are either
        pre-existing or distributed to customers or users and therefore cannot be changed.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        web = aws.ec2.Instance("web",
            ami="ami-21f78e11",
            availability_zone="us-west-2a",
            instance_type="t2.micro",
            tags={
                "Name": "HelloWorld",
            })
        example = aws.ec2.Eip("example", vpc=True)
        eip_assoc = aws.ec2.EipAssociation("eipAssoc",
            instance_id=web.id,
            allocation_id=example.id)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] allocation_id: The allocation ID. This is required for EC2-VPC.
        :param pulumi.Input[bool] allow_reassociation: Whether to allow an Elastic IP to
               be re-associated. Defaults to `true` in VPC.
        :param pulumi.Input[str] instance_id: The ID of the instance. This is required for
               EC2-Classic. For EC2-VPC, you can specify either the instance ID or the
               network interface ID, but not both. The operation fails if you specify an
               instance ID unless exactly one network interface is attached.
        :param pulumi.Input[str] network_interface_id: The ID of the network interface. If the
               instance has more than one network interface, you must specify a network
               interface ID.
        :param pulumi.Input[str] private_ip_address: The primary or secondary private IP address
               to associate with the Elastic IP address. If no private IP address is
               specified, the Elastic IP address is associated with the primary private IP
               address.
        :param pulumi.Input[str] public_ip: The Elastic IP address. This is required for EC2-Classic.
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

            __props__['allocation_id'] = allocation_id
            __props__['allow_reassociation'] = allow_reassociation
            __props__['instance_id'] = instance_id
            __props__['network_interface_id'] = network_interface_id
            __props__['private_ip_address'] = private_ip_address
            __props__['public_ip'] = public_ip
        super(EipAssociation, __self__).__init__(
            'aws:ec2/eipAssociation:EipAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            allocation_id: Optional[pulumi.Input[str]] = None,
            allow_reassociation: Optional[pulumi.Input[bool]] = None,
            instance_id: Optional[pulumi.Input[str]] = None,
            network_interface_id: Optional[pulumi.Input[str]] = None,
            private_ip_address: Optional[pulumi.Input[str]] = None,
            public_ip: Optional[pulumi.Input[str]] = None) -> 'EipAssociation':
        """
        Get an existing EipAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] allocation_id: The allocation ID. This is required for EC2-VPC.
        :param pulumi.Input[bool] allow_reassociation: Whether to allow an Elastic IP to
               be re-associated. Defaults to `true` in VPC.
        :param pulumi.Input[str] instance_id: The ID of the instance. This is required for
               EC2-Classic. For EC2-VPC, you can specify either the instance ID or the
               network interface ID, but not both. The operation fails if you specify an
               instance ID unless exactly one network interface is attached.
        :param pulumi.Input[str] network_interface_id: The ID of the network interface. If the
               instance has more than one network interface, you must specify a network
               interface ID.
        :param pulumi.Input[str] private_ip_address: The primary or secondary private IP address
               to associate with the Elastic IP address. If no private IP address is
               specified, the Elastic IP address is associated with the primary private IP
               address.
        :param pulumi.Input[str] public_ip: The Elastic IP address. This is required for EC2-Classic.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["allocation_id"] = allocation_id
        __props__["allow_reassociation"] = allow_reassociation
        __props__["instance_id"] = instance_id
        __props__["network_interface_id"] = network_interface_id
        __props__["private_ip_address"] = private_ip_address
        __props__["public_ip"] = public_ip
        return EipAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allocationId")
    def allocation_id(self) -> pulumi.Output[str]:
        """
        The allocation ID. This is required for EC2-VPC.
        """
        return pulumi.get(self, "allocation_id")

    @property
    @pulumi.getter(name="allowReassociation")
    def allow_reassociation(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether to allow an Elastic IP to
        be re-associated. Defaults to `true` in VPC.
        """
        return pulumi.get(self, "allow_reassociation")

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Output[str]:
        """
        The ID of the instance. This is required for
        EC2-Classic. For EC2-VPC, you can specify either the instance ID or the
        network interface ID, but not both. The operation fails if you specify an
        instance ID unless exactly one network interface is attached.
        """
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter(name="networkInterfaceId")
    def network_interface_id(self) -> pulumi.Output[str]:
        """
        The ID of the network interface. If the
        instance has more than one network interface, you must specify a network
        interface ID.
        """
        return pulumi.get(self, "network_interface_id")

    @property
    @pulumi.getter(name="privateIpAddress")
    def private_ip_address(self) -> pulumi.Output[str]:
        """
        The primary or secondary private IP address
        to associate with the Elastic IP address. If no private IP address is
        specified, the Elastic IP address is associated with the primary private IP
        address.
        """
        return pulumi.get(self, "private_ip_address")

    @property
    @pulumi.getter(name="publicIp")
    def public_ip(self) -> pulumi.Output[str]:
        """
        The Elastic IP address. This is required for EC2-Classic.
        """
        return pulumi.get(self, "public_ip")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

