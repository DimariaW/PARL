#   Copyright (c) 2018 PaddlePaddle Authors. All Rights Reserved.
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

import os
import parl
import unittest
import time
import threading

from parl.remote.master import Master
from parl.remote.worker import Worker
from parl.remote.client import disconnect
from parl.remote.monitor import ClusterMonitor
from parl.utils import get_free_tcp_port


@parl.remote_class
class Actor(object):
    def __init__(self, x=10):
        self.x = x
        self.data = []

class TestClusterStatus(unittest.TestCase):
    def tearDown(self):
        disconnect()

    def test_cluster_status(self):
        port = get_free_tcp_port()
        master = Master(port=port)
        th = threading.Thread(target=master.run)
        th.start()
        time.sleep(5)
        parl.connect('localhost:{}'.format(port))
        worker = Worker('localhost:{}'.format(port), 1)
        time.sleep(5)
        status_info = master.cluster_monitor.get_status_info()
        self.assertEqual(status_info, 'has 0 used cpus, 1 vacant cpus.')
        actor = Actor()
        time.sleep(50)
        status_info = master.cluster_monitor.get_status_info()
        self.assertEqual(status_info, 'has 1 used cpus, 0 vacant cpus.')
        worker.exit()
        master.exit()
        th.join()


if __name__ == '__main__':
    unittest.main()
