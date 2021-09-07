import json
import matplotlib.pyplot as plt
import seaborn as sns
with open('../utils/vocab_based/labeldata.json', 'r') as f:
    data = json.load(f)
summary = {}
upgrade_summary = {}
label_count = 0
count = 0
upgrade_count = 0
label_list = [
"battery", "internet", "bluetooth", "usb/type-c", "device connection", "software/system update", "screen", "virtual assistance",
"headphone", "audio/voice", "app", "notification", "camera/multimedia", "sim/esim", "communication", "account", "security", 
"boot", "storage", "backup", "setup", "gps", "user interface", "feature request", "appearance", "customer service", "other", "useless"
        ]
for idx, d in data.items():
    label = d['label']
    if len(label) > 0:
        label_count+=1
    if len(label) > 1:
        count+=1
        if "software/system update" in label:
            for l in label:
                if l == "software/system update":
                    pass
                elif l in upgrade_summary.keys():
                    upgrade_summary[l]+=1
                else:
                    upgrade_summary[l]=1
            upgrade_count += 1
    for l in label:
        if l in summary.keys():
            summary[l]+=1
        else:
            summary[l]=1
_, __ = plt.pie(summary.values(), labels=summary.keys())
plt.title('distribution', fontsize=24)
plt.legend(_, ["{0} - {1:.2f}%".format(i, j/label_count*100) for i, j in zip(summary.keys(), summary.values())], loc="lower left")
plt.axis('equal')
plt.show()
for l in label_list:
    if l not in summary.keys():
        summary[l] = 0
print(summary)
print("# label data: {}".format(label_count))
print("# multi_label: {}".format(count))
print("# multi_label with upgrade: {}".format(upgrade_count))
