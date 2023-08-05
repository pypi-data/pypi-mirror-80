# -*-coding:utf-8-*-
# ! /usr/bin/python3

import os
import json
from .gui import *


class CardEnv(object):
    def __init__(self):
        self.version = '0.0.1'
        cui = gui()
        self.i = cui.i
        self.s = cui.s
        self.w = cui.w
        self.c = color()

    @staticmethod
    def check_install(command):
        command_pass = 0
        for cmd_path in os.environ['PATH'].split(':'):
            if os.path.isdir(cmd_path) and command in os.listdir(cmd_path):
                command_pass = 1
            if not command_pass:
                command_pass = 0
        return command_pass

    @staticmethod
    def check_brew(self):
        if not self.check_install('brew'):
            self.i('start install HomeBrew .....')
            os.system(
                '/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')
        else:
            self.s('brew existed')

    @staticmethod
    def check_node(self):
        if not self.check_install('node'):
            self.i('start install node .....')
            os.system('brew install node')
            os.system('npm install tnpm -g --registry=https://registry.npm.alibaba-inc.com')
        else:
            self.s('node existed')
            self.i('start check tnpm')
            if not self.check_install('tnpm'):
                os.system('npm install tnpm -g --registry=https://registry.npm.alibaba-inc.com')
            else:
                self.i('tnpm is installed')

    @staticmethod
    def check_accore1(self):
        if not self.check_install('act'):
            self.i('start install AntCardSDK Build tools .....')
            os.system("tnpm install @ali/cube -g")
        else:
            stream_local = os.popen('npm ls @ali/cube -g -json')
            local_info = json.loads(stream_local.read())
            local_version = local_info["dependencies"]["@ali/cube"]["version"]
            stream = os.popen('npm info @ali/cube -json')
            corev1_json = stream.read()
            corev1_json_obj = json.loads(corev1_json)
            latest_version = corev1_json_obj["dist-tags"]["latest"]
            self.i('accore local version : ' + local_version)
            self.i('accore latest version : ' + latest_version)
            if latest_version != local_version:
                self.i('start upgrade AntCardSDK Build tools .....')
                op_cmd = 'tnpm install' + ' @ali/cube' + '@' + latest_version + ' -g'
                os.system(op_cmd)
            else:
                pass

    @staticmethod
    def card_sdk_setup(self):
        self.check_brew(self)
        self.check_node(self)
        self.check_accore1(self)
