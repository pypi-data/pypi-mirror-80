# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from . import outputs

__all__ = [
    'CertificateAuthorityCertificateAuthorityConfiguration',
    'CertificateAuthorityCertificateAuthorityConfigurationSubject',
    'CertificateAuthorityRevocationConfiguration',
    'CertificateAuthorityRevocationConfigurationCrlConfiguration',
    'GetCertificateAuthorityRevocationConfigurationResult',
    'GetCertificateAuthorityRevocationConfigurationCrlConfigurationResult',
]

@pulumi.output_type
class CertificateAuthorityCertificateAuthorityConfiguration(dict):
    def __init__(__self__, *,
                 key_algorithm: str,
                 signing_algorithm: str,
                 subject: 'outputs.CertificateAuthorityCertificateAuthorityConfigurationSubject'):
        """
        :param str key_algorithm: Type of the public key algorithm and size, in bits, of the key pair that your key pair creates when it issues a certificate. Valid values can be found in the [ACM PCA Documentation](https://docs.aws.amazon.com/acm-pca/latest/APIReference/API_CertificateAuthorityConfiguration.html).
        :param str signing_algorithm: Name of the algorithm your private CA uses to sign certificate requests. Valid values can be found in the [ACM PCA Documentation](https://docs.aws.amazon.com/acm-pca/latest/APIReference/API_CertificateAuthorityConfiguration.html).
        :param 'CertificateAuthorityCertificateAuthorityConfigurationSubjectArgs' subject: Nested argument that contains X.500 distinguished name information. At least one nested attribute must be specified.
        """
        pulumi.set(__self__, "key_algorithm", key_algorithm)
        pulumi.set(__self__, "signing_algorithm", signing_algorithm)
        pulumi.set(__self__, "subject", subject)

    @property
    @pulumi.getter(name="keyAlgorithm")
    def key_algorithm(self) -> str:
        """
        Type of the public key algorithm and size, in bits, of the key pair that your key pair creates when it issues a certificate. Valid values can be found in the [ACM PCA Documentation](https://docs.aws.amazon.com/acm-pca/latest/APIReference/API_CertificateAuthorityConfiguration.html).
        """
        return pulumi.get(self, "key_algorithm")

    @property
    @pulumi.getter(name="signingAlgorithm")
    def signing_algorithm(self) -> str:
        """
        Name of the algorithm your private CA uses to sign certificate requests. Valid values can be found in the [ACM PCA Documentation](https://docs.aws.amazon.com/acm-pca/latest/APIReference/API_CertificateAuthorityConfiguration.html).
        """
        return pulumi.get(self, "signing_algorithm")

    @property
    @pulumi.getter
    def subject(self) -> 'outputs.CertificateAuthorityCertificateAuthorityConfigurationSubject':
        """
        Nested argument that contains X.500 distinguished name information. At least one nested attribute must be specified.
        """
        return pulumi.get(self, "subject")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class CertificateAuthorityCertificateAuthorityConfigurationSubject(dict):
    def __init__(__self__, *,
                 common_name: Optional[str] = None,
                 country: Optional[str] = None,
                 distinguished_name_qualifier: Optional[str] = None,
                 generation_qualifier: Optional[str] = None,
                 given_name: Optional[str] = None,
                 initials: Optional[str] = None,
                 locality: Optional[str] = None,
                 organization: Optional[str] = None,
                 organizational_unit: Optional[str] = None,
                 pseudonym: Optional[str] = None,
                 state: Optional[str] = None,
                 surname: Optional[str] = None,
                 title: Optional[str] = None):
        """
        :param str common_name: Fully qualified domain name (FQDN) associated with the certificate subject.
        :param str country: Two digit code that specifies the country in which the certificate subject located.
        :param str distinguished_name_qualifier: Disambiguating information for the certificate subject.
        :param str generation_qualifier: Typically a qualifier appended to the name of an individual. Examples include Jr. for junior, Sr. for senior, and III for third.
        :param str given_name: First name.
        :param str initials: Concatenation that typically contains the first letter of the `given_name`, the first letter of the middle name if one exists, and the first letter of the `surname`.
        :param str locality: The locality (such as a city or town) in which the certificate subject is located.
        :param str organization: Legal name of the organization with which the certificate subject is affiliated.
        :param str organizational_unit: A subdivision or unit of the organization (such as sales or finance) with which the certificate subject is affiliated.
        :param str pseudonym: Typically a shortened version of a longer `given_name`. For example, Jonathan is often shortened to John. Elizabeth is often shortened to Beth, Liz, or Eliza.
        :param str state: State in which the subject of the certificate is located.
        :param str surname: Family name. In the US and the UK for example, the surname of an individual is ordered last. In Asian cultures the surname is typically ordered first.
        :param str title: A title such as Mr. or Ms. which is pre-pended to the name to refer formally to the certificate subject.
        """
        if common_name is not None:
            pulumi.set(__self__, "common_name", common_name)
        if country is not None:
            pulumi.set(__self__, "country", country)
        if distinguished_name_qualifier is not None:
            pulumi.set(__self__, "distinguished_name_qualifier", distinguished_name_qualifier)
        if generation_qualifier is not None:
            pulumi.set(__self__, "generation_qualifier", generation_qualifier)
        if given_name is not None:
            pulumi.set(__self__, "given_name", given_name)
        if initials is not None:
            pulumi.set(__self__, "initials", initials)
        if locality is not None:
            pulumi.set(__self__, "locality", locality)
        if organization is not None:
            pulumi.set(__self__, "organization", organization)
        if organizational_unit is not None:
            pulumi.set(__self__, "organizational_unit", organizational_unit)
        if pseudonym is not None:
            pulumi.set(__self__, "pseudonym", pseudonym)
        if state is not None:
            pulumi.set(__self__, "state", state)
        if surname is not None:
            pulumi.set(__self__, "surname", surname)
        if title is not None:
            pulumi.set(__self__, "title", title)

    @property
    @pulumi.getter(name="commonName")
    def common_name(self) -> Optional[str]:
        """
        Fully qualified domain name (FQDN) associated with the certificate subject.
        """
        return pulumi.get(self, "common_name")

    @property
    @pulumi.getter
    def country(self) -> Optional[str]:
        """
        Two digit code that specifies the country in which the certificate subject located.
        """
        return pulumi.get(self, "country")

    @property
    @pulumi.getter(name="distinguishedNameQualifier")
    def distinguished_name_qualifier(self) -> Optional[str]:
        """
        Disambiguating information for the certificate subject.
        """
        return pulumi.get(self, "distinguished_name_qualifier")

    @property
    @pulumi.getter(name="generationQualifier")
    def generation_qualifier(self) -> Optional[str]:
        """
        Typically a qualifier appended to the name of an individual. Examples include Jr. for junior, Sr. for senior, and III for third.
        """
        return pulumi.get(self, "generation_qualifier")

    @property
    @pulumi.getter(name="givenName")
    def given_name(self) -> Optional[str]:
        """
        First name.
        """
        return pulumi.get(self, "given_name")

    @property
    @pulumi.getter
    def initials(self) -> Optional[str]:
        """
        Concatenation that typically contains the first letter of the `given_name`, the first letter of the middle name if one exists, and the first letter of the `surname`.
        """
        return pulumi.get(self, "initials")

    @property
    @pulumi.getter
    def locality(self) -> Optional[str]:
        """
        The locality (such as a city or town) in which the certificate subject is located.
        """
        return pulumi.get(self, "locality")

    @property
    @pulumi.getter
    def organization(self) -> Optional[str]:
        """
        Legal name of the organization with which the certificate subject is affiliated.
        """
        return pulumi.get(self, "organization")

    @property
    @pulumi.getter(name="organizationalUnit")
    def organizational_unit(self) -> Optional[str]:
        """
        A subdivision or unit of the organization (such as sales or finance) with which the certificate subject is affiliated.
        """
        return pulumi.get(self, "organizational_unit")

    @property
    @pulumi.getter
    def pseudonym(self) -> Optional[str]:
        """
        Typically a shortened version of a longer `given_name`. For example, Jonathan is often shortened to John. Elizabeth is often shortened to Beth, Liz, or Eliza.
        """
        return pulumi.get(self, "pseudonym")

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        State in which the subject of the certificate is located.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def surname(self) -> Optional[str]:
        """
        Family name. In the US and the UK for example, the surname of an individual is ordered last. In Asian cultures the surname is typically ordered first.
        """
        return pulumi.get(self, "surname")

    @property
    @pulumi.getter
    def title(self) -> Optional[str]:
        """
        A title such as Mr. or Ms. which is pre-pended to the name to refer formally to the certificate subject.
        """
        return pulumi.get(self, "title")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class CertificateAuthorityRevocationConfiguration(dict):
    def __init__(__self__, *,
                 crl_configuration: Optional['outputs.CertificateAuthorityRevocationConfigurationCrlConfiguration'] = None):
        """
        :param 'CertificateAuthorityRevocationConfigurationCrlConfigurationArgs' crl_configuration: Nested argument containing configuration of the certificate revocation list (CRL), if any, maintained by the certificate authority. Defined below.
        """
        if crl_configuration is not None:
            pulumi.set(__self__, "crl_configuration", crl_configuration)

    @property
    @pulumi.getter(name="crlConfiguration")
    def crl_configuration(self) -> Optional['outputs.CertificateAuthorityRevocationConfigurationCrlConfiguration']:
        """
        Nested argument containing configuration of the certificate revocation list (CRL), if any, maintained by the certificate authority. Defined below.
        """
        return pulumi.get(self, "crl_configuration")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class CertificateAuthorityRevocationConfigurationCrlConfiguration(dict):
    def __init__(__self__, *,
                 expiration_in_days: int,
                 custom_cname: Optional[str] = None,
                 enabled: Optional[bool] = None,
                 s3_bucket_name: Optional[str] = None):
        """
        :param int expiration_in_days: Number of days until a certificate expires. Must be between 1 and 5000.
        :param str custom_cname: Name inserted into the certificate CRL Distribution Points extension that enables the use of an alias for the CRL distribution point. Use this value if you don't want the name of your S3 bucket to be public.
        :param bool enabled: Boolean value that specifies whether certificate revocation lists (CRLs) are enabled. Defaults to `false`.
        :param str s3_bucket_name: Name of the S3 bucket that contains the CRL. If you do not provide a value for the `custom_cname` argument, the name of your S3 bucket is placed into the CRL Distribution Points extension of the issued certificate. You must specify a bucket policy that allows ACM PCA to write the CRL to your bucket.
        """
        pulumi.set(__self__, "expiration_in_days", expiration_in_days)
        if custom_cname is not None:
            pulumi.set(__self__, "custom_cname", custom_cname)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if s3_bucket_name is not None:
            pulumi.set(__self__, "s3_bucket_name", s3_bucket_name)

    @property
    @pulumi.getter(name="expirationInDays")
    def expiration_in_days(self) -> int:
        """
        Number of days until a certificate expires. Must be between 1 and 5000.
        """
        return pulumi.get(self, "expiration_in_days")

    @property
    @pulumi.getter(name="customCname")
    def custom_cname(self) -> Optional[str]:
        """
        Name inserted into the certificate CRL Distribution Points extension that enables the use of an alias for the CRL distribution point. Use this value if you don't want the name of your S3 bucket to be public.
        """
        return pulumi.get(self, "custom_cname")

    @property
    @pulumi.getter
    def enabled(self) -> Optional[bool]:
        """
        Boolean value that specifies whether certificate revocation lists (CRLs) are enabled. Defaults to `false`.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="s3BucketName")
    def s3_bucket_name(self) -> Optional[str]:
        """
        Name of the S3 bucket that contains the CRL. If you do not provide a value for the `custom_cname` argument, the name of your S3 bucket is placed into the CRL Distribution Points extension of the issued certificate. You must specify a bucket policy that allows ACM PCA to write the CRL to your bucket.
        """
        return pulumi.get(self, "s3_bucket_name")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class GetCertificateAuthorityRevocationConfigurationResult(dict):
    def __init__(__self__, *,
                 crl_configurations: Sequence['outputs.GetCertificateAuthorityRevocationConfigurationCrlConfigurationResult']):
        pulumi.set(__self__, "crl_configurations", crl_configurations)

    @property
    @pulumi.getter(name="crlConfigurations")
    def crl_configurations(self) -> Sequence['outputs.GetCertificateAuthorityRevocationConfigurationCrlConfigurationResult']:
        return pulumi.get(self, "crl_configurations")


@pulumi.output_type
class GetCertificateAuthorityRevocationConfigurationCrlConfigurationResult(dict):
    def __init__(__self__, *,
                 custom_cname: str,
                 enabled: bool,
                 expiration_in_days: int,
                 s3_bucket_name: str):
        pulumi.set(__self__, "custom_cname", custom_cname)
        pulumi.set(__self__, "enabled", enabled)
        pulumi.set(__self__, "expiration_in_days", expiration_in_days)
        pulumi.set(__self__, "s3_bucket_name", s3_bucket_name)

    @property
    @pulumi.getter(name="customCname")
    def custom_cname(self) -> str:
        return pulumi.get(self, "custom_cname")

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="expirationInDays")
    def expiration_in_days(self) -> int:
        return pulumi.get(self, "expiration_in_days")

    @property
    @pulumi.getter(name="s3BucketName")
    def s3_bucket_name(self) -> str:
        return pulumi.get(self, "s3_bucket_name")


