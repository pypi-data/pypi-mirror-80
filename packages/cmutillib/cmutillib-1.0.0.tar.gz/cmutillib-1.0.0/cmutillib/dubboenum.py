from enum import Enum, unique


@unique
class clustertype(Enum):
    MOCK = 1
    FAILOVER = 2
    FAILFAST = 3
    FAILSAFE = 4
    FAILBACK = 5
    FORKING = 6
    AVAILABLE = 7
    MERGEABLE = 8
    BROADCAST = 9
    ZONE_AWARE = 10


@unique
class registry_protocol(Enum):
    ZOOKEEPER = 1
    MULTICAST = 2
    REDIS = 3
    SIMPLE = 4


@unique
class rpc_protocol(Enum):
    dubbo = 1
    rmi = 2
    hessian = 3
    webservice = 4
    memcached = 5
    redis = 6


@unique
class loadbalance(Enum):
    random = 1
    roundrobin = 2
    leastactive = 3
    consistenthash = 4
