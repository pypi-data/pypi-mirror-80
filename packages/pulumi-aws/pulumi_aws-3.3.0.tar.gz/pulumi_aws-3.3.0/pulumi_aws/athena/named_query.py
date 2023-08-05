# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['NamedQuery']


class NamedQuery(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 database: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 query: Optional[pulumi.Input[str]] = None,
                 workgroup: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides an Athena Named Query resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        hoge_bucket = aws.s3.Bucket("hogeBucket")
        test_key = aws.kms.Key("testKey",
            deletion_window_in_days=7,
            description="Athena KMS Key")
        test_workgroup = aws.athena.Workgroup("testWorkgroup", configuration=aws.athena.WorkgroupConfigurationArgs(
            result_configuration=aws.athena.WorkgroupConfigurationResultConfigurationArgs(
                encryption_configuration={
                    "encryptionOption": "SSE_KMS",
                    "kms_key_arn": test_key.arn,
                },
            ),
        ))
        hoge_database = aws.athena.Database("hogeDatabase",
            name="users",
            bucket=hoge_bucket.id)
        foo = aws.athena.NamedQuery("foo",
            workgroup=test_workgroup.id,
            database=hoge_database.name,
            query=hoge_database.name.apply(lambda name: f"SELECT * FROM {name} limit 10;"))
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] database: The database to which the query belongs.
        :param pulumi.Input[str] description: A brief explanation of the query. Maximum length of 1024.
        :param pulumi.Input[str] name: The plain language name for the query. Maximum length of 128.
        :param pulumi.Input[str] query: The text of the query itself. In other words, all query statements. Maximum length of 262144.
        :param pulumi.Input[str] workgroup: The workgroup to which the query belongs. Defaults to `primary`
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

            if database is None:
                raise TypeError("Missing required property 'database'")
            __props__['database'] = database
            __props__['description'] = description
            __props__['name'] = name
            if query is None:
                raise TypeError("Missing required property 'query'")
            __props__['query'] = query
            __props__['workgroup'] = workgroup
        super(NamedQuery, __self__).__init__(
            'aws:athena/namedQuery:NamedQuery',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            database: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            query: Optional[pulumi.Input[str]] = None,
            workgroup: Optional[pulumi.Input[str]] = None) -> 'NamedQuery':
        """
        Get an existing NamedQuery resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] database: The database to which the query belongs.
        :param pulumi.Input[str] description: A brief explanation of the query. Maximum length of 1024.
        :param pulumi.Input[str] name: The plain language name for the query. Maximum length of 128.
        :param pulumi.Input[str] query: The text of the query itself. In other words, all query statements. Maximum length of 262144.
        :param pulumi.Input[str] workgroup: The workgroup to which the query belongs. Defaults to `primary`
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["database"] = database
        __props__["description"] = description
        __props__["name"] = name
        __props__["query"] = query
        __props__["workgroup"] = workgroup
        return NamedQuery(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def database(self) -> pulumi.Output[str]:
        """
        The database to which the query belongs.
        """
        return pulumi.get(self, "database")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A brief explanation of the query. Maximum length of 1024.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The plain language name for the query. Maximum length of 128.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def query(self) -> pulumi.Output[str]:
        """
        The text of the query itself. In other words, all query statements. Maximum length of 262144.
        """
        return pulumi.get(self, "query")

    @property
    @pulumi.getter
    def workgroup(self) -> pulumi.Output[Optional[str]]:
        """
        The workgroup to which the query belongs. Defaults to `primary`
        """
        return pulumi.get(self, "workgroup")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

