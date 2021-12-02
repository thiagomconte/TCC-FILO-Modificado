import sys


def main():
    if len(sys.argv) < 6:
        print("Parametros incorretos\n")
        print("Primeiro parametro: Tabela de relacao\n")
        print("Segundo parametro: Arquivo info das rotas destruidas\n")
        print("Terceiro parametro: Solucao apos destroy and repair\n")
        print("Quarto parametro: Solucao original\n")
        print("Quinto parametro: Destino solucao integrada com destroy and repair\n")
        sys.exit()
 
    newFiloSolutionRoutesIndex = readNewSolutionIndex()
    print(newFiloSolutionRoutesIndex)
    print("########################################")
    # destroyedRoutes = readDestroyedRoutesIndex()
    destroyedRoutesPosition = readDestroyedRoutes()
    print(destroyedRoutesPosition) 
    print("########################################")
    tableRelation = readTableRelation()
    print(tableRelation)
    writeIntegrationFile(
        newFiloSolutionRoutesIndex,
        destroyedRoutesPosition,
        tableRelation,
    )


def readNewSolutionIndex():

    newFiloSolutionRoutes = []
    newFiloSolutionRoutesSaida = []
    newFiloSolutionPath = open(sys.argv[3], "r").read().split("\n")
    for i in range(0, len(newFiloSolutionPath) - 1):
        newFiloSolutionRoutes.append(newFiloSolutionPath[i].split(":")[1])

    for route in newFiloSolutionRoutes:
        aux = route.split(" ")  # SEPARA AS ROTAS EM PONTOS

        for j in aux:
            if j != "":  # VERIFICA SE É UM NÚMERO
                newFiloSolutionRoutesSaida.append(int(j))
        newFiloSolutionRoutesSaida.append(-1)

    return newFiloSolutionRoutesSaida


def readDestroyedRoutes():
    destroyedRoutes = []
    destroyedRoutesPosition = []
    destroyedPath = open(sys.argv[2], "r").read().split("\n")
    for i in range(0, len(destroyedPath) - 1):
        destroyedRoutes.append(destroyedPath[i].split(":")[0])

    for route in destroyedRoutes:
        aux = route.split("#")[1]  # SEPARA AS ROTAS EM PONTOS
        destroyedRoutesPosition.append(int(aux))

    return destroyedRoutesPosition


def readDestroyedRoutesIndex():
    destroyedRoutes = []
    destroyedRoutesSaida = []
    destroyedPath = open(sys.argv[2], "r").read().split("\n")
    for i in range(0, len(destroyedPath) - 1):
        destroyedRoutes.append(destroyedPath[i].split(":")[1])

    for route in destroyedRoutes:
        aux = route.split(" ")  # SEPARA AS ROTAS EM PONTOS

        for j in aux:
            if j != "":  # VERIFICA SE É UM NÚMERO
                destroyedRoutesSaida.append(int(j))

    return destroyedRoutesSaida


def readTableRelation():
    with open(sys.argv[1]) as f:
        tableRelation = []
        for line in f:  # read rest of lines
            tableRelation.append([int(x) for x in line.split()])

        return tableRelation


def writeIntegrationFile(
    newFiloSolutionRoutesIndex, destroyedRoutesPosition, tableRelation
):
    counter = 1
    with open(sys.argv[4], "r") as firstfile, open(sys.argv[5], "w") as secondfile:
        for line in firstfile:
            if counter in destroyedRoutesPosition: #ROTAS QUE FORAM DESTRUIDAS
                aux = 0
                secondfile.write(f"Route #{counter}:")
                for item in newFiloSolutionRoutesIndex: #SOLUCAO FILO DAR
                    if item < 0:
                        newFiloSolutionRoutesIndex[aux] = 0 
                        break
                    else:
                        for i in range(0, len(tableRelation)):
                            if item == tableRelation[i][0]:
                                secondfile.write(f" {tableRelation[i][1]}")
                                newFiloSolutionRoutesIndex[aux] = 0                
                    aux+=1            
                secondfile.write("\n")
            else:
                secondfile.write(line)
            counter += 1


if __name__ == "__main__":
    main()
