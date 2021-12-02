import json
import sys
import random
import codecs
import math


def randomMode(routes, percentageRoutes, originalInstanceJson, deliveries, filoSolution):

    routesSaida = []
    routesSize = len(routes)
    numSelectedRoutes = math.ceil(routesSize * (percentageRoutes / 100))
    print(numSelectedRoutes)
    randomRoutes = random.sample(range(0, routesSize), numSelectedRoutes)
    randomModeInfo(filoSolution, randomRoutes)
    writeTableRelationToFile(routes, randomRoutes)
    for randomNumbers in randomRoutes:
        aux = routes[randomNumbers].split(" ")  # SEPARA AS ROTAS EM PONTOS

        for j in aux:
            if j != "":  # VERIFICA SE É UM NÚMERO
                routesSaida.append(deliveries[int(j) - 1])

    # COORDENADAS DEPOSITO
    originlng = originalInstanceJson["origin"]["lng"]
    originlat = originalInstanceJson["origin"]["lat"]
    writeRandomModeToFile(originlng, originlat, originalInstanceJson, routesSaida)
    

def randomModeInfo(filoSolution, randomRoutes):
    outputInfo = codecs.open(sys.argv[5] + "_info" + ".txt", "w", "utf-8")
    for randomNumbers in randomRoutes:
        outputInfo.write(f"{filoSolution[randomNumbers]}\n")

def writeTableRelationToFile(routes, randomRoutes):
    originalFileName = sys.argv[3].split("/")[-1]
    outputTable = codecs.open(sys.argv[5] + "_" + originalFileName + ".txt", "w", "utf-8")
    counter = 1
    for randomNumbers in randomRoutes:
        aux = routes[randomNumbers].split(" ")  # SEPARA AS ROTAS EM PONTOS

        for j in aux:
            if j != "":  # VERIFICA SE É UM NÚMERO
                outputTable.write(f"{counter}  {j}\n")
                counter += 1


def writeRandomModeToFile(originlng, originlat, originalInstanceJson, routesSaida):

    # CABECARIO DO ARQUIVO DE SAIDA
    output = codecs.open(sys.argv[5] + ".txt", "w", "utf-8")
    output.write(f"NAME : {originalInstanceJson['name']} \n")
    output.write(f"COMMENT : \n")
    output.write(f"TYPE : CVRP \n")
    output.write(f"DIMENSION : {len(routesSaida) + 1}\n")
    output.write(f"EDGE_WEIGHT_TYPE : EUC_2D \n")
    output.write(f"CAPACITY : {originalInstanceJson['vehicle_capacity']} \n")
    output.write(f"NODE_COORD_SECTION \n")
    output.write(f"1 {originlng} {originlat}\n")

    # COORDENADAS DAS ENTREGAS
    counter = 2
    for item in routesSaida:
        output.write(f"{counter} {item['point']['lng']} {item['point']['lat']} \n")
        counter += 1

    # SEÇÃO DE DEMANDA
    output.write(f"DEMAND_SECTION\n")
    output.write(f"1 0\n")
    counter = 2
    for item in routesSaida:
        output.write(f"{counter} {item['size']} \n")
        counter += 1

    # DEPOT SECTION E FINAL DO ARQUIVO
    output.write(f"DEPOT_SECTION\n")
    output.write(f"1\n-1\nEOF")


def main():
    if len(sys.argv) < 6:
        print("Parametros incorretos\n")
        print("Primeiro parametro: Porcentagem de rotas selecionadas\n")
        print("Segundo parametro: Tipo de rotina:\n1 - Aleatorio\n2 - Guloso\n")
        print("Terceiro parametro: Arquivo.vrp.sol\n")
        print("Quarto parametro: arquivo Instancia original\n")
        print("Quinto parametro: destino do arquivo gerado\n")
        sys.exit()

    percentageRoutes = int(sys.argv[1])
    routineType = int(sys.argv[2])
    filoSolutionPath = sys.argv[3]
    originalInstanceJsonPath = sys.argv[4]

    # LÊ VRP.SOL E DIVIDE POR QUEBRA DE LINHA
    filoSolution = open(filoSolutionPath, "r").read().split("\n")

    # LÊ A INSTÂNCIA DA LOGGI E GUARDA NA "originalInstanceJson"
    with open(originalInstanceJsonPath, "r") as data_file:
        json_data = data_file.read()
    originalInstanceJson = json.loads(json_data)

    # DELIVERIES DO ARQUIVO JSON LOGGI
    deliveries = originalInstanceJson["deliveries"]

    routes = []

    # GUARDA CADA ROTA
    for i in range(0, len(filoSolution) - 1):
        routes.append(filoSolution[i].split(":")[1])

    if routineType == 1:
        randomMode(routes, percentageRoutes, originalInstanceJson, deliveries, filoSolution)


if __name__ == "__main__":
    main()
