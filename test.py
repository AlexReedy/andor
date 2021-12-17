readtime_data = []
for preampgain in range(3):
    for vss in range(2):
        for hss in range(4):
            row = [preampgain, vss, hss]
            readtime_data.append(row)
for i in range(len(readtime_data)):
    print(readtime_data[i])





























