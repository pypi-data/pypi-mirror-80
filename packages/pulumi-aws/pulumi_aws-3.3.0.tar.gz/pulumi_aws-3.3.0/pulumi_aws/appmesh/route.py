# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from . import outputs
from ._inputs import *

__all__ = ['Route']


class Route(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 mesh_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 spec: Optional[pulumi.Input[pulumi.InputType['RouteSpecArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 virtual_router_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides an AWS App Mesh route resource.

        ## Example Usage
        ### HTTP Routing

        ```python
        import pulumi
        import pulumi_aws as aws

        serviceb = aws.appmesh.Route("serviceb",
            mesh_name=aws_appmesh_mesh["simple"]["id"],
            virtual_router_name=aws_appmesh_virtual_router["serviceb"]["name"],
            spec=aws.appmesh.RouteSpecArgs(
                http_route=aws.appmesh.RouteSpecHttpRouteArgs(
                    match=aws.appmesh.RouteSpecHttpRouteMatchArgs(
                        prefix="/",
                    ),
                    action=aws.appmesh.RouteSpecHttpRouteActionArgs(
                        weighted_targets=[
                            aws.appmesh.RouteSpecHttpRouteActionWeightedTargetArgs(
                                virtual_node=aws_appmesh_virtual_node["serviceb1"]["name"],
                                weight=90,
                            ),
                            aws.appmesh.RouteSpecHttpRouteActionWeightedTargetArgs(
                                virtual_node=aws_appmesh_virtual_node["serviceb2"]["name"],
                                weight=10,
                            ),
                        ],
                    ),
                ),
            ))
        ```
        ### HTTP Header Routing

        ```python
        import pulumi
        import pulumi_aws as aws

        serviceb = aws.appmesh.Route("serviceb",
            mesh_name=aws_appmesh_mesh["simple"]["id"],
            virtual_router_name=aws_appmesh_virtual_router["serviceb"]["name"],
            spec=aws.appmesh.RouteSpecArgs(
                http_route=aws.appmesh.RouteSpecHttpRouteArgs(
                    match=aws.appmesh.RouteSpecHttpRouteMatchArgs(
                        method="POST",
                        prefix="/",
                        scheme="https",
                        headers=[aws.appmesh.RouteSpecHttpRouteMatchHeaderArgs(
                            name="clientRequestId",
                            match=aws.appmesh.RouteSpecHttpRouteMatchHeaderMatchArgs(
                                prefix="123",
                            ),
                        )],
                    ),
                    action=aws.appmesh.RouteSpecHttpRouteActionArgs(
                        weighted_targets=[aws.appmesh.RouteSpecHttpRouteActionWeightedTargetArgs(
                            virtual_node=aws_appmesh_virtual_node["serviceb"]["name"],
                            weight=100,
                        )],
                    ),
                ),
            ))
        ```
        ### TCP Routing

        ```python
        import pulumi
        import pulumi_aws as aws

        serviceb = aws.appmesh.Route("serviceb",
            mesh_name=aws_appmesh_mesh["simple"]["id"],
            virtual_router_name=aws_appmesh_virtual_router["serviceb"]["name"],
            spec=aws.appmesh.RouteSpecArgs(
                tcp_route=aws.appmesh.RouteSpecTcpRouteArgs(
                    action=aws.appmesh.RouteSpecTcpRouteActionArgs(
                        weighted_targets=[aws.appmesh.RouteSpecTcpRouteActionWeightedTargetArgs(
                            virtual_node=aws_appmesh_virtual_node["serviceb1"]["name"],
                            weight=100,
                        )],
                    ),
                ),
            ))
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] mesh_name: The name of the service mesh in which to create the route.
        :param pulumi.Input[str] name: The name to use for the route.
        :param pulumi.Input[pulumi.InputType['RouteSpecArgs']] spec: The route specification to apply.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource.
        :param pulumi.Input[str] virtual_router_name: The name of the virtual router in which to create the route.
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

            if mesh_name is None:
                raise TypeError("Missing required property 'mesh_name'")
            __props__['mesh_name'] = mesh_name
            __props__['name'] = name
            if spec is None:
                raise TypeError("Missing required property 'spec'")
            __props__['spec'] = spec
            __props__['tags'] = tags
            if virtual_router_name is None:
                raise TypeError("Missing required property 'virtual_router_name'")
            __props__['virtual_router_name'] = virtual_router_name
            __props__['arn'] = None
            __props__['created_date'] = None
            __props__['last_updated_date'] = None
        super(Route, __self__).__init__(
            'aws:appmesh/route:Route',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            created_date: Optional[pulumi.Input[str]] = None,
            last_updated_date: Optional[pulumi.Input[str]] = None,
            mesh_name: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            spec: Optional[pulumi.Input[pulumi.InputType['RouteSpecArgs']]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            virtual_router_name: Optional[pulumi.Input[str]] = None) -> 'Route':
        """
        Get an existing Route resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the route.
        :param pulumi.Input[str] created_date: The creation date of the route.
        :param pulumi.Input[str] last_updated_date: The last update date of the route.
        :param pulumi.Input[str] mesh_name: The name of the service mesh in which to create the route.
        :param pulumi.Input[str] name: The name to use for the route.
        :param pulumi.Input[pulumi.InputType['RouteSpecArgs']] spec: The route specification to apply.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource.
        :param pulumi.Input[str] virtual_router_name: The name of the virtual router in which to create the route.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["created_date"] = created_date
        __props__["last_updated_date"] = last_updated_date
        __props__["mesh_name"] = mesh_name
        __props__["name"] = name
        __props__["spec"] = spec
        __props__["tags"] = tags
        __props__["virtual_router_name"] = virtual_router_name
        return Route(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the route.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="createdDate")
    def created_date(self) -> pulumi.Output[str]:
        """
        The creation date of the route.
        """
        return pulumi.get(self, "created_date")

    @property
    @pulumi.getter(name="lastUpdatedDate")
    def last_updated_date(self) -> pulumi.Output[str]:
        """
        The last update date of the route.
        """
        return pulumi.get(self, "last_updated_date")

    @property
    @pulumi.getter(name="meshName")
    def mesh_name(self) -> pulumi.Output[str]:
        """
        The name of the service mesh in which to create the route.
        """
        return pulumi.get(self, "mesh_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name to use for the route.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def spec(self) -> pulumi.Output['outputs.RouteSpec']:
        """
        The route specification to apply.
        """
        return pulumi.get(self, "spec")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="virtualRouterName")
    def virtual_router_name(self) -> pulumi.Output[str]:
        """
        The name of the virtual router in which to create the route.
        """
        return pulumi.get(self, "virtual_router_name")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

