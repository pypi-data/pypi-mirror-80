'''
Created on 2019年6月4日

@author: 67362
'''
from json.decoder import JSONDecodeError

from SeleniumLibrary.base import keyword
from SeleniumLibrary.base.librarycomponent import LibraryComponent
from .dubboenum import clustertype, rpc_protocol, registry_protocol, loadbalance
import os.path
import json
import jpype
class interfaceutils(object):

    def __init__(self):
        self._start_jvm()
        pass
    @keyword
    def call_dubbo(self, address, interfacename, methodname, methodArgs, rpcProtocol=1,registryProtocol=None, timeout=1000, version='',
                   retries=0, cluster=3, group='', connections=100, loadBalance=1,
                   isasync=False, registryGroup='', registryUsername='',
                   registryPwd='', registryTimeout=10000):

        self._start_jvm()
        Test = jpype.JClass('robot.keywords.DubboKeywordsForJava')
        # 或者通过JPackage引用Test类
        # com = jpype.JPackage('robot.keywords')
        t = Test()
        # rpcProtocol
        try:
            if rpc_protocol.dubbo.value == int(rpcProtocol):
                rpcProtocolstr = rpc_protocol.dubbo.name.lower()
            elif rpc_protocol.hessian.value == int(rpcProtocol):
                rpcProtocolstr = rpc_protocol.hessian.name.lower()
            elif rpc_protocol.rmi.value == int(rpcProtocol):
                rpcProtocolstr = rpc_protocol.rmi.name.lower()
            elif rpc_protocol.webservice.value == int(rpcProtocol):
                rpcProtocolstr = rpc_protocol.webservice.name.lower()
            elif rpc_protocol.memcached.value == int(rpcProtocol):
                rpcProtocolstr = rpc_protocol.memcached.name.lower()
            elif rpc_protocol.redis.value == int(rpcProtocol):
                rpcProtocolstr = rpc_protocol.redis.name.lower()
            else:
                rpcProtocolstr = rpc_protocol.dubbo.name.lower()
        except ValueError :
            rpcProtocolstr = rpc_protocol.dubbo.name.lower()
        # cluster
        try:
            if clustertype.MOCK.value == int(cluster):
                clusterstr = clustertype.MOCK.name.lower()
            elif clustertype.FAILOVER.value == int(cluster):
                clusterstr = clustertype.FAILOVER.name.lower()
            elif clustertype.FAILFAST.value == int(cluster):
                clusterstr = clustertype.FAILFAST.name.lower()
            elif clustertype.FAILSAFE.value == int(cluster):
                clusterstr = clustertype.FAILSAFE.name.lower()
            elif clustertype.FAILBACK.value == int(cluster):
                clusterstr = clustertype.FAILBACK.name.lower()
            elif clustertype.FORKING.value == int(cluster):
                clusterstr = clustertype.FORKING.name.lower()
            elif clustertype.AVAILABLE.value == int(cluster):
                clusterstr = clustertype.AVAILABLE.name.lower()
            elif clustertype.MERGEABLE.value == int(cluster):
                clusterstr = clustertype.MERGEABLE.name.lower()
            elif clustertype.BROADCAST.value == int(cluster):
                clusterstr = clustertype.BROADCAST.name.lower()
            elif clustertype.ZONE_AWARE.value == int(cluster):
                clusterstr = "zone-aware"
            else:
                clusterstr = clustertype.FAILFAST.name.lower()
        except ValueError:
            clusterstr = clustertype.FAILFAST.name.lower()
        # loadbalance
        try:
            if loadbalance.random.value == int(loadBalance):
                loadBalancestr = loadbalance.random.name.lower()
            elif loadbalance.roundrobin.value == int(loadBalance):
                loadBalancestr = loadbalance.roundrobin.name.lower()
            elif loadbalance.leastactive.value == int(loadBalance):
                loadBalancestr = loadbalance.leastactive.name.lower()
            elif loadbalance.consistenthash.value == int(loadBalance):
                loadBalancestr = loadbalance.consistenthash.name.lower()
            else:
                loadBalancestr = loadbalance.random.name.lower()
        except ValueError:
            loadBalancestr = loadbalance.random.name.lower()
        # isasync
        try:
            isasync = bool(isasync)
        except ValueError:
            isasync = "false"
        # if isasync == True:
        #     isasyncstr = "true"
        # else:
        #     isasyncstr = "false"

        # registryProtocol
        if registryProtocol is None:
            registryProtocolstr = ''
        else:
            try:
                if registry_protocol.ZOOKEEPER.value == int(registryProtocol):
                    registryProtocolstr = registry_protocol.ZOOKEEPER.name.lower()
                elif registry_protocol.MULTICAST.value == int(registryProtocol):
                    registryProtocolstr = registry_protocol.MULTICAST.name.lower()
                elif registry_protocol.REDIS.value == int(registryProtocol):
                    registryProtocolstr = registry_protocol.REDIS.name.lower()
                elif registry_protocol.SIMPLE.value == int(registryProtocol):
                    registryProtocolstr = registry_protocol.SIMPLE.name.lower()
                else:
                    registryProtocolstr = ''
            except ValueError:
                registryProtocolstr = ''
        try:
            timeout = int(timeout)
        except ValueError:
            timeout = 1000
        try:
            retries = int(retries)
        except ValueError:
            retries = 0
        try:
            connections = int(connections)
        except ValueError:
            connections = 100
        # if not isinstance(timeout, int):
        #     timeout = 1000
        # if not isinstance(retries, int):
        #     retries = 0
        # if not isinstance(connections, int):
        #     connections = 100
        try:
            registryTimeout = int(registryTimeout)
        except ValueError:
            registryTimeout = 10000
        # if registryTimeout is None or not isinstance(registryTimeout, int):
        #     registrytimeoutstr = '10000'
        # else:
        #     registrytimeoutstr = str(registryTimeout)
        res = t.callDubbo(str(address), str(interfacename), str(methodname), str(methodArgs), rpcProtocolstr,
                          str(timeout), str(version), str(retries), clusterstr, str(group), str(connections),
                          loadBalancestr,
                          str(isasync), registryProtocolstr, str(registryGroup), str(registryUsername),
                          str(registryPwd), str(registryTimeout))
        try:
            resstr = json.dumps(res)
            resjson = json.loads(resstr)
        except Exception as e:
            resjson = res
        return resjson

    def _start_jvm(self, jarpath="\libs\dubboframe.jar", dependencypath="lib"):
        if not jpype.isJVMStarted():
            fileDir = os.path.realpath(__file__)
            # 获取 jar包路径
            jar_path = os.path.split(fileDir)[0] +jarpath
            dependency = os.path.split(fileDir)[0] + r'\libs\lib'
            dependency2 = os.path.join(os.path.abspath('.'), dependencypath)
            if dependency2 and dependency2 != dependency:
                dependency += ";"+dependency2
            print('--------startjvm---------')
            jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % jar_path,
                       "-Djava.ext.dirs=%s" % dependency)  # 当有依赖的JAR包存在时，一定要使用-Djava.ext.dirs参数进行引入
        if not jpype.isThreadAttachedToJVM():
            print('-----attaching jvm-----')
            jpype.attachThreadToJVM()

    def call_dubbo_direct(self, address, interfacename, methodname, methodArgs, rpcProtocol=1, timeout=1000, version='',
                          retries=0, cluster=3, group='', connections=100, loadBalance=1,
                          isasync=False):
        return self.call_dubbo(address, interfacename, methodname, methodArgs, rpcProtocol,None, timeout, version,
                               retries, cluster, group, connections, loadBalance,
                               isasync)
    def shutdown_jvm(self):
        print("--------shutdownjvm---------")
        jpype.shutdownJVM()

    def send_RocketMq(self):
        self._start_jvm()
        sendmq = jpype.JClass('robot.keywords.RocketMqKeywords')
        # 或者通过JPackage引用Test类
        # com = jpype.JPackage('robot.keywords')
        t = sendmq()
        l = list()
        l.append("this is a test")
        jl = jpype.java.util.ArrayList()
        for i in l:
            jl.add(i)
        res = t.sendMsg("dmall-perf","perfWork","D1BBA8AA-B887-4BA0-8369-0CC9C58C1C40","http://zonedevds.dmc.dmall.com/","10.248.224.55:8018","rkt_production_process_flow_v3_dev",jl)
if __name__ == '__main__':
    dc={"t":"1","t2":"2"}
    dc2 = {"t":"2","t2":"3"}
    l = list()
    l.append(dc)
    l.append(dc2)
    print(str(l))
    i = interfaceutils()
    i.send_RocketMq()
    # i = interfaceutils()
    # i.call_dubbo_direct("127.0.0.1:20880","com.dubbo.provider.service.ProviderService","sayHello",'[{"String":"sadasdsa"}]',"dubbo")
    # i.call_dubbo("zookeeper://10.248.224.18:2181?backup=10.248.224.25:2181,10.248.224.39:2181","com.dmall.esc.api.sdk.ESCUserInfoService","getUser",'[{"com.dmall.esc.api.sdk.domain.request.ESCGetUserReq":"{\\\"mobile\\\":\\\"13540424160\\\"}"}]',"1","1")
    # jpype.shutdownJVM()
