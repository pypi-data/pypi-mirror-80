# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['DomainIdentityVerification']


class DomainIdentityVerification(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 domain: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Represents a successful verification of an SES domain identity.

        Most commonly, this resource is used together with `route53.Record` and
        `ses.DomainIdentity` to request an SES domain identity,
        deploy the required DNS verification records, and wait for verification to complete.

        > **WARNING:** This resource implements a part of the verification workflow. It does not represent a real-world entity in AWS, therefore changing or deleting this resource on its own has no immediate effect.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ses.DomainIdentity("example", domain="example.com")
        example_amazonses_verification_record = aws.route53.Record("exampleAmazonsesVerificationRecord",
            zone_id=aws_route53_zone["example"]["zone_id"],
            name=example.id.apply(lambda id: f"_amazonses.{id}"),
            type="TXT",
            ttl=600,
            records=[example.verification_token])
        example_verification = aws.ses.DomainIdentityVerification("exampleVerification", domain=example.id,
        opts=ResourceOptions(depends_on=[example_amazonses_verification_record]))
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] domain: The domain name of the SES domain identity to verify.
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

            if domain is None:
                raise TypeError("Missing required property 'domain'")
            __props__['domain'] = domain
            __props__['arn'] = None
        super(DomainIdentityVerification, __self__).__init__(
            'aws:ses/domainIdentityVerification:DomainIdentityVerification',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            domain: Optional[pulumi.Input[str]] = None) -> 'DomainIdentityVerification':
        """
        Get an existing DomainIdentityVerification resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the domain identity.
        :param pulumi.Input[str] domain: The domain name of the SES domain identity to verify.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["domain"] = domain
        return DomainIdentityVerification(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the domain identity.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def domain(self) -> pulumi.Output[str]:
        """
        The domain name of the SES domain identity to verify.
        """
        return pulumi.get(self, "domain")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

