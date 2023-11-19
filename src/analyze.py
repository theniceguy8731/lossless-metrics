import csv
import numpy as np
import matplotlib.pyplot as plt


csv_data=[]
csv_file="../results/final-result.csv"

with open(csv_file,"r+") as file:
    csv_reader=csv.reader(file)
    for row in csv_reader:
        csv_data.append(row)
print(csv_data)

algo_name=[]
compression_time=[]
decompression_time=[]
compressed_file_size=[]

for i in csv_data:
    if i[0]=="Algo_name":
        pass
    else:
        algo_name.append(i[0])
        compression_time.append(int(i[1]))
        decompression_time.append(int(i[2]))
        compressed_file_size.append(int(i[3]))

print(algo_name,compression_time,decompression_time,compressed_file_size)

fig,axs = plt.subplots(2,2,figsize=(20,10))
axs[0,0].bar(algo_name, compression_time, color ='maroon', 
        width = 0.4)
axs[1,0].bar(algo_name, decompression_time, color ='blue', 
        width = 0.4)
axs[0,1].bar(algo_name, compressed_file_size, color ='pink', 
        width = 0.4)
fig.delaxes(axs[1, 1])

plt.show()
