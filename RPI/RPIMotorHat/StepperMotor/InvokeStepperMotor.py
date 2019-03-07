#!/usr/bin/env python
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import codecs
import atexit
from Raspi_MotorHat import Raspi_MotorHat, Raspi_StepperMotor

mh = Raspi_MotorHat(0x6F)
myStepper = None

def turnOffMotors():
    mh.getMotor(1).run(Raspi_MotorHat.RELEASE)
    mh.getMotor(2).run(Raspi_MotorHat.RELEASE)
    mh.getMotor(3).run(Raspi_MotorHat.RELEASE)
    mh.getMotor(4).run(Raspi_MotorHat.RELEASE)

atexit.register(turnOffMotors())

def describe(processor):
    processor.setDescription("Controls a 12V .5 AMP stepper motor attached to a Raspberry PI")

def onInitialize(processor):
    processor.setSupportsDynamicProperties()
    myStepper = mh.getStepper(200, 2)
    myStepper.setSpeed(300)

class RPISenseHat(object):
    def __init__(self):
        self.content = None

    def process(self, input_stream):
        self.content = codecs.getreader('utf-8')(input_stream).read()
        return len(self.content)

def onTrigger(context, session):
    flow_file = session.get()

    if flow_file is None:
        flow_file = session.create()

    myStepper.step(100, Raspi_MotorHat.FORWARD, Raspi_MotorHat.SINGLE)
    session.transfer(flow_file, REL_SUCCESS)