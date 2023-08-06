#!/usr/bin/env python
# coding: utf-8
import codecs
import json
import os
import subprocess
import time

from tronpytool import Tron

ROOT = os.path.join(os.path.dirname(__file__))


class WrapContract(object):
    """docstring for WrapContract The contract for this BOBA TEA"""

    def __init__(self, _network):
        nn1 = Tron(_network)
        if nn1.is_connected():
            self.tron_v1client = nn1
        else:
            print(
                "client v1 is not connected. please check the internet connection or the service is down! network: {}".format(
                    _network))

    def getClient(self):
        return self.tron_v1client

    def loadContract(self, contract_metadata):
        try:
            contractDict = json.load(codecs.open(contract_metadata, 'r', 'utf-8-sig'))
            hex_address = contractDict["transaction"]["contract_address"]
            self.trc_address = self.tron_v1client.address.from_hex(hex_address).decode("utf-8")
            self.transction_detail = contractDict
            self.init_contract()
        except Exception as e:
            print("Problems from loading items from the file: ", e)
        return self

    def getTxID(self):
        return self.transction_detail["txid"]

    def init_contract(self):
        try:
            self.tron_v1client.trx.get_transaction(self.getTxID())
        except Exception as e:
            print("Searching for this tx: ", e)
        print("loading contract address {}".format(self.trc_address))
        return self


class SolcWrap(object):
    """docstring for SolcWrap"""
    outputfolder = "build"
    solfolder = ""
    file_name = "xxx.sol"
    prefixname = ""
    statement = 'End : {}, IO File {}'
    solc_cmd = "solc_remote"

    def __init__(self):
        super(SolcWrap, self).__init__()

    def SetOutput(self, path):
        self.outputfolder = path
        return self

    def SetSolPath(self, path):
        self.solfolder = path
        return self

    def BuildRemote(self):
        list_files = subprocess.run(["{}/{}".format(ROOT, self.solc_cmd)])
        print("The exit code was: %d" % list_files.returncode)
        return self

    def WrapModel(self):
        # path="{}/combinded.json".format(self.outputfolder)
        pathc = os.path.join(os.path.dirname(__file__), self.outputfolder, "combined.json")
        try:
            pathcli = codecs.open(pathc, 'r', 'utf-8-sig')
            self.combined_data = json.load(pathcli)
        except Exception as e:
            print("Problems from loading items from the file: ", e)
        return self

    def byClassName(self, path, classname):
        return "{prefix}:{name}".format(prefix=path, name=classname)

    def GetCode(self, fullname):
        return self.combined_data["contracts"][fullname]["abi"], self.combined_data["contracts"][fullname]["bin"]

    def GetCode(self, path, classname):
        return self.combined_data["contracts"][self.byClassName(path, classname)]["abi"], \
               self.combined_data["contracts"][self.byClassName(path, classname)]["bin"]

    def writeFile(self, content, filename):
        fo = open(filename, "w")
        fo.write(content)
        fo.close()
        print(self.statement.format(time.ctime(), filename))

    def StoreTxResult(self, tx_result_data, filepath):
        self.writeFile(json.dumps(tx_result_data, ensure_ascii=False), filepath)
