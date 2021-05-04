# --------------------------------------------------------------------------- #
#   test_executor.py                                                          #
#                                                                             #
#   Copyright © 2015-2021, Rajiv Bakulesh Shah, original author.              #
#                                                                             #
#   Licensed under the Apache License, Version 2.0 (the "License");           #
#   you may not use this file except in compliance with the License.          #
#   You may obtain a copy of the License at:                                  #
#       http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                             #
#   Unless required by applicable law or agreed to in writing, software       #
#   distributed under the License is distributed on an "AS IS" BASIS,         #
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#   See the License for the specific language governing permissions and       #
#   limitations under the License.                                            #
# --------------------------------------------------------------------------- #


import concurrent.futures
import time

from pottery.executor import BailOutExecutor
from tests.base import TestCase  # type: ignore


class ExecutorTests(TestCase):
    @staticmethod
    def _expensive_func(delay):
        time.sleep(delay)

    def test_threadpoolexecutor(self):
        'ThreadPoolExecutor waits for futures to complete on .__exit__()'
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self._expensive_func, 0.1)
        assert not future.running()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future1 = executor.submit(self._expensive_func, 0.1)
            future2 = executor.submit(self._expensive_func, 0.2)
            future1.result()
        assert not future1.running()
        assert not future2.running()

    def test_bailoutexecutor(self):
        'BailOutExecutor does not wait for futures to complete on .__exit__()'
        with BailOutExecutor() as executor:
            future = executor.submit(self._expensive_func, 0.1)
        assert future.running()
        time.sleep(0.15)
        assert not future.running()

        with BailOutExecutor() as executor:
            future1 = executor.submit(self._expensive_func, 0.1)
            future2 = executor.submit(self._expensive_func, 0.2)
            future1.result()
        assert not future1.running()
        assert future2.running()
        time.sleep(0.15)
        assert not future2.running()