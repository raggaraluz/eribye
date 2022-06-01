Clock.bpm = 175
Scale.default = 'minor'
Root.default = 'Ab'

####################################################
##### Can you imagine how PM cell data sounds? #####
####################################################
import pandas as pd
pm = pd.read_parquet('EUtranCellFDD_PM.parquet')

m1 >> pads(list(pm.dL_user_thp / max(pm.dL_user_thp) * 20), sustain = list(pm.latency), amp = list(pm.dl_traffic / max(pm.dl_traffic)), bpm=90)

m2 >> bell(list(pm.dlprbutil), dur = 6, amp = 0.2)

d1 >> play('x         xx         ')

d2 >> play('Goodbye my friend', bpm=90, amp = 0.2)

m1.stop()

b1 >> blip([0, -1, -2, -3], dur=2, start=Clock.mod(8), hpf=500, sustain=1) + (-7)

b2 >> varsaw([0, -1, -2, -3], dur=2, start=Clock.mod(8), hpf=500, sustain=1, attack=0.1, amp = 0.5) + (-7)

d3 >> play('x o ')

d2.stop()


