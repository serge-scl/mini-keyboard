# For the editor to work correctly, 60-70% of the word should be correct without errors.
# Correctly without errors, the written part of the word corresponds approximately
# to the root of the word or syllable with the emphasis on it.
# from key_event_dev import kinv as ks1
import random
import json
from key_event_dev import text_in
from action_track2 import YesEvent as Yes_w
from action_track2 import NoEvent as No_w
from action_track2 import MayBeNo as Mbn_w
from action_track2 import MayBeYes as Mby_w
from action_track2 import TiklEvent as Tkl_w
from action_track2 import Stuck as St_w

btr = open("box_tlt", "r")
vect_tlt = btr.read()
btr.close()
vekt_tlt = int(vect_tlt)

# def weighted_choice_sub(weights):
#     rnd = random.random() * sum(weights)
#     for i, w in enumerate(weights):
#         rnd -= w
#         if rnd < 0:
#             return weights[i]


# """The pyramids gave humanity more than an economic theory of class essence."""

first_distribution = {60: Yes_w, 17: No_w, 7: Mbn_w, 11: Mby_w, 9: Tkl_w, 5: St_w}

stat = {"Yes_w": 60, "No_w": 15, "Mbn_w": 7, "Mby_w": 10, "Tkl_w": 9}
r_stat = {v: k for k, v in stat.items()}

# ---------------------------------------------------

txi = text_in("abfa")  # there is line of input text

# ----------------------------------------------------

weig = []
for i31 in stat:
    weig.append(stat[i31])

basic_simulation = []
for ti in txi:
    # if ti[2] > 16 navigete else
    def back_blank(x):
        if x == [-1, 0, 18]:
            return -1
        elif x == [1, 0, 18]:
            return 1
        else:
            return 0
    # elif ti[2] < 16: text block

    def weighted_choice(weights):
        totals = []
        running_total = 0

        for w in weights:
            running_total += w
            totals.append(running_total)

        rnd = random.random() * running_total
        for i, total in enumerate(totals):
            if rnd < total:
                return weights[i]


    wgch = weighted_choice(weig)
    pow_tlt = r_stat[wgch]

    choice = f"{pow_tlt}({ti}, {vekt_tlt})"
    # print(choice)
    ch2 = eval(choice)
    for i101 in range(0, 2):  # start block
        basic_simulation.append([0, 0])
    for i34 in ch2(10):
        basic_simulation.append(i34)
        # print(i34)
    for i100 in range(0, 2):  # stop dlock
        basic_simulation.append([1, 1])
        # guro x,y, z

    
with open("port_sens.json", "w") as kef:
    json.dump(basic_simulation, kef, indent=None)


if __name__ == "__main__":
    print(basic_simulation)
    pass
