import json
import sys
import random
import codecs


def randomMode(routes, percentageRoutes, originalInstanceFilo, filoSolution):

    routesSaida = []
    routesSize = len(routes)
    numSelectedRoutes = round(routesSize * (percentageRoutes / 100))
    randomRoutes = random.sample(range(0, routesSize), numSelectedRoutes)
    randomModeInfo(filoSolution, randomRoutes)
    writeTableRelationToFile(routes, randomRoutes)
    for randomNumbers in randomRoutes:
        aux = routes[randomNumbers].split(" ")  # SEPARA AS ROTAS EM PONTOS

        for j in aux:
            if j != "":  # VERIFICA SE É UM NÚMERO
                points = { "lng": originalInstanceFilo[int(j) + 7].split("\t")[1],  "lat": originalInstanceFilo[int(j) + 7].split("\t")[2]}
                routesSaida.append(points)

    writeRandomModeToFile(originlng, originlat, originalInstanceFilo, routesSaida)
    

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


def writeRandomModeToFile(originlng, originlat, originalInstanceFilo, routesSaida):

    # CABECARIO DO ARQUIVO DE SAIDA
    output = codecs.open(sys.argv[5] + ".txt", "w", "utf-8")
    output.write(f"NAME : {originalInstanceFilo['name']} \n")
    output.write(f"COMMENT : \n")
    output.write(f"TYPE : CVRP \n")
    output.write(f"DIMENSION : {len(routesSaida) + 1}\n")
    output.write(f"EDGE_WEIGHT_TYPE : EUC_2D \n")
    output.write(f"CAPACITY : {originalInstanceFilo['vehicle_capacity']} \n")
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
    originalInstanceFiloPath = sys.argv[4]

    # LÊ VRP.SOL E DIVIDE POR QUEBRA DE LINHA
    filoSolution = open(filoSolutionPath, "r").read().split("\n")

    # LÊ A INSTÂNCIA DO FILO E GUARDA NA "originalInstanceFilo"
    originalInstanceFilo = open(originalInstanceFiloPath, "r").read().split("\n")

    # routes = []

    # # GUARDA CADA ROTA
    # for i in range(0, len(filoSolution) - 1):
    #     routes.append(filoSolution[i].split(":")[1])

    # if routineType == 1:
    #     randomMode(routes, percentageRoutes, originalInstanceFilo, filoSolution)


if __name__ == "__main__":
    main()
