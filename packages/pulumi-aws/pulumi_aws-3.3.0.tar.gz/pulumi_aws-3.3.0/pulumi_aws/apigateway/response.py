# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['Response']


class Response(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 response_parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 response_templates: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 response_type: Optional[pulumi.Input[str]] = None,
                 rest_api_id: Optional[pulumi.Input[str]] = None,
                 status_code: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides an API Gateway Gateway Response for a REST API Gateway.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        main = aws.apigateway.RestApi("main")
        test = aws.apigateway.Response("test",
            rest_api_id=main.id,
            status_code="401",
            response_type="UNAUTHORIZED",
            response_templates={
                "application/json": "{'message':$context.error.messageString}",
            },
            response_parameters={
                "gatewayresponse.header.Authorization": "'Basic'",
            })
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] response_parameters: A map specifying the parameters (paths, query strings and headers) of the Gateway Response.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] response_templates: A map specifying the templates used to transform the response body.
        :param pulumi.Input[str] response_type: The response type of the associated GatewayResponse.
        :param pulumi.Input[str] rest_api_id: The string identifier of the associated REST API.
        :param pulumi.Input[str] status_code: The HTTP status code of the Gateway Response.
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

            __props__['response_parameters'] = response_parameters
            __props__['response_templates'] = response_templates
            if response_type is None:
                raise TypeError("Missing required property 'response_type'")
            __props__['response_type'] = response_type
            if rest_api_id is None:
                raise TypeError("Missing required property 'rest_api_id'")
            __props__['rest_api_id'] = rest_api_id
            __props__['status_code'] = status_code
        super(Response, __self__).__init__(
            'aws:apigateway/response:Response',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            response_parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            response_templates: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            response_type: Optional[pulumi.Input[str]] = None,
            rest_api_id: Optional[pulumi.Input[str]] = None,
            status_code: Optional[pulumi.Input[str]] = None) -> 'Response':
        """
        Get an existing Response resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] response_parameters: A map specifying the parameters (paths, query strings and headers) of the Gateway Response.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] response_templates: A map specifying the templates used to transform the response body.
        :param pulumi.Input[str] response_type: The response type of the associated GatewayResponse.
        :param pulumi.Input[str] rest_api_id: The string identifier of the associated REST API.
        :param pulumi.Input[str] status_code: The HTTP status code of the Gateway Response.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["response_parameters"] = response_parameters
        __props__["response_templates"] = response_templates
        __props__["response_type"] = response_type
        __props__["rest_api_id"] = rest_api_id
        __props__["status_code"] = status_code
        return Response(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="responseParameters")
    def response_parameters(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map specifying the parameters (paths, query strings and headers) of the Gateway Response.
        """
        return pulumi.get(self, "response_parameters")

    @property
    @pulumi.getter(name="responseTemplates")
    def response_templates(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map specifying the templates used to transform the response body.
        """
        return pulumi.get(self, "response_templates")

    @property
    @pulumi.getter(name="responseType")
    def response_type(self) -> pulumi.Output[str]:
        """
        The response type of the associated GatewayResponse.
        """
        return pulumi.get(self, "response_type")

    @property
    @pulumi.getter(name="restApiId")
    def rest_api_id(self) -> pulumi.Output[str]:
        """
        The string identifier of the associated REST API.
        """
        return pulumi.get(self, "rest_api_id")

    @property
    @pulumi.getter(name="statusCode")
    def status_code(self) -> pulumi.Output[Optional[str]]:
        """
        The HTTP status code of the Gateway Response.
        """
        return pulumi.get(self, "status_code")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

