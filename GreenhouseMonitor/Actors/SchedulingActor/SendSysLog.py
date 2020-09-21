#!/bin/python3

from Messages.Message import Message
from Actors.SchedulingActor.SchedulingActor import SchedulingActor
from thespian.actors import *
import sys
import pickle

msg = Message("TimingTask1")

ActorSystem().tell(ActorSystem().createActor(SchedulingActor, globalName='SchedulingActorSingleton'), msg.encode())

