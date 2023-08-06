#
# Copyright 2018-2019 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import time
from flask import Flask, request, Response
from flask_restx import Api, Namespace
from flask_cors import CORS
from .default_config import API_TITLE, API_DESC, API_VERSION
from .utils import getLogger, getHostnameAndIp, register, logHandler
import logging

# 重新定义flask日志
logging.getLogger("werkzeug").addHandler(logHandler("flask"))

MAX_API = Namespace('model', description='Model information and inference operations')


class MAXApp(object):

    def __init__(self, title=API_TITLE, desc=API_DESC, version=API_VERSION):
        self.app = Flask(title, static_url_path='')
        self.app.logger = getLogger("cyclonefw")
        self.metrics = {}
        # load config
        if os.path.exists("config.py"):
            self.app.config.from_object("config")

        self.api = Api(
            self.app,
            title=title,
            description=desc,
            version=version)

        self.api.namespaces.clear()
        self.api.add_namespace(MAX_API)

        # enable cors if flag is set
        # if os.getenv('CORS_ENABLE') == 'true' and (
        #         os.environ.get('WERKZEUG_RUN_MAIN') == 'true' or self.app.debug is not True):
        # 默认跨域
        CORS(self.app, origins='*')
        print('NOTE: MAX Model Server is currently allowing cross-origin requests - (CORS ENABLED)')

    def add_api(self, api, route):
        MAX_API.add_resource(api, route)

    def mount_static(self, route):
        @self.app.route(route)
        def index():
            return self.app.send_static_file('index.html')

    def after(self, resp):
        if request.path == "/metrics":
            return resp
        accessTime = request.__getattr__("access_time")
        done = int(time.time() * 1000) - accessTime
        statusCode = resp.status_code
        if statusCode not in self.metrics:
            self.metrics[statusCode] = {}
        if request.path not in self.metrics[statusCode]:
            self.metrics[statusCode][request.path] = {
                "count": 0,
                "total": 0
            }
        self.metrics[statusCode][request.path]["count"] += 1
        self.metrics[statusCode][request.path]["total"] += done
        return resp

    def before(self):
        request.__setattr__('access_time', int(time.time() * 1000))

    def run(self, host='0.0.0.0', port=5000):
        """
        启动服务
        :param host: host, 默认为0.0.0.0
        :param port: 端口, 默认为5000
        :return:
        """

        finalPort = self.app.config["PORT"] if "PORT" in self.app.config else port

        if "REGISTRY" in self.app.config:
            hostname, ip = getHostnameAndIp()
            ip = self.app.config["IP"] if "IP" in self.app.config else ip
            register(self.app.config["REGISTRY"],
                     self.app.config["NAME"] if "NAME" in self.app.config else ip,
                     ip, finalPort,
                     self.app.config["TAGS"] if "TAGS" in self.app.config else [])

        @self.app.route("/metrics", methods=("GET",))
        def metrics():
            """
            监控接口
            :return:
            """
            resp = Response()
            resp.headers.set('Content-Type', 'text/plain')
            content = []
            for code in self.metrics.keys():
                pathData = self.metrics[code]
                for path in pathData.keys():
                    metricsData = pathData[path]
                    content.append("{}{{{}}} {}".format(
                        "count",
                        'path="{}",code="{}"'.format(path, code),
                        metricsData["count"]
                    ))
                    content.append("{}{{{}}} {}".format(
                        "total",
                        'path="{}",code="{}"'.format(path, code),
                        metricsData["total"]
                    ))
            resp.set_data("\n".join(content))
            return resp

        self.app.before_request(self.before)
        self.app.after_request(self.after)
        self.app.run(host=host, port=finalPort)
