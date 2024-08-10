class DFA:
    def __init__(self, estados, alfabeto, f_transicion, e_inicial, e_aceptacion):
        self.estados = estados
        self.alfabeto = alfabeto
        self.f_transicion = f_transicion
        self.e_inicial = e_inicial
        self.e_aceptacion = e_aceptacion

    def minimizacion(self):
        # Inicializar estructuras de datos
        equivalencias = {}  # Diccionario para marcar la equivalencia de pares de estados
        transiciones = {}   # Diccionario para almacenar transiciones para cada par de estados
        registros_verificacion = []  # Lista para registrar todos los pasos de verificación

        # Inicializar la tabla de transiciones para cada par de estados y cada símbolo del alfabeto
        for p in self.estados:
            for q in self.estados:
                if p < q:  # Solo considerar pares únicos (p, q) con p < q
                    equivalencias[(p, q)] = True  # Asumir inicialmente que son equivalentes
                    transiciones[(p, q)] = {}
                    for simbolo in self.alfabeto:
                        p_destino = self.f_transicion[p][simbolo]
                        q_destino = self.f_transicion[q][simbolo]
                        transiciones[(p, q)][simbolo] = (p_destino, q_destino)

        # Primera verificación: Diferenciar estados de aceptación
        for (p, q) in equivalencias:
            if (p in self.e_aceptacion) != (q in self.e_aceptacion):
                equivalencias[(p, q)] = False  # Los estados p y q no son equivalentes si uno es de aceptación y el otro no

        # Registro de pasos y verificaciones
        paso = 0
        while True:
            paso += 1
            cambios_realizados = False

            # Crear una copia de los pares de equivalencias para evitar modificar el diccionario durante la iteración
            pares_a_verificar = list(equivalencias.keys())
            for (p, q) in pares_a_verificar:
                if equivalencias[(p, q)]:  # Solo verificar pares aún considerados equivalentes
                    paso_info = {
                        'paso': paso,
                        'par_estado': (p, q),
                        'verificaciones': []
                    }

                    # Verificar con cada símbolo del alfabeto
                    for simbolo in self.alfabeto:
                        p_destino = self.f_transicion[p][simbolo]
                        q_destino = self.f_transicion[q][simbolo]
                        par_destino = (min(p_destino, q_destino), max(p_destino, q_destino))

                        verificacion_info = {
                            'simbolo': simbolo,
                            'p_destino': p_destino,
                            'q_destino': q_destino,
                            'par_destino': par_destino,
                            'es_equivalente': equivalencias.get(par_destino, True)
                        }
                        paso_info['verificaciones'].append(verificacion_info)

                        # Verificar si el par de destinos ha sido marcado como no equivalente
                        if not equivalencias.get(par_destino, True):
                            equivalencias[(p, q)] = False
                            cambios_realizados = True
                            break  # No es necesario verificar más símbolos para este par
                    if not equivalencias[(p, q)]:
                        registros_verificacion.append(paso_info)
                        break  # Salir del bucle de símbolos si ya se marcó el par como no equivalente

            # Si no se realizaron cambios, salir del bucle
            if not cambios_realizados:
                break

        # Recopilar pares equivalentes
        pares_equivalentes = []
        for (p, q), son_equivalentes in equivalencias.items():
            if son_equivalentes:
                pares_equivalentes.append((p, q))  # Agregar los pares equivalentes a la lista

        # Devolver el resultado de la minimización y el registro de pasos
        return pares_equivalentes, registros_verificacion

def leer_dfa_desde_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as file:
            num_casos = int(file.readline().strip())
            for _ in range(num_casos):
                num_estados = int(file.readline().strip())
                alfabeto = file.readline().strip().split()
                estados_aceptacion = set(map(int, file.readline().strip().split()))
                f_transicion = {}
                for i in range(num_estados):
                    transiciones = list(map(int, file.readline().strip().split()))
                    f_transicion[i] = dict(zip(alfabeto, transiciones))
                dfa = DFA(
                    estados=set(range(num_estados)),
                    alfabeto=alfabeto,
                    f_transicion=f_transicion,
                    e_inicial=0,
                    e_aceptacion=estados_aceptacion
                )
                pares_equivalentes, registros_verificacion = dfa.minimizacion()
                # Aquí se puede hacer uso de los resultados y registros de verificación
                if pares_equivalentes:
                    print(" ".join(f"({p},{q})" for p, q in pares_equivalentes))
                else:
                    print("No hay pares equivalentes.")
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{nombre_archivo}'.")
    except ValueError as e:
        print(f"Error: Formato inválido en el archivo. {str(e)}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

# Uso del programa
nombre_archivo = 'input.txt'
leer_dfa_desde_archivo(nombre_archivo)
