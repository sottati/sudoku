# Branch and Bound
# Hay que definir las cotas, definir estrategias etc etc etc
# dejo escrito el pseudocodigo igual q en backtracking

def branchAndBound():
    env = inicializarEstructura()
    nodoRaiz = crearNodoRaiz()
    agregar(env, nodoRaiz)
    cota = actualizarCota(cota, nodoRaiz)
    mejorSolucion = null
    while env !== vacio: # este vacio tenemos q definir q seria, si long = 0 o un conjunto vacio, ni idea
        nodo = primero(env)
        if !podar(nodo, cota):
            hijos = generarHijos(nodo)
            for hijo in hijos:
                if !podar(hijo, cota):
                    if esSolucion(hijo):
                        if esMejor(mejorSolucion, hijo):
                            mejorSolucion = hijo
                            cota = actualizarCota(cota, hijo)
                        else:
                            agregar(env, hijo)
                            cota = actualizarCota(cota, hijo)
                        