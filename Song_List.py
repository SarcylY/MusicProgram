class note:
    def __init__(self, name, acci, pitch, dur = 1):
        self.name = name
        self.acci = acci
        self.pitch = pitch
        self.dur = dur

    def from_string(name):
        pass

twinkle_1 = note('c','n',4,1)
twinkle_2 = note('c','n',4,1)
twinkle_3 = note('g','n',4,1)
twinkle_4 = note('g','n',4,1)
twinkle_5 = note('a','n',4,1)
twinkle_6 = note('a','n',4,1)
twinkle_7 = note('g','n',4,2)
twinkle_8 = note('f','n',4,1)
twinkle_9 = note('f','n',4,1)
twinkle_10 = note('e','n',4,1)
twinkle_11 = note('e','n',4,1)
twinkle_12 = note('d','n',4,1)
twinkle_13 = note('d','n',4,1)
twinkle_14 = note('c','n',4,2)

twinkle = []
i = 1
while i <= 14:
    current_note = "twinkle_" + str(i)
    exec("twinkle.append(" + current_note + ")")
    i += 1

mary_1 = note('e','n',4,1)
mary_2 = note('d','n',4,1)
mary_3 = note('c','n',4,1)
mary_4 = note('d','n',4,1)
mary_5 = note('e','n',4,1)
mary_6 = note('e','n',4,1)
mary_7 = note('e','n',4,2)
mary_8 = note('d','n',4,1)
mary_9 = note('d','n',4,1)
mary_10 = note('d','n',4,2)
mary_11 = note('e','n',4,1)
mary_12 = note('g','n',4,1)
mary_13 = note('g','n',4,2)
mary_14 = note('e','n',4,1)
mary_15 = note('d','n',4,1)
mary_16 = note('c','n',4,1)
mary_17 = note('d','n',4,1)
mary_18 = note('e','n',4,1)
mary_19 = note('e','n',4,1)
mary_20 = note('e','n',4,2)
mary_21 = note('d','n',4,1)
mary_22 = note('d','n',4,1)
mary_23 = note('e','n',4,1)
mary_24 = note('d','n',4,1)
mary_25 = note('c','n',4,4)

mary = []
i = 1
while i <= 25:
    current_note = "mary_" + str(i)
    exec("mary.append(" + current_note + ")")
    i += 1

chro_1 = note('c','n',4,2)
chro_2 = note('c','#',4,2)
chro_3 = note('d','n',4,2)
chro_4 = note('d','#',4,2)
chro_5 = note('e','n',4,2)
chro_6 = note('f','n',4,2)
chro_7 = note('f','#',4,2)
chro_8 = note('g','n',4,2)
chro_9 = note('g','#',4,2)
chro_10 = note('a','n',4,2)
chro_11 = note('a','#',4,2)
chro_12 = note('b','n',4,2)
chro_13 = note('c','n',5,2)
chro_14 = note('b','n',4,2)
chro_15 = note('b','b',4,2)
chro_16 = note('a','n',4,2)
chro_17 = note('a','b',4,2)
chro_18 = note('g','n',4,2)
chro_19 = note('g','b',4,2)
chro_20 = note('f','n',4,2)
chro_21 = note('e','n',4,2)
chro_22 = note('e','b',4,2)
chro_23 = note('d','n',4,2)
chro_24 = note('d','b',4,2)
chro_25 = note('c','n',4,2)

chro = []
i = 1
while i <= 25:
    current_note = "chro_" + str(i)
    exec("chro.append(" + current_note + ")")
    i += 1

surp_1 = note('c','n',4,0.5)
surp_2 = note('c','n',4,0.5)
surp_3 = note('e','n',4,0.5)
surp_4 = note('e','n',4,0.5)
surp_5 = note('g','n',4,0.5)
surp_6 = note('g','n',4,0.5)
surp_7 = note('e','n',4,1)
surp_8 = note('f','n',4,0.5)
surp_9 = note('f','n',4,0.5)
surp_10 = note('d','n',4,0.5)
surp_11 = note('d','n',4,0.5)
surp_12 = note('b','n',3,0.5)
surp_13 = note('b','n',3,0.5)
surp_14 = note('g','n',3,1)
surp_15 = note('c','n',4,0.5)
surp_16 = note('c','n',4,0.5)
surp_17 = note('e','n',4,0.5)
surp_18 = note('e','n',4,0.5)
surp_19 = note('g','n',4,0.5)
surp_20 = note('g','n',4,0.5)
surp_21 = note('e','n',4,1)
surp_22 = note('c','n',5,0.5)
surp_23 = note('c','n',5,0.5)
surp_24 = note('f','#',4,0.5)
surp_25 = note('f','#',4,0.5)
surp_26 = note('g','n',4,2)

surp = []
i = 1
while i <= 26:
    current_note = "surp_" + str(i)
    exec("surp.append(" + current_note + ")")
    i += 1

etude_1 = note('c','n',5,0.5)
etude_2 = note('d','b',5,0.5)
etude_3 = note('b','n',4,0.5)
etude_4 = note('c','n',5,0.5)
etude_5 = note('e','b',5,0.5)
etude_6 = note('d','b',5,0.5)
etude_7 = note('c','n',5,0.5)
etude_8 = note('d','b',5,0.5)
etude_9 = note('b','n',4,0.5)
etude_10 = note('c','n',5,0.5)
etude_11 = note('f','#',5,0.5)
etude_12 = note('g','n',5,0.5)

etude_13 = note('c','n',5,0.5)
etude_14 = note('d','b',5,0.5)
etude_15 = note('b','n',4,0.5)
etude_16 = note('c','n',5,0.5)
etude_17 = note('e','b',5,0.5)
etude_18 = note('d','b',5,0.5)
etude_19 = note('c','n',5,0.5)
etude_20 = note('d','b',5,0.5)
etude_21 = note('b','n',4,0.5)
etude_22 = note('c','n',5,0.5)
etude_23 = note('a','b',5,0.5)
etude_24 = note('f','n',5,0.5)

etude_25 = note('e','n',5,0.5)
etude_26 = note('f','n',5,0.5)
etude_27 = note('e','n',5,0.5)
etude_28 = note('d','#',5,0.5)
etude_29 = note('e','n',5,0.5)
etude_30 = note('g','n',5,0.5)
etude_31 = note('b','b',5,0.5)
etude_32 = note('c','n',6,0.5)
etude_33 = note('b','b',5,0.5)
etude_34 = note('a','n',5,0.5)
etude_35 = note('b','b',5,0.5)
etude_36 = note('d','b',6,0.5)

etude_37 = note('c','n',6,0.5)
etude_38 = note('d','b',6,0.5)
etude_39 = note('c','n',6,0.5)
etude_40 = note('b','n',5,0.5)
etude_41 = note('c','n',6,0.5)
etude_42 = note('g','n',5,0.5)
etude_43 = note('a','b',5,0.5)
etude_44 = note('b','b',5,0.5)
etude_45 = note('a','b',5,0.5)
etude_46 = note('g','n',5,0.5)
etude_47 = note('a','b',5,0.5)
etude_48 = note('e','n',5,0.5)

etude_49 = note('f','n',5,0.5)
etude_50 = note('g','n',5,0.5)
etude_51 = note('f','n',5,0.5)
etude_52 = note('e','n',5,0.5)
etude_53 = note('f','n',5,0.5)
etude_54 = note('c','n',5,0.5)
etude_55 = note('d','b',5,0.5)
etude_56 = note('e','b',5,0.5)
etude_57 = note('d','b',5,0.5)
etude_58 = note('c','n',5,0.5)
etude_59 = note('d','b',5,0.5)
etude_60 = note('b','n',4,0.5)

etude_61 = note('c','n',5,0.5)
etude_62 = note('d','b',5,0.5)
etude_63 = note('c','n',5,0.5)
etude_64 = note('b','n',4,0.5)
etude_65 = note('c','n',5,0.5)
etude_66 = note('g','n',4,0.5)
etude_67 = note('a','b',4,0.5)
etude_68 = note('b','b',4,0.5)
etude_69 = note('a','b',4,0.5)
etude_70 = note('g','n',4,0.5)
etude_71 = note('a','b',4,0.5)
etude_72 = note('f','n',4,0.5)

etude_73 = note('e','n',4,0.5)
etude_74 = note('g','n',4,0.5)
etude_75 = note('b','b',4,0.5)
etude_76 = note('d','b',5,0.5)
etude_77 = note('e','n',5,0.5)
etude_78 = note('g','n',5,0.5)
etude_79 = note('b','b',5,0.5)
etude_80 = note('d','b',6,0.5)
etude_81 = note('c','n',6,0.5)
etude_82 = note('b','b',5,0.5)
etude_83 = note('a','b',5,0.5)
etude_84 = note('g','n',5,0.5)

etude_85 = note('b','b',5,0.5)
etude_86 = note('c','n',6,0.5)
etude_87 = note('a','b',5,0.5)
etude_88 = note('g','n',5,0.5)
etude_89 = note('a','b',5,0.5)
etude_90 = note('f','n',5,0.5)
etude_91 = note('e','n',5,0.5)
etude_92 = note('g','n',5,0.5)
etude_93 = note('f','n',5,0.5)
etude_94 = note('e','n',5,0.5)
etude_95 = note('f','n',5,0.5)
etude_96 = note('d','b',5,0.5)

etude = []
i = 1
while i <= 96:
    current_note = "etude_" + str(i)
    exec("etude.append(" + current_note + ")")
    i += 1

test_1 = note('c','n',4,1)
test_2 = note('g','n',6,1)
test_3 = note('f','n',4,1)
test_4 = note('a','n',7,1)

test = []
i = 1
while i <= 4:
    current_note = "test_" + str(i)
    exec("test.append(" + current_note + ")")
    i += 1