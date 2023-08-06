import re

from dev_ping_tester.Cisco import Cisco

from dev_ping_tester.Huawei import Huawei
from dev_ping_tester.BaseDevice import BaseDevice


class AutoDetectDevice(BaseDevice):
    def __init__(self,name,hostname,port,username,password,protocol,debug=False):
        super(AutoDetectDevice,self).__init__(name=name,hostname=hostname,port=port,username=username,password=password,protocol=protocol,enable=None,debug=debug)
        self.handler = None
        self.device_type=""
        self._proxy = None
        # Check device type
        self._connect()
        self._check_device_type()

    def _terminal_length_zero(self):
        # Terminal length zero need to execute after the device type check.
        pass

    def run_and_match(self,command,regex):
        self.handler.send("{}\n##\n".format(command))
        self.expect(r"[>|#|$]\s?##")
        if re.search(regex,str(self.handler.before,encoding="utf-8")):
            return True
        else:
            return False

    def _check_device_type(self):

        # Check if it's huawei
        command = "screen-length 0 temporary\ndisplay version"
        regex=r"Huawei\sTechnologies"
        if self.run_and_match(command,regex):
            self.device_type="huawei"
            self._proxy=Huawei(self.name,self.hostname,self.port,self.username,self.password,self.protocol,debug=self.debug)
            self._proxy.handler=self.handler
            self._proxy._terminal_length_zero()
            return
        command2 = "terminal length 0\nshow version"
        regex=r"Cisco\sSystems"
        if self.run_and_match(command2,regex):
            self.device_type="cisco"
            self._proxy=Cisco(self.name,self.hostname,self.port,self.username,self.password,self.protocol,debug=self.debug)
            self._proxy.handler=self.handler
            self._proxy._terminal_length_zero()
            return
        raise Exception("None Supported device.")


    def ping(self,dest,count):
        return self._proxy.ping(dest,count)


