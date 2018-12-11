
from pyo import *

# The purpose of setAutoStartChildren() method is to allow the user
# to control all objects in a dsp chain with single calls on the
# last object of the chain. When active, play/out/stop calls will
# propagate to the children objets (ie. audio objects given as
# argument to the "main" one. 

# The stop(wait) method has a new argument (wait=0) that can be used
# to delay when the real stop call is made. By default, objects given
# to a `mul` attribute are not concerned by the waiting time (the stop
# call triggers the release part of the amplitude envelope while other
# objects wait for the envelope to finish before stoping themselves).
# This behaviour can be reverted by calling useWaitTimeOnStop()
# on specific objects.

# Fader and Adsr objects ignore waiting time given to the stop method.
# They already implement there own fadeout parts.

s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()
s.setAutoStartChildren(True)

TEST = 0

if TEST == 0:
    # Simple oscillator with an amplitude envelope. Call a.stop(1) to fadeout.
    a = RCOsc(freq=[150,150.5], sharp=0.5, mul=Fader(1, 1, mul=.2)).out()
elif TEST == 1:
    # Simple oscillator with frequency and amplitude envelopes.
    freq = Linseg([(0,500),(1, 750),(2, 500)], loop=True)
    a = Sine(freq=freq, mul=Fader(1, 1, mul=.2)).out()
elif TEST == 2:
    # Test case for useWaitTimeOnStop().
    lf = Linseg([(0,0),(0.2,0.1),(0.4,0)], loop=True)
    lf.useWaitTimeOnStop()
    freq = Linseg([(0,500),(1, 750),(2, 500)], loop=True)
    a = Sine(freq=freq, mul=Fader(1, 1, mul=lf)).out()
elif TEST == 3:
    # Test case for list of audio objects.
    lf = Linseg([(0,0),(0.2,0.1),(0.4,0)], loop=True)
    lf.useWaitTimeOnStop()
    pits = [Linseg([(0, 500), (1, 600), (3, 400), (5, 500)]),
            Linseg([(0, 700), (1, 500), (3, 800), (5, 750)])]
    a = Sine(freq=pits, mul=Fader(1, 1, mul=lf)).out()
elif TEST == 4:
    # Test case for deeper propagation. Call rev.stop(5) to keep the reverb trail.
    env = Fader(0.1, 0.1)
    sf = SfPlayer(SNDS_PATH+"/transparent.aif", loop=True, mul=env)
    rev = WGVerb(sf, feedback=0.9, mul=0.5).out()
elif TEST == 5:
    # Test case for TableRead object.
    table = LinTable([(0, 1000), (2048, 1500), (6144,500), (8192, 1000)])
    reader = TableRead(table, freq=1, loop=1)
    a = Sine(freq=reader, mul=Fader(1, 1, mul=.2)).out()
elif TEST == 6:
    # Test case for addLinkedObject().
    tab = NewTable(length=2, chnls=1)
    rec = TableRec(Sine(500), tab, .01)
    amp = Port(TrigVal(rec["trig"], 0.5))
    amp.useWaitTimeOnStop()
    osc = Osc(tab, tab.getRate(), mul=Fader(1, 1, mul=amp))
    osc.addLinkedObject(rec)
    osc.out()

s.gui(locals())
