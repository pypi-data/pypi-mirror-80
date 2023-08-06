#!/usr/bin/env python

###############################################################################
# Copyright 2020 ScPA StarLine Ltd. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

import threading, time


class StoppableThread(threading.Thread):

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class Spinner():

    def __init__(self, target = None, rate = 1.0):
        self._delay  = 1. / abs(rate)
        self._target = target
        self._thread = None
        self.real_rate = 0.0


    def _rated_loop(self, *args, **kwargs):
        current_thread = threading.currentThread()
        next_call_time = time.time()
        while not current_thread.stopped():
            next_call_time = next_call_time + self._delay;
            self._target(*args, **kwargs)
            rest_time = next_call_time - time.time()
            self.real_rate = (self.real_rate + min(1. / rest_time, 0))
            time.sleep(max(rest_time, 0))


    def set_target(self, target):
        self.stop()
        self._target = target


    def set_rate(self, rate):
        self._delay  = 1. / abs(rate)


    def is_active(self):
        return (self._thread and self._thread.is_alive())


    def is_not_active(self):
        return not self.is_active()


    def start(self,  *args, **kwargs):
        self.stop()
        self._thread = StoppableThread(target = self._rated_loop, args=args, kwargs=kwargs)
        self._thread.daemon = True
        self._thread.start()


    def stop(self):
        if self._thread and self._thread.is_alive():
            self._thread.stop()


    def restart(self):
        self.stop()
        self.start()


    def get_real_rate(self):
        return self.real_rate
