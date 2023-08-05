# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['InstanceProfile']


class InstanceProfile(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 name_prefix: Optional[pulumi.Input[str]] = None,
                 path: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides an IAM instance profile.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        role = aws.iam.Role("role",
            path="/",
            assume_role_policy=\"\"\"{
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "sts:AssumeRole",
                    "Principal": {
                       "Service": "ec2.amazonaws.com"
                    },
                    "Effect": "Allow",
                    "Sid": ""
                }
            ]
        }
        \"\"\")
        test_profile = aws.iam.InstanceProfile("testProfile", role=role.name)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The profile's name. If omitted, this provider will assign a random, unique name.
        :param pulumi.Input[str] name_prefix: Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        :param pulumi.Input[str] path: Path in which to create the profile.
        :param pulumi.Input[str] role: The role name to include in the profile.
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

            __props__['name'] = name
            __props__['name_prefix'] = name_prefix
            __props__['path'] = path
            __props__['role'] = role
            __props__['arn'] = None
            __props__['create_date'] = None
            __props__['unique_id'] = None
        super(InstanceProfile, __self__).__init__(
            'aws:iam/instanceProfile:InstanceProfile',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            create_date: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            name_prefix: Optional[pulumi.Input[str]] = None,
            path: Optional[pulumi.Input[str]] = None,
            role: Optional[pulumi.Input[str]] = None,
            unique_id: Optional[pulumi.Input[str]] = None) -> 'InstanceProfile':
        """
        Get an existing InstanceProfile resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN assigned by AWS to the instance profile.
        :param pulumi.Input[str] create_date: The creation timestamp of the instance profile.
        :param pulumi.Input[str] name: The profile's name. If omitted, this provider will assign a random, unique name.
        :param pulumi.Input[str] name_prefix: Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        :param pulumi.Input[str] path: Path in which to create the profile.
        :param pulumi.Input[str] role: The role name to include in the profile.
        :param pulumi.Input[str] unique_id: The [unique ID][1] assigned by AWS.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["create_date"] = create_date
        __props__["name"] = name
        __props__["name_prefix"] = name_prefix
        __props__["path"] = path
        __props__["role"] = role
        __props__["unique_id"] = unique_id
        return InstanceProfile(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN assigned by AWS to the instance profile.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="createDate")
    def create_date(self) -> pulumi.Output[str]:
        """
        The creation timestamp of the instance profile.
        """
        return pulumi.get(self, "create_date")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The profile's name. If omitted, this provider will assign a random, unique name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="namePrefix")
    def name_prefix(self) -> pulumi.Output[Optional[str]]:
        """
        Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        """
        return pulumi.get(self, "name_prefix")

    @property
    @pulumi.getter
    def path(self) -> pulumi.Output[Optional[str]]:
        """
        Path in which to create the profile.
        """
        return pulumi.get(self, "path")

    @property
    @pulumi.getter
    def role(self) -> pulumi.Output[Optional[str]]:
        """
        The role name to include in the profile.
        """
        return pulumi.get(self, "role")

    @property
    @pulumi.getter(name="uniqueId")
    def unique_id(self) -> pulumi.Output[str]:
        """
        The [unique ID][1] assigned by AWS.
        """
        return pulumi.get(self, "unique_id")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

