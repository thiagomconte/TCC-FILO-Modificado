import json
import sys

if len(sys.argv) < 4:
    print("Parametros incorretos\n")
    print("Primeiro parametro: arquivo json original\n")
    print("Segundo parametro: Arquivo.vrp.sol\n")
    print("Terceiro parametro: destino do arquivo solução gerado\n")
    sys.exit()

originalInstanceJsonPath = sys.argv[1]
filoSolutionPath = sys.argv[2]

# LÊ VRP.SOL E DIVIDE POR QUEBRA DE LINHA
filoSolution = open(filoSolutionPath, "r").read().split("\n")

# LÊ A INSTÂNCIA DA LOGGI E GUARDA NA "originalInstanceJson"
with open(originalInstanceJsonPath, "r") as data_file:
    json_data = data_file.read()
originalInstanceJson = json.loads(json_data)

# DELIVERIES DO ARQUIVO JSON LOGGI
deliveries = originalInstanceJson["deliveries"]

routes = []
vehicles = []

# GUARDA CADA ROTA
for i in range(0, len(filoSolution) - 1):
    routes.append(filoSolution[i].split(":")[1])

individualRoutes = []
routesSaida = []
matrixRoutes = []

# GUARDA UMA ROTA COMPLETA NA MATRIZ DE ROTAS "matrixRoutes"
for route in routes:
    aux = route.split(" ")  # SEPARA AS ROTAS EM PONTOS

    for j in aux:
        if j != "":  # VERIFICA SE É UM NÚMERO
            routesSaida.append(deliveries[int(j) - 1])

    matrixRoutes.append(routesSaida)
    routesSaida = []

#CRIA O VETOR DE VEHICLES
for i in matrixRoutes:
    vehicles.append({"origin": originalInstanceJson["origin"], "deliveries": i})

# FORMATA NOME DA INSTÂNCIA
instanceName = sys.argv[3].split("/")[-1]

# CRIA O ARQUIVO JSON FINAL A SER ESCRITO EM UM ARQUIVO DE SAÍDA
outputJson = {"name": instanceName, "vehicles": vehicles}
with open(sys.argv[3], "w") as outputFile:
    json.dump(outputJson, outputFile)
