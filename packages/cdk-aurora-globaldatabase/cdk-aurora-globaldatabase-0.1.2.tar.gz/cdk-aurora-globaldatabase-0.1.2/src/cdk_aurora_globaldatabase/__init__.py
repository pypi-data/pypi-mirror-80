"""
[![NPM version](https://badge.fury.io/js/cdk-aurora-globaldatabase.svg)](https://badge.fury.io/js/cdk-aurora-globaldatabase)
[![PyPI version](https://badge.fury.io/py/cdk-aurora-globaldatabase.svg)](https://badge.fury.io/py/cdk-aurora-globaldatabase)
![Release](https://github.com/guan840912/cdk-aurora-globaldatabase/workflows/Release/badge.svg)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/cdk-aurora-globaldatabase?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/cdk-aurora-globaldatabase?label=pypi&color=blue)

# cdk-aurora-globaldatabase

`cdk-aurora-globaldatabase` is an AWS CDK construct library that allows you to create [Amazon Aurora Global Databases](https://aws.amazon.com/rds/aurora/global-database/) with AWS CDK in Typescript or Python.

# Why

**Amazon Aurora Global Databases** is designed for multi-regional Amazon Aurora Database clusters that span across different AWS regions. Due to the lack of native cloudformation support, it has been very challenging to build with cloudformation or AWS CDK with the upstream `aws-rds` construct.

`cdk-aurora-globaldatabase` aims to offload the heavy-lifting and helps you provision and deploy cross-regional **Amazon Aurora Global Databases** simply with just a few CDK statements.

## Now Try It !!!

# Sample for Mysql

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from ..index import GolbalAuroraRDSMaster, InstanceTypeEnum, GolbalAuroraRDSSlaveInfra
from aws_cdk.core import App, Stack, CfnOutput
import aws_cdk.aws_ec2 as ec2
# new app .
mock_app = App()

# setting two region env config .
env_singapro = {"account": process.env.CDK_DEFAULT_ACCOUNT, "region": "ap-southeast-1"}
env_tokyo = {"account": process.env.CDK_DEFAULT_ACCOUNT, "region": "ap-northeast-1"}

# create stack main .
stack_m = Stack(mock_app, "testing-stackM", env=env_tokyo)
vpc_public = ec2.Vpc(stack_m, "defaultVpc",
    nat_gateways=0,
    max_azs=3,
    subnet_configuration=[SubnetConfiguration(
        cidr_mask=26,
        name="masterVPC2",
        subnet_type=ec2.SubnetType.PUBLIC
    )]
)
globaldb_m = GolbalAuroraRDSMaster(stack_m, "golbalAuroraRDSMaster",
    instance_type=InstanceTypeEnum.R5_LARGE,
    vpc=vpc_public,
    rds_password="1qaz2wsx"
)
globaldb_m.rds_cluster.connections.allow_default_port_from(ec2.Peer.ipv4(f"{process.env.MYIP}/32"))

# create stack slave infra or you can give your subnet group.
stack_s = Stack(mock_app, "testing-stackS", env=env_singapro)
vpc_public2 = ec2.Vpc(stack_s, "defaultVpc2",
    nat_gateways=0,
    max_azs=3,
    subnet_configuration=[SubnetConfiguration(
        cidr_mask=26,
        name="secondVPC2",
        subnet_type=ec2.SubnetType.PUBLIC
    )]
)
globaldb_s = GolbalAuroraRDSSlaveInfra(stack_s, "slaveregion", vpc=vpc_public2, subnet_type=ec2.SubnetType.PUBLIC)

# so we need to wait stack slave created first .
stack_m.add_dependency(stack_s)

CfnOutput(stack_m, "password", value=globaldb_m.rds_password)
# add second region cluster
globaldb_m.add_regional_cluster(stack_m, "addregionalrds",
    region="ap-southeast-1",
    db_subnet_group_name=globaldb_s.db_subnet_group.db_subnet_group_name
)
```

# Sample for Postgres

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from ..index import GolbalAuroraRDSMaster, InstanceTypeEnum, GolbalAuroraRDSSlaveInfra
from aws_cdk.core import App, Stack, CfnOutput
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_rds as _rds

mock_app = App()
env_singapro = {"account": process.env.CDK_DEFAULT_ACCOUNT, "region": "ap-southeast-1"}
env_tokyo = {"account": process.env.CDK_DEFAULT_ACCOUNT, "region": "ap-northeast-1"}

stack_m = Stack(mock_app, "testing-stackM", env=env_tokyo)
vpc_public = ec2.Vpc(stack_m, "defaultVpc",
    nat_gateways=0,
    max_azs=3,
    subnet_configuration=[SubnetConfiguration(
        cidr_mask=26,
        name="masterVPC2",
        subnet_type=ec2.SubnetType.PUBLIC
    )]
)

# Note if you use postgres , need to give the same value in engineVersion and  dbClusterpPG's engine .
globaldb_m = GolbalAuroraRDSMaster(stack_m, "golbalAuroraRDSMaster",
    instance_type=InstanceTypeEnum.R5_LARGE,
    vpc=vpc_public,
    rds_password="1qaz2wsx",
    engine_version=_rds.DatabaseClusterEngine.aurora_postgres(
        version=_rds.AuroraPostgresEngineVersion.VER_11_7
    ),
    db_clusterp_pG=_rds.ParameterGroup(stack_m, "dbClusterparametergroup",
        engine=_rds.DatabaseClusterEngine.aurora_postgres(
            version=_rds.AuroraPostgresEngineVersion.VER_11_7
        ),
        parameters={
            "rds.force_ssl": "1",
            "rds.log_retention_period": "10080",
            "auto_explain.log_min_duration": "5000",
            "auto_explain.log_verbose": "1",
            "timezone": "UTC+8",
            "shared_preload_libraries": "auto_explain,pg_stat_statements,pg_hint_plan,pgaudit",
            "log_connections": "1",
            "log_statement": "ddl",
            "log_disconnections": "1",
            "log_lock_waits": "1",
            "log_min_duration_statement": "5000",
            "log_rotation_age": "1440",
            "log_rotation_size": "102400",
            "random_page_cost": "1",
            "track_activity_query_size": "16384",
            "idle_in_transaction_session_timeout": "7200000"
        }
    )
)
globaldb_m.rds_cluster.connections.allow_default_port_from(ec2.Peer.ipv4(f"{process.env.MYIP}/32"))

stack_s = Stack(mock_app, "testing-stackS", env=env_singapro)
vpc_public2 = ec2.Vpc(stack_s, "defaultVpc2",
    nat_gateways=0,
    max_azs=3,
    subnet_configuration=[SubnetConfiguration(
        cidr_mask=26,
        name="secondVPC2",
        subnet_type=ec2.SubnetType.PUBLIC
    )]
)
globaldb_s = GolbalAuroraRDSSlaveInfra(stack_s, "slaveregion",
    vpc=vpc_public2, subnet_type=ec2.SubnetType.PUBLIC
)

stack_m.add_dependency(stack_s)

CfnOutput(stack_m, "password", value=globaldb_m.rds_password)
# add second region cluster
globaldb_m.add_regional_cluster(stack_m, "addregionalrds",
    region="ap-southeast-1",
    db_subnet_group_name=globaldb_s.db_subnet_group.db_subnet_group_name
)
```

### To deploy

```bash
cdk deploy
```

### To destroy

```bash
cdk destroy
```
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

import aws_cdk.aws_ec2
import aws_cdk.aws_rds
import aws_cdk.core


class GolbalAuroraRDSMaster(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aurora-globaldatabase.GolbalAuroraRDSMaster",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        db_clusterp_pg: typing.Optional[aws_cdk.aws_rds.IParameterGroup] = None,
        db_user_name: typing.Optional[builtins.str] = None,
        default_database_name: typing.Optional[builtins.str] = None,
        deletion_protection: typing.Optional[builtins.bool] = None,
        engine_version: typing.Optional[aws_cdk.aws_rds.IClusterEngine] = None,
        instance_type: typing.Optional["InstanceTypeEnum"] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        rds_password: typing.Optional[builtins.str] = None,
        storage_encrypted: typing.Optional[builtins.bool] = None,
        time_zone: typing.Optional["MySQLtimeZone"] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param db_clusterp_pg: RDS ParameterGroup. Default: - Aurora MySQL ParameterGroup
        :param db_user_name: RDS default Super User Name. Default: - sysadmin
        :param default_database_name: RDS default Database Name. Default: - globaldatabase
        :param deletion_protection: Global RDS Database Cluster Engine Deletion Protection Option . Default: - false
        :param engine_version: RDS Database Cluster Engine . Default: - rds.DatabaseClusterEngine.auroraMysql({version: rds.AuroraMysqlEngineVersion.VER_2_07_1,})
        :param instance_type: RDS Instance Type only can use r4 or r5 type see more https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html#aurora-global-database.limitations. Default: - r5.large
        :param parameters: RDS Parameters. Default: - {time_zone: 'UTC'}
        :param rds_password: return RDS Cluster password.
        :param storage_encrypted: Global RDS Database Cluster Engine Storage Encrypted Option . Default: - true
        :param time_zone: RDS time zone. Default: - MySQLtimeZone.UTC
        :param vpc: RDS default VPC. Default: - new VPC
        """
        props = GolbalAuroraRDSMasterProps(
            db_clusterp_pg=db_clusterp_pg,
            db_user_name=db_user_name,
            default_database_name=default_database_name,
            deletion_protection=deletion_protection,
            engine_version=engine_version,
            instance_type=instance_type,
            parameters=parameters,
            rds_password=rds_password,
            storage_encrypted=storage_encrypted,
            time_zone=time_zone,
            vpc=vpc,
        )

        jsii.create(GolbalAuroraRDSMaster, self, [scope, id, props])

    @jsii.member(jsii_name="addRegionalCluster")
    def add_regional_cluster(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        region: builtins.str,
        db_subnet_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param region: 
        :param db_subnet_group_name: 
        """
        options = RegionalOptions(
            region=region, db_subnet_group_name=db_subnet_group_name
        )

        return jsii.invoke(self, "addRegionalCluster", [scope, id, options])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clusterEngineVersion")
    def cluster_engine_version(self) -> builtins.str:
        """return RDS Cluster DB Engine Version."""
        return jsii.get(self, "clusterEngineVersion")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="dbClusterpPG")
    def db_clusterp_pg(self) -> aws_cdk.aws_rds.IParameterGroup:
        """return RDS Cluster ParameterGroup."""
        return jsii.get(self, "dbClusterpPG")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="engine")
    def engine(self) -> builtins.str:
        """return RDS Cluster DB Engine ."""
        return jsii.get(self, "engine")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> aws_cdk.aws_rds.IClusterEngine:
        """return RDS Cluster DB Engine Version."""
        return jsii.get(self, "engineVersion")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="globalClusterArn")
    def global_cluster_arn(self) -> builtins.str:
        """return Global RDS Cluster Resource ARN ."""
        return jsii.get(self, "globalClusterArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="globalClusterIdentifier")
    def global_cluster_identifier(self) -> builtins.str:
        """return Global RDS Cluster Identifier ."""
        return jsii.get(self, "globalClusterIdentifier")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="rdsCluster")
    def rds_cluster(self) -> aws_cdk.aws_rds.IDatabaseCluster:
        """return RDS Cluster."""
        return jsii.get(self, "rdsCluster")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="rdsClusterarn")
    def rds_clusterarn(self) -> builtins.str:
        """return RDS Cluster Resource ARN ."""
        return jsii.get(self, "rdsClusterarn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="rdsInstanceType")
    def rds_instance_type(self) -> "InstanceTypeEnum":
        """return Global RDS Cluster instance Type ."""
        return jsii.get(self, "rdsInstanceType")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="rdsIsPublic")
    def rds_is_public(self) -> aws_cdk.aws_ec2.SubnetType:
        """return RDS Cluster is Public ?"""
        return jsii.get(self, "rdsIsPublic")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="rdsPassword")
    def rds_password(self) -> builtins.str:
        """return RDS Cluster password."""
        return jsii.get(self, "rdsPassword")


@jsii.data_type(
    jsii_type="cdk-aurora-globaldatabase.GolbalAuroraRDSMasterProps",
    jsii_struct_bases=[],
    name_mapping={
        "db_clusterp_pg": "dbClusterpPG",
        "db_user_name": "dbUserName",
        "default_database_name": "defaultDatabaseName",
        "deletion_protection": "deletionProtection",
        "engine_version": "engineVersion",
        "instance_type": "instanceType",
        "parameters": "parameters",
        "rds_password": "rdsPassword",
        "storage_encrypted": "storageEncrypted",
        "time_zone": "timeZone",
        "vpc": "vpc",
    },
)
class GolbalAuroraRDSMasterProps:
    def __init__(
        self,
        *,
        db_clusterp_pg: typing.Optional[aws_cdk.aws_rds.IParameterGroup] = None,
        db_user_name: typing.Optional[builtins.str] = None,
        default_database_name: typing.Optional[builtins.str] = None,
        deletion_protection: typing.Optional[builtins.bool] = None,
        engine_version: typing.Optional[aws_cdk.aws_rds.IClusterEngine] = None,
        instance_type: typing.Optional["InstanceTypeEnum"] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        rds_password: typing.Optional[builtins.str] = None,
        storage_encrypted: typing.Optional[builtins.bool] = None,
        time_zone: typing.Optional["MySQLtimeZone"] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param db_clusterp_pg: RDS ParameterGroup. Default: - Aurora MySQL ParameterGroup
        :param db_user_name: RDS default Super User Name. Default: - sysadmin
        :param default_database_name: RDS default Database Name. Default: - globaldatabase
        :param deletion_protection: Global RDS Database Cluster Engine Deletion Protection Option . Default: - false
        :param engine_version: RDS Database Cluster Engine . Default: - rds.DatabaseClusterEngine.auroraMysql({version: rds.AuroraMysqlEngineVersion.VER_2_07_1,})
        :param instance_type: RDS Instance Type only can use r4 or r5 type see more https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html#aurora-global-database.limitations. Default: - r5.large
        :param parameters: RDS Parameters. Default: - {time_zone: 'UTC'}
        :param rds_password: return RDS Cluster password.
        :param storage_encrypted: Global RDS Database Cluster Engine Storage Encrypted Option . Default: - true
        :param time_zone: RDS time zone. Default: - MySQLtimeZone.UTC
        :param vpc: RDS default VPC. Default: - new VPC
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if db_clusterp_pg is not None:
            self._values["db_clusterp_pg"] = db_clusterp_pg
        if db_user_name is not None:
            self._values["db_user_name"] = db_user_name
        if default_database_name is not None:
            self._values["default_database_name"] = default_database_name
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if parameters is not None:
            self._values["parameters"] = parameters
        if rds_password is not None:
            self._values["rds_password"] = rds_password
        if storage_encrypted is not None:
            self._values["storage_encrypted"] = storage_encrypted
        if time_zone is not None:
            self._values["time_zone"] = time_zone
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def db_clusterp_pg(self) -> typing.Optional[aws_cdk.aws_rds.IParameterGroup]:
        """RDS ParameterGroup.

        default
        :default: - Aurora MySQL ParameterGroup
        """
        result = self._values.get("db_clusterp_pg")
        return result

    @builtins.property
    def db_user_name(self) -> typing.Optional[builtins.str]:
        """RDS default Super User Name.

        default
        :default: - sysadmin
        """
        result = self._values.get("db_user_name")
        return result

    @builtins.property
    def default_database_name(self) -> typing.Optional[builtins.str]:
        """RDS default Database Name.

        default
        :default: - globaldatabase
        """
        result = self._values.get("default_database_name")
        return result

    @builtins.property
    def deletion_protection(self) -> typing.Optional[builtins.bool]:
        """Global RDS Database Cluster Engine Deletion Protection Option .

        default
        :default: - false
        """
        result = self._values.get("deletion_protection")
        return result

    @builtins.property
    def engine_version(self) -> typing.Optional[aws_cdk.aws_rds.IClusterEngine]:
        """RDS Database Cluster Engine .

        default
        :default: - rds.DatabaseClusterEngine.auroraMysql({version: rds.AuroraMysqlEngineVersion.VER_2_07_1,})
        """
        result = self._values.get("engine_version")
        return result

    @builtins.property
    def instance_type(self) -> typing.Optional["InstanceTypeEnum"]:
        """RDS Instance Type only can use r4 or r5 type  see more https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html#aurora-global-database.limitations.

        default
        :default: - r5.large
        """
        result = self._values.get("instance_type")
        return result

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """RDS Parameters.

        default
        :default: - {time_zone: 'UTC'}
        """
        result = self._values.get("parameters")
        return result

    @builtins.property
    def rds_password(self) -> typing.Optional[builtins.str]:
        """return RDS Cluster password."""
        result = self._values.get("rds_password")
        return result

    @builtins.property
    def storage_encrypted(self) -> typing.Optional[builtins.bool]:
        """Global RDS Database Cluster Engine Storage Encrypted Option .

        default
        :default: - true
        """
        result = self._values.get("storage_encrypted")
        return result

    @builtins.property
    def time_zone(self) -> typing.Optional["MySQLtimeZone"]:
        """RDS time zone.

        default
        :default: - MySQLtimeZone.UTC
        """
        result = self._values.get("time_zone")
        return result

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """RDS default VPC.

        default
        :default: - new VPC
        """
        result = self._values.get("vpc")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GolbalAuroraRDSMasterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GolbalAuroraRDSSlaveInfra(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aurora-globaldatabase.GolbalAuroraRDSSlaveInfra",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        deletion_protection: typing.Optional[builtins.bool] = None,
        stack: typing.Optional[aws_cdk.core.Stack] = None,
        storage_encrypted: typing.Optional[builtins.bool] = None,
        subnet_type: typing.Optional[aws_cdk.aws_ec2.SubnetType] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param deletion_protection: Global RDS Database Cluster Engine Deletion Protection Option . Default: - false
        :param stack: RDS Stack.
        :param storage_encrypted: Global RDS Database Cluster Engine Storage Encrypted Option . Default: - true
        :param subnet_type: Slave region.
        :param vpc: Slave region VPC. Default: - new VPC
        """
        props = GolbalAuroraRDSSlaveInfraProps(
            deletion_protection=deletion_protection,
            stack=stack,
            storage_encrypted=storage_encrypted,
            subnet_type=subnet_type,
            vpc=vpc,
        )

        jsii.create(GolbalAuroraRDSSlaveInfra, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="dbSubnetGroup")
    def db_subnet_group(self) -> aws_cdk.aws_rds.CfnDBSubnetGroup:
        """GolbalAuroraRDSSlaveInfra subnet group .

        default
        :default: - true
        """
        return jsii.get(self, "dbSubnetGroup")


@jsii.data_type(
    jsii_type="cdk-aurora-globaldatabase.GolbalAuroraRDSSlaveInfraProps",
    jsii_struct_bases=[],
    name_mapping={
        "deletion_protection": "deletionProtection",
        "stack": "stack",
        "storage_encrypted": "storageEncrypted",
        "subnet_type": "subnetType",
        "vpc": "vpc",
    },
)
class GolbalAuroraRDSSlaveInfraProps:
    def __init__(
        self,
        *,
        deletion_protection: typing.Optional[builtins.bool] = None,
        stack: typing.Optional[aws_cdk.core.Stack] = None,
        storage_encrypted: typing.Optional[builtins.bool] = None,
        subnet_type: typing.Optional[aws_cdk.aws_ec2.SubnetType] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param deletion_protection: Global RDS Database Cluster Engine Deletion Protection Option . Default: - false
        :param stack: RDS Stack.
        :param storage_encrypted: Global RDS Database Cluster Engine Storage Encrypted Option . Default: - true
        :param subnet_type: Slave region.
        :param vpc: Slave region VPC. Default: - new VPC
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if stack is not None:
            self._values["stack"] = stack
        if storage_encrypted is not None:
            self._values["storage_encrypted"] = storage_encrypted
        if subnet_type is not None:
            self._values["subnet_type"] = subnet_type
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def deletion_protection(self) -> typing.Optional[builtins.bool]:
        """Global RDS Database Cluster Engine Deletion Protection Option .

        default
        :default: - false
        """
        result = self._values.get("deletion_protection")
        return result

    @builtins.property
    def stack(self) -> typing.Optional[aws_cdk.core.Stack]:
        """RDS Stack."""
        result = self._values.get("stack")
        return result

    @builtins.property
    def storage_encrypted(self) -> typing.Optional[builtins.bool]:
        """Global RDS Database Cluster Engine Storage Encrypted Option .

        default
        :default: - true
        """
        result = self._values.get("storage_encrypted")
        return result

    @builtins.property
    def subnet_type(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetType]:
        """Slave region."""
        result = self._values.get("subnet_type")
        return result

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """Slave region VPC.

        default
        :default: - new VPC
        """
        result = self._values.get("vpc")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GolbalAuroraRDSSlaveInfraProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-aurora-globaldatabase.InstanceTypeEnum")
class InstanceTypeEnum(enum.Enum):
    R4_LARGE = "R4_LARGE"
    R4_XLARGE = "R4_XLARGE"
    R4_2XLARGE = "R4_2XLARGE"
    R4_4XLARGE = "R4_4XLARGE"
    R4_8XLARGE = "R4_8XLARGE"
    R4_16XLARGE = "R4_16XLARGE"
    R5_LARGE = "R5_LARGE"
    R5_XLARGE = "R5_XLARGE"
    R5_2XLARGE = "R5_2XLARGE"
    R5_4XLARGE = "R5_4XLARGE"
    R5_8XLARGE = "R5_8XLARGE"
    R5_12XLARGE = "R5_12XLARGE"
    R5_16XLARGE = "R5_16XLARGE"
    R5_24XLARGE = "R5_24XLARGE"


@jsii.enum(jsii_type="cdk-aurora-globaldatabase.MySQLtimeZone")
class MySQLtimeZone(enum.Enum):
    UTC = "UTC"
    ASIA_TAIPEI = "ASIA_TAIPEI"
    AFRICA_CAIRO = "AFRICA_CAIRO"
    ASIA_BANGKOK = "ASIA_BANGKOK"
    AUSTRALIA_DARWIN = "AUSTRALIA_DARWIN"
    AFRICA_CASABLANCA = "AFRICA_CASABLANCA"
    ASIA_BEIRUT = "ASIA_BEIRUT"
    AUSTRALIA_HOBART = "AUSTRALIA_HOBART"
    AFRICA_HARARE = "AFRICA_HARARE"
    ASIA_CALCUTTA = "ASIA_CALCUTTA"
    AUSTRALIA_PERTH = "AUSTRALIA_PERTH"
    AFRICA_MONROVIA = "AFRICA_MONROVIA"
    ASIA_DAMASCUS = "ASIA_DAMASCUS"
    AUSTRALIA_SYDNEY = "AUSTRALIA_SYDNEY"
    AFRICA_NAIROBI = "AFRICA_NAIROBI"
    ASIA_DHAKA = "ASIA_DHAKA"
    BRAZIL_EAST = "BRAZIL_EAST"
    AFRICA_TRIPOLI = "AFRICA_TRIPOLI"
    ASIA_IRKUTSK = "ASIA_IRKUTSK"
    CANADA_NEWFOUNDLAND = "CANADA_NEWFOUNDLAND"
    AFRICA_WINDHOEK = "AFRICA_WINDHOEK"
    ASIA_JERUSALEM = "ASIA_JERUSALEM"
    CANADA_SASKATCHEWAN = "CANADA_SASKATCHEWAN"
    AMERICA_ARAGUAINA = "AMERICA_ARAGUAINA"
    ASIA_KABUL = "ASIA_KABUL"
    EUROPE_AMSTERDAM = "EUROPE_AMSTERDAM"
    AMERICA_ASUNCION = "AMERICA_ASUNCION"
    ASIA_KARACHI = "ASIA_KARACHI"
    EUROPE_ATHENS = "EUROPE_ATHENS"
    AMERICA_BOGOTA = "AMERICA_BOGOTA"
    ASIA_KATHMANDU = "ASIA_KATHMANDU"
    EUROPE_DUBLIN = "EUROPE_DUBLIN"
    AMERICA_CARACAS = "AMERICA_CARACAS"
    ASIA_KRASNOYARSK = "ASIA_KRASNOYARSK"
    EUROPE_HELSINKI = "EUROPE_HELSINKI"
    AMERICA_CHIHUAHUA = "AMERICA_CHIHUAHUA"
    ASIA_MAGADAN = "ASIA_MAGADAN"
    EUROPE_ISTANBUL = "EUROPE_ISTANBUL"
    AMERICA_CUIABA = "AMERICA_CUIABA"
    ASIA_MUSCAT = "ASIA_MUSCAT"
    EUROPE_KALININGRAD = "EUROPE_KALININGRAD"
    AMERICA_DENVER = "AMERICA_DENVER"
    ASIA_NOVOSIBIRSK = "ASIA_NOVOSIBIRSK"
    EUROPE_MOSCOW = "EUROPE_MOSCOW"
    AMERICA_FORTALEZA = "AMERICA_FORTALEZA"
    ASIA_RIYADH = "ASIA_RIYADH"
    EUROPE_PARIS = "EUROPE_PARIS"
    AMERICA_GUATEMALA = "AMERICA_GUATEMALA"
    ASIA_SEOUL = "ASIA_SEOUL"
    EUROPE_PRAGUE = "EUROPE_PRAGUE"
    AMERICA_HALIFAX = "AMERICA_HALIFAX"
    ASIA_SHANGHAI = "ASIA_SHANGHAI"
    EUROPE_SARAJEVO = "EUROPE_SARAJEVO"
    AMERICA_MANAUS = "AMERICA_MANAUS"
    ASIA_SINGAPORE = "ASIA_SINGAPORE"
    PACIFIC_AUCKLAND = "PACIFIC_AUCKLAND"
    AMERICA_MATAMOROS = "AMERICA_MATAMOROS"
    PACIFIC_FIJI = "PACIFIC_FIJI"
    AMERICA_MONTERREY = "AMERICA_MONTERREY"
    ASIA_TEHRAN = "ASIA_TEHRAN"
    PACIFIC_GUAM = "PACIFIC_GUAM"
    AMERICA_MONTEVIDEO = "AMERICA_MONTEVIDEO"
    ASIA_TOKYO = "ASIA_TOKYO"
    PACIFIC_HONOLULU = "PACIFIC_HONOLULU"
    AMERICA_PHOENIX = "AMERICA_PHOENIX"
    ASIA_ULAANBAATAR = "ASIA_ULAANBAATAR"
    PACIFIC_SAMOA = "PACIFIC_SAMOA"
    AMERICA_SANTIAGO = "AMERICA_SANTIAGO"
    ASIA_VLADIVOSTOK = "ASIA_VLADIVOSTOK"
    US_ALASKA = "US_ALASKA"
    AMERICA_TIJUANA = "AMERICA_TIJUANA"
    ASIA_YAKUTSK = "ASIA_YAKUTSK"
    US_CENTRAL = "US_CENTRAL"
    ASIA_AMMAN = "ASIA_AMMAN"
    ASIA_YEREVAN = "ASIA_YEREVAN"
    US_EASTERN = "US_EASTERN"
    ASIA_ASHGABAT = "ASIA_ASHGABAT"
    ATLANTIC_AZORES = "ATLANTIC_AZORES"
    US_EAST_INDIANA = "US_EAST_INDIANA"
    ASIA_BAGHDAD = "ASIA_BAGHDAD"
    AUSTRALIA_ADELAIDE = "AUSTRALIA_ADELAIDE"
    US_PACIFIC = "US_PACIFIC"
    ASIA_BAKU = "ASIA_BAKU"
    AUSTRALIA_BRISBANE = "AUSTRALIA_BRISBANE"


class PasswordProvider(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aurora-globaldatabase.PasswordProvider",
):
    """Random Password Provider."""

    def __init__(self) -> None:
        jsii.create(PasswordProvider, self, [])

    @jsii.member(jsii_name="genRdsPassword")
    @builtins.classmethod
    def gen_rds_password(cls) -> builtins.str:
        return jsii.sinvoke(cls, "genRdsPassword", [])


@jsii.data_type(
    jsii_type="cdk-aurora-globaldatabase.RegionalOptions",
    jsii_struct_bases=[],
    name_mapping={"region": "region", "db_subnet_group_name": "dbSubnetGroupName"},
)
class RegionalOptions:
    def __init__(
        self,
        *,
        region: builtins.str,
        db_subnet_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param region: 
        :param db_subnet_group_name: 
        """
        self._values: typing.Dict[str, typing.Any] = {
            "region": region,
        }
        if db_subnet_group_name is not None:
            self._values["db_subnet_group_name"] = db_subnet_group_name

    @builtins.property
    def region(self) -> builtins.str:
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return result

    @builtins.property
    def db_subnet_group_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("db_subnet_group_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RegionalOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "GolbalAuroraRDSMaster",
    "GolbalAuroraRDSMasterProps",
    "GolbalAuroraRDSSlaveInfra",
    "GolbalAuroraRDSSlaveInfraProps",
    "InstanceTypeEnum",
    "MySQLtimeZone",
    "PasswordProvider",
    "RegionalOptions",
]

publication.publish()
