"""
## AWS CDK Assets

<!--BEGIN STABILITY BANNER-->---


![Deprecated](https://img.shields.io/badge/deprecated-critical.svg?style=for-the-badge)

> This API may emit warnings. Backward compatibility is not guaranteed.

---
<!--END STABILITY BANNER-->

All types moved to @aws-cdk/core.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.core


@jsii.data_type(
    jsii_type="@aws-cdk/assets.CopyOptions",
    jsii_struct_bases=[],
    name_mapping={"exclude": "exclude", "follow": "follow"},
)
class CopyOptions:
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.List[builtins.str]] = None,
        follow: typing.Optional["FollowMode"] = None,
    ) -> None:
        """Obtains applied when copying directories into the staging location.

        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never

        deprecated
        :deprecated: see ``core.CopyOptions``

        stability
        :stability: deprecated
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if exclude is not None:
            self._values["exclude"] = exclude
        if follow is not None:
            self._values["follow"] = follow

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        """Glob patterns to exclude from the copy.

        default
        :default: nothing is excluded

        stability
        :stability: deprecated
        """
        result = self._values.get("exclude")
        return result

    @builtins.property
    def follow(self) -> typing.Optional["FollowMode"]:
        """A strategy for how to handle symlinks.

        default
        :default: Never

        stability
        :stability: deprecated
        """
        result = self._values.get("follow")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CopyOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/assets.FingerprintOptions",
    jsii_struct_bases=[CopyOptions],
    name_mapping={"exclude": "exclude", "follow": "follow", "extra_hash": "extraHash"},
)
class FingerprintOptions(CopyOptions):
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.List[builtins.str]] = None,
        follow: typing.Optional["FollowMode"] = None,
        extra_hash: typing.Optional[builtins.str] = None,
    ) -> None:
        """Options related to calculating source hash.

        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never
        :param extra_hash: Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content

        deprecated
        :deprecated: see ``core.FingerprintOptions``

        stability
        :stability: deprecated
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if exclude is not None:
            self._values["exclude"] = exclude
        if follow is not None:
            self._values["follow"] = follow
        if extra_hash is not None:
            self._values["extra_hash"] = extra_hash

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        """Glob patterns to exclude from the copy.

        default
        :default: nothing is excluded

        stability
        :stability: deprecated
        """
        result = self._values.get("exclude")
        return result

    @builtins.property
    def follow(self) -> typing.Optional["FollowMode"]:
        """A strategy for how to handle symlinks.

        default
        :default: Never

        stability
        :stability: deprecated
        """
        result = self._values.get("follow")
        return result

    @builtins.property
    def extra_hash(self) -> typing.Optional[builtins.str]:
        """Extra information to encode into the fingerprint (e.g. build instructions and other inputs).

        default
        :default: - hash is only based on source content

        stability
        :stability: deprecated
        """
        result = self._values.get("extra_hash")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FingerprintOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/assets.FollowMode")
class FollowMode(enum.Enum):
    """Symlink follow mode.

    deprecated
    :deprecated: see ``core.SymlinkFollowMode``

    stability
    :stability: deprecated
    """

    NEVER = "NEVER"
    """Never follow symlinks.

    stability
    :stability: deprecated
    """
    ALWAYS = "ALWAYS"
    """Materialize all symlinks, whether they are internal or external to the source directory.

    stability
    :stability: deprecated
    """
    EXTERNAL = "EXTERNAL"
    """Only follows symlinks that are external to the source directory.

    stability
    :stability: deprecated
    """
    BLOCK_EXTERNAL = "BLOCK_EXTERNAL"
    """Forbids source from having any symlinks pointing outside of the source tree.

    This is the safest mode of operation as it ensures that copy operations
    won't materialize files from the user's file system. Internal symlinks are
    not followed.

    If the copy operation runs into an external symlink, it will fail.

    stability
    :stability: deprecated
    """


@jsii.interface(jsii_type="@aws-cdk/assets.IAsset")
class IAsset(typing_extensions.Protocol):
    """Common interface for all assets.

    deprecated
    :deprecated: use ``core.IAsset``

    stability
    :stability: deprecated
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IAssetProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sourceHash")
    def source_hash(self) -> builtins.str:
        """A hash of the source of this asset, which is available at construction time.

        As this is a plain
        string, it can be used in construct IDs in order to enforce creation of a new resource when
        the content hash has changed.

        stability
        :stability: deprecated
        """
        ...


