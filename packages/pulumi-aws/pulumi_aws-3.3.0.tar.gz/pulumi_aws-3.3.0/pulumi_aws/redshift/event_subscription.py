# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['EventSubscription']


class EventSubscription(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 event_categories: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 severity: Optional[pulumi.Input[str]] = None,
                 sns_topic_arn: Optional[pulumi.Input[str]] = None,
                 source_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 source_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides a Redshift event subscription resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        default_cluster = aws.redshift.Cluster("defaultCluster",
            cluster_identifier="default",
            database_name="default")
        # ...
        default_topic = aws.sns.Topic("defaultTopic")
        default_event_subscription = aws.redshift.EventSubscription("defaultEventSubscription",
            sns_topic_arn=default_topic.arn,
            source_type="cluster",
            source_ids=[default_cluster.id],
            severity="INFO",
            event_categories=[
                "configuration",
                "management",
                "monitoring",
                "security",
            ],
            tags={
                "Name": "default",
            })
        ```
        ## Attributes

        The following additional atttributes are provided:

        * `arn` - Amazon Resource Name (ARN) of the Redshift event notification subscription
        * `id` - The name of the Redshift event notification subscription
        * `customer_aws_id` - The AWS customer account associated with the Redshift event notification subscription

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] enabled: A boolean flag to enable/disable the subscription. Defaults to true.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] event_categories: A list of event categories for a SourceType that you want to subscribe to. See https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-event-notifications.html or run `aws redshift describe-event-categories`.
        :param pulumi.Input[str] name: The name of the Redshift event subscription.
        :param pulumi.Input[str] severity: The event severity to be published by the notification subscription. Valid options are `INFO` or `ERROR`.
        :param pulumi.Input[str] sns_topic_arn: The ARN of the SNS topic to send events to.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] source_ids: A list of identifiers of the event sources for which events will be returned. If not specified, then all sources are included in the response. If specified, a source_type must also be specified.
        :param pulumi.Input[str] source_type: The type of source that will be generating the events. Valid options are `cluster`, `cluster-parameter-group`, `cluster-security-group`, or `cluster-snapshot`. If not set, all sources will be subscribed to.
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

            __props__['enabled'] = enabled
            __props__['event_categories'] = event_categories
            __props__['name'] = name
            __props__['severity'] = severity
            if sns_topic_arn is None:
                raise TypeError("Missing required property 'sns_topic_arn'")
            __props__['sns_topic_arn'] = sns_topic_arn
            __props__['source_ids'] = source_ids
            __props__['source_type'] = source_type
            __props__['tags'] = tags
            __props__['arn'] = None
            __props__['customer_aws_id'] = None
            __props__['status'] = None
        super(EventSubscription, __self__).__init__(
            'aws:redshift/eventSubscription:EventSubscription',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            customer_aws_id: Optional[pulumi.Input[str]] = None,
            enabled: Optional[pulumi.Input[bool]] = None,
            event_categories: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            severity: Optional[pulumi.Input[str]] = None,
            sns_topic_arn: Optional[pulumi.Input[str]] = None,
            source_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            source_type: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'EventSubscription':
        """
        Get an existing EventSubscription resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] enabled: A boolean flag to enable/disable the subscription. Defaults to true.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] event_categories: A list of event categories for a SourceType that you want to subscribe to. See https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-event-notifications.html or run `aws redshift describe-event-categories`.
        :param pulumi.Input[str] name: The name of the Redshift event subscription.
        :param pulumi.Input[str] severity: The event severity to be published by the notification subscription. Valid options are `INFO` or `ERROR`.
        :param pulumi.Input[str] sns_topic_arn: The ARN of the SNS topic to send events to.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] source_ids: A list of identifiers of the event sources for which events will be returned. If not specified, then all sources are included in the response. If specified, a source_type must also be specified.
        :param pulumi.Input[str] source_type: The type of source that will be generating the events. Valid options are `cluster`, `cluster-parameter-group`, `cluster-security-group`, or `cluster-snapshot`. If not set, all sources will be subscribed to.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["customer_aws_id"] = customer_aws_id
        __props__["enabled"] = enabled
        __props__["event_categories"] = event_categories
        __props__["name"] = name
        __props__["severity"] = severity
        __props__["sns_topic_arn"] = sns_topic_arn
        __props__["source_ids"] = source_ids
        __props__["source_type"] = source_type
        __props__["status"] = status
        __props__["tags"] = tags
        return EventSubscription(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="customerAwsId")
    def customer_aws_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "customer_aws_id")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        A boolean flag to enable/disable the subscription. Defaults to true.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="eventCategories")
    def event_categories(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A list of event categories for a SourceType that you want to subscribe to. See https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-event-notifications.html or run `aws redshift describe-event-categories`.
        """
        return pulumi.get(self, "event_categories")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the Redshift event subscription.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def severity(self) -> pulumi.Output[Optional[str]]:
        """
        The event severity to be published by the notification subscription. Valid options are `INFO` or `ERROR`.
        """
        return pulumi.get(self, "severity")

    @property
    @pulumi.getter(name="snsTopicArn")
    def sns_topic_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the SNS topic to send events to.
        """
        return pulumi.get(self, "sns_topic_arn")

    @property
    @pulumi.getter(name="sourceIds")
    def source_ids(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A list of identifiers of the event sources for which events will be returned. If not specified, then all sources are included in the response. If specified, a source_type must also be specified.
        """
        return pulumi.get(self, "source_ids")

    @property
    @pulumi.getter(name="sourceType")
    def source_type(self) -> pulumi.Output[Optional[str]]:
        """
        The type of source that will be generating the events. Valid options are `cluster`, `cluster-parameter-group`, `cluster-security-group`, or `cluster-snapshot`. If not set, all sources will be subscribed to.
        """
        return pulumi.get(self, "source_type")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        return pulumi.get(self, "status")

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

