# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['UserProfile']


class UserProfile(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allow_self_management: Optional[pulumi.Input[bool]] = None,
                 ssh_public_key: Optional[pulumi.Input[str]] = None,
                 ssh_username: Optional[pulumi.Input[str]] = None,
                 user_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides an OpsWorks User Profile resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        my_profile = aws.opsworks.UserProfile("myProfile",
            user_arn=aws_iam_user["user"]["arn"],
            ssh_username="my_user")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] allow_self_management: Whether users can specify their own SSH public key through the My Settings page
        :param pulumi.Input[str] ssh_public_key: The users public key
        :param pulumi.Input[str] ssh_username: The ssh username, with witch this user wants to log in
        :param pulumi.Input[str] user_arn: The user's IAM ARN
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

            __props__['allow_self_management'] = allow_self_management
            __props__['ssh_public_key'] = ssh_public_key
            if ssh_username is None:
                raise TypeError("Missing required property 'ssh_username'")
            __props__['ssh_username'] = ssh_username
            if user_arn is None:
                raise TypeError("Missing required property 'user_arn'")
            __props__['user_arn'] = user_arn
        super(UserProfile, __self__).__init__(
            'aws:opsworks/userProfile:UserProfile',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            allow_self_management: Optional[pulumi.Input[bool]] = None,
            ssh_public_key: Optional[pulumi.Input[str]] = None,
            ssh_username: Optional[pulumi.Input[str]] = None,
            user_arn: Optional[pulumi.Input[str]] = None) -> 'UserProfile':
        """
        Get an existing UserProfile resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] allow_self_management: Whether users can specify their own SSH public key through the My Settings page
        :param pulumi.Input[str] ssh_public_key: The users public key
        :param pulumi.Input[str] ssh_username: The ssh username, with witch this user wants to log in
        :param pulumi.Input[str] user_arn: The user's IAM ARN
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["allow_self_management"] = allow_self_management
        __props__["ssh_public_key"] = ssh_public_key
        __props__["ssh_username"] = ssh_username
        __props__["user_arn"] = user_arn
        return UserProfile(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allowSelfManagement")
    def allow_self_management(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether users can specify their own SSH public key through the My Settings page
        """
        return pulumi.get(self, "allow_self_management")

    @property
    @pulumi.getter(name="sshPublicKey")
    def ssh_public_key(self) -> pulumi.Output[Optional[str]]:
        """
        The users public key
        """
        return pulumi.get(self, "ssh_public_key")

    @property
    @pulumi.getter(name="sshUsername")
    def ssh_username(self) -> pulumi.Output[str]:
        """
        The ssh username, with witch this user wants to log in
        """
        return pulumi.get(self, "ssh_username")

    @property
    @pulumi.getter(name="userArn")
    def user_arn(self) -> pulumi.Output[str]:
        """
        The user's IAM ARN
        """
        return pulumi.get(self, "user_arn")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