class _IAssetProxy:
    """Common interface for all assets.

    deprecated
    :deprecated: use ``core.IAsset``

    stability
    :stability: deprecated
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/assets.IAsset"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sourceHash")
    def source_hash(self) -> builtins.str:
        """A hash of the source of this asset, which is available at construction time.

        As this is a plain
        string, it can be used in construct IDs in order to enforce creation of a new resource when
        the content hash has changed.

        stability
        :stability: deprecated
        """
        return jsii.get(self, "sourceHash")


class Staging(
    aws_cdk.core.AssetStaging,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/assets.Staging",
):
    """Deprecated.

    deprecated
    :deprecated: use ``core.AssetStaging``

    stability
    :stability: deprecated
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        source_path: builtins.str,
        extra_hash: typing.Optional[builtins.str] = None,
        exclude: typing.Optional[typing.List[builtins.str]] = None,
        follow: typing.Optional["FollowMode"] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param source_path: Local file or directory to stage.
        :param extra_hash: Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never

        stability
        :stability: deprecated
        """
        props = StagingProps(
            source_path=source_path,
            extra_hash=extra_hash,
            exclude=exclude,
            follow=follow,
        )

        jsii.create(Staging, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@aws-cdk/assets.StagingProps",
    jsii_struct_bases=[FingerprintOptions],
    name_mapping={
        "exclude": "exclude",
        "follow": "follow",
        "extra_hash": "extraHash",
        "source_path": "sourcePath",
    },
)
class StagingProps(FingerprintOptions):
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.List[builtins.str]] = None,
        follow: typing.Optional["FollowMode"] = None,
        extra_hash: typing.Optional[builtins.str] = None,
        source_path: builtins.str,
    ) -> None:
        """Deprecated.

        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never
        :param extra_hash: Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param source_path: Local file or directory to stage.

        deprecated
        :deprecated: use ``core.AssetStagingProps``

        stability
        :stability: deprecated
        """
        self._values: typing.Dict[str, typing.Any] = {
            "source_path": source_path,
        }
        if exclude is not None:
            self._values["exclude"] = exclude
        if follow is not None:
            self._values["follow"] = follow
        if extra_hash is not None:
            self._values["extra_hash"] = extra_hash

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        """Glob patterns to exclude from the copy.

        default
        :default: nothing is excluded

        stability
        :stability: deprecated
        """
        result = self._values.get("exclude")
        return result

    @builtins.property
    def follow(self) -> typing.Optional["FollowMode"]:
        """A strategy for how to handle symlinks.

        default
        :default: Never

        stability
        :stability: deprecated
        """
        result = self._values.get("follow")
        return result

    @builtins.property
    def extra_hash(self) -> typing.Optional[builtins.str]:
        """Extra information to encode into the fingerprint (e.g. build instructions and other inputs).

        default
        :default: - hash is only based on source content

        stability
        :stability: deprecated
        """
        result = self._values.get("extra_hash")
        return result

    @builtins.property
    def source_path(self) -> builtins.str:
        """Local file or directory to stage.

        stability
        :stability: deprecated
        """
        result = self._values.get("source_path")
        assert result is not None, "Required property 'source_path' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StagingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CopyOptions",
    "FingerprintOptions",
    "FollowMode",
    "IAsset",
    "Staging",
    "StagingProps",
]

publication.publish()
