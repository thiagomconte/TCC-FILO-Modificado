
# # rj
# for i in range(0, 2):
#     instanceInfo = open(
#         f"./conversionsPython/cvrp-0-df-{i}.txt", "r").read().split("\n")
#     numClient = int(instanceInfo[3].split(":")[1])
#     nome = instanceInfo[0].split(":")[1]
#     output = open("instancesInfo.csv", "a")
#     output.write(f"{nome};{numClient} \n")

# for i in range(10, 18):
#     instanceInfo = open(
#         f"./conversionsPython/cvrp-0-df-{i}.txt", "r").read().split("\n")
#     numClient = int(instanceInfo[3].split(":")[1])
#     nome = instanceInfo[0].split(":")[1]
#     output = open("instancesInfo.csv", "a")
#     output.write(f"{nome};{numClient} \n")

# # PA
# for i in range(0, 2):
#     instanceInfo = open(
#         f"./conversionsPython/cvrp-0-pa-{i}.txt", "r").read().split("\n")
#     numClient = int(instanceInfo[3].split(":")[1])
#     nome = instanceInfo[0].split(":")[1]
#     output = open("instancesInfo.csv", "a")
#     output.write(f"{nome};{numClient} \n")

# for i in range(10, 18):
#     instanceInfo = open(
#         f"./conversionsPython/cvrp-0-pa-{i}.txt", "r").read().split("\n")
#     numClient = int(instanceInfo[3].split(":")[1])
#     nome = instanceInfo[0].split(":")[1]
#     output = open("instancesInfo.csv", "a")
#     output.write(f"{nome};{numClient} \n")

# # RJ
# for i in range(0, 2):
#     instanceInfo = open(
#         f"./conversionsPython/cvrp-0-rj-{i}.txt", "r").read().split("\n")
#     numClient = int(instanceInfo[3].split(":")[1])
#     nome = instanceInfo[0].split(":")[1]
#     output = open("instancesInfo.csv", "a")
#     output.write(f"{nome};{numClient} \n")

# for i in range(10, 18):
#     instanceInfo = open(
#         f"./conversionsPython/cvrp-0-rj-{i}.txt", "r").read().split("\n")
#     numClient = int(instanceInfo[3].split(":")[1])
#     nome = instanceInfo[0].split(":")[1]
#     output = open("instancesInfo.csv", "a")
#     output.write(f"{nome};{numClient} \n")


# dfArray = [0, 1, 2, 18, 30]
# rjArray = [11, 25, 30, 35, 65, 77]

# for i in dfArray:
#     instanceInfo = open(
#         f"./conversionsPython/cvrp-1-df-{i}.txt", "r").read().split("\n")
#     numClient = int(instanceInfo[3].split(":")[1])
#     nome = instanceInfo[0].split(":")[1]
#     output = open("instancesInfo.csv", "a")
#     output.write(f"{nome};{numClient} \n")

# for i in range(0, 2):
#     instanceInfo = open(
#         f"./conversionsPython/cvrp-2-df-{i}.txt", "r").read().split("\n")
#     numClient = int(instanceInfo[3].split(":")[1])
#     nome = instanceInfo[0].split(":")[1]
#     output = open("instancesInfo.csv", "a")
#     output.write(f"{nome};{numClient} \n")

# for i in rjArray:
#     instanceInfo = open(
#         f"./conversionsPython/cvrp-1-rj-{i}.txt", "r").read().split("\n")
#     numClient = int(instanceInfo[3].split(":")[1])
#     nome = instanceInfo[0].split(":")[1]
#     output = open("instancesInfo.csv", "a")
#     output.write(f"{nome};{numClient} \n")

# paArray = [0, 2]
# for i in paArray:
#     instanceInfo = open(
#         f"./conversionsPython/cvrp-1-pa-{i}.txt", "r").read().split("\n")
#     numClient = int(instanceInfo[3].split(":")[1])
#     nome = instanceInfo[0].split(":")[1]
#     output = open("instancesInfo.csv", "a")
#     output.write(f"{nome};{numClient} \n")

# for i in range(2, 6):
#     instanceInfo = open(
#         f"./conversionsPython/cvrp-{i}-rj-0.txt", "r").read().split("\n")
#     numClient = int(instanceInfo[3].split(":")[1])
#     nome = instanceInfo[0].split(":")[1]
#     output = open("instancesInfo.csv", "a")
#     output.write(f"{nome};{numClient} \n")

instanceInfo = open(
        f"./conversionsPython/cvrp-1-rj-0.txt", "r").read().split("\n")
numClient = int(instanceInfo[3].split(":")[1])
nome = instanceInfo[0].split(":")[1]
output = open("instancesInfo.csv", "a")
output.write(f"{nome};{numClient} \n")    
