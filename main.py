import sys
<<<<<<< HEAD
from typing import List, Dict, Tuple, Set


def get_instance_files(instance: str) -> Tuple[str, str]:
=======
from typing import List, Dict, Tuple, Set, Optional


def get_instance_files(instance: str) -> Tuple[str, str]:
    """
    Retorna los archivos de tareas y recursos según la instancia.
    """
>>>>>>> 8037717b9a2f53165763a8ee06b874ca43a9f7ee
    if instance == "1":
        return "tareas.txt", "recursos.txt"
    elif instance == "2":
        return "tareas_2.txt", "recursos_2.txt"
    else:
<<<<<<< HEAD
        raise ValueError("Instancia no válida. Usa '1' o '2'.")


def load_tasks(filename: str) -> List[Dict]:
=======
        raise ValueError("Instancia no válida. Usa '1', '2' o 'all'.")


def load_tasks(filename: str) -> List[Dict]:
    """
    Lee tareas desde archivo.
    Formato esperado por línea: ID_TAREA,DURACION,CATEGORIA
    """
>>>>>>> 8037717b9a2f53165763a8ee06b874ca43a9f7ee
    tasks = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            parts = [part.strip() for part in line.split(",")]

            if len(parts) < 3:
                continue

            task = {
                "id": parts[0],
                "duration": int(parts[1]),
                "category": parts[2]
            }
            tasks.append(task)

    return tasks


def load_resources(filename: str) -> List[Dict]:
<<<<<<< HEAD
=======
    """
    Lee recursos desde archivo.
    Formato esperado por línea: ID_RECURSO,CAT1,CAT2,...
    """
>>>>>>> 8037717b9a2f53165763a8ee06b874ca43a9f7ee
    resources = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            parts = [part.strip() for part in line.split(",")]

            if len(parts) < 2:
                continue

            resource = {
                "id": parts[0],
                "categories": parts[1:]
            }
            resources.append(resource)

    return resources


def get_task_categories(tasks: List[Dict]) -> Set[str]:
    categories = set()

    for task in tasks:
        categories.add(task["category"])

    return categories


def get_resource_categories(resources: List[Dict]) -> Set[str]:
    categories = set()

    for resource in resources:
        for category in resource["categories"]:
            categories.add(category)

    return categories


def compatible_resources_count(task: Dict, resources: List[Dict]) -> int:
    count = 0

    for resource in resources:
        if task["category"] in resource["categories"]:
            count += 1

    return count


def analyze_tasks_by_category(tasks: List[Dict]) -> Dict[str, int]:
    result = {}

    for task in tasks:
        category = task["category"]
        result[category] = result.get(category, 0) + 1

    return result


def analyze_resources_by_category(resources: List[Dict]) -> Dict[str, int]:
    result = {}

    for resource in resources:
        for category in resource["categories"]:
            result[category] = result.get(category, 0) + 1

    return result


def get_longest_tasks(tasks: List[Dict], top_n: int = 5) -> List[Dict]:
    return sorted(tasks, key=lambda task: task["duration"], reverse=True)[:top_n]


def get_most_restrictive_tasks(
    tasks: List[Dict],
    resources: List[Dict],
    top_n: int = 5
) -> List[Tuple[str, int, str]]:
    restrictive_tasks = []

    for task in tasks:
        count = compatible_resources_count(task, resources)
        restrictive_tasks.append((task["id"], count, task["category"]))

    restrictive_tasks.sort(key=lambda x: x[1])
    return restrictive_tasks[:top_n]


def get_duration_stats(tasks: List[Dict]) -> Tuple[int, int, float]:
    durations = [task["duration"] for task in tasks]

    minimum = min(durations)
    maximum = max(durations)
    average = sum(durations) / len(durations)

    return minimum, maximum, average


def get_tasks_without_resource(tasks: List[Dict], resources: List[Dict]) -> List[str]:
    result = []

    for task in tasks:
        if compatible_resources_count(task, resources) == 0:
            result.append(task["id"])

    return result


def print_analysis(tasks: List[Dict], resources: List[Dict], instance: str) -> None:
    print("\n" + "=" * 70)
    print("ANÁLISIS DE LA INSTANCIA {}".format(instance))
    print("=" * 70)

    print("\n--- RESUMEN GENERAL ---")
    print("Cantidad de tareas: {}".format(len(tasks)))
    print("Cantidad de recursos: {}".format(len(resources)))

    task_categories = sorted(get_task_categories(tasks))
    resource_categories = sorted(get_resource_categories(resources))

    print("Categorías en tareas: {}".format(task_categories))
    print("Categorías en recursos: {}".format(resource_categories))

    print("\n--- ESTADÍSTICAS DE DURACIÓN ---")
    minimum, maximum, average = get_duration_stats(tasks)
    print("Duración mínima: {}".format(minimum))
    print("Duración máxima: {}".format(maximum))
    print("Duración promedio: {:.2f}".format(average))

    print("\n--- TAREAS MÁS LARGAS ---")
    for task in get_longest_tasks(tasks):
        print(
            "{} | duración={} | categoría={}".format(
                task["id"], task["duration"], task["category"]
            )
        )

    print("\n--- TAREAS POR CATEGORÍA ---")
    tasks_by_category = analyze_tasks_by_category(tasks)
    for category, count in sorted(tasks_by_category.items()):
        print("{}: {}".format(category, count))

    print("\n--- RECURSOS POR CATEGORÍA ---")
    resources_by_category = analyze_resources_by_category(resources)
    for category, count in sorted(resources_by_category.items()):
        print("{}: {}".format(category, count))

    print("\n--- TAREAS MÁS RESTRICTIVAS ---")
    for task_id, count, category in get_most_restrictive_tasks(tasks, resources):
        print(
            "{} | categoría={} | recursos compatibles={}".format(
                task_id, category, count
            )
        )

    print("\n--- ALERTAS ---")
    tasks_without_resource = get_tasks_without_resource(tasks, resources)

    if tasks_without_resource:
        print("Tareas sin recurso compatible:")
        for task_id in tasks_without_resource:
            print("- {}".format(task_id))
    else:
        print("Todas las tareas tienen al menos un recurso compatible.")


def sort_tasks_by_duration(tasks: List[Dict]) -> List[Dict]:
<<<<<<< HEAD
=======
    """
    Ordena tareas de mayor a menor duración.
    Complejidad: O(n log n)
    """
>>>>>>> 8037717b9a2f53165763a8ee06b874ca43a9f7ee
    return sorted(tasks, key=lambda task: task["duration"], reverse=True)


def initialize_resource_loads(resources: List[Dict]) -> Dict[str, int]:
<<<<<<< HEAD
=======
    """
    Inicializa la carga de cada recurso en 0.
    """
>>>>>>> 8037717b9a2f53165763a8ee06b874ca43a9f7ee
    resource_loads = {}

    for resource in resources:
        resource_loads[resource["id"]] = 0

    return resource_loads


def select_least_loaded_compatible_resource(
    task: Dict,
    resources: List[Dict],
    resource_loads: Dict[str, int]
) -> Dict:
<<<<<<< HEAD
=======
    """
    Selecciona el recurso compatible con menor carga actual.
    Complejidad por tarea: O(m)
    """
>>>>>>> 8037717b9a2f53165763a8ee06b874ca43a9f7ee
    selected_resource = None
    selected_load = None

    for resource in resources:
        if task["category"] not in resource["categories"]:
            continue

        current_load = resource_loads[resource["id"]]

        if selected_resource is None or current_load < selected_load:
            selected_resource = resource
            selected_load = current_load

    if selected_resource is None:
        raise ValueError("La tarea {} no tiene recursos compatibles.".format(task["id"]))

    return selected_resource


def schedule_tasks(tasks: List[Dict], resources: List[Dict]) -> Tuple[List[Dict], Dict[str, int], int]:
<<<<<<< HEAD
=======
    """
    Planificación greedy:
    - ordena tareas por duración descendente
    - asigna cada tarea al recurso compatible menos cargado

    Retorna:
    - assignments
    - cargas finales por recurso
    - makespan
    """
>>>>>>> 8037717b9a2f53165763a8ee06b874ca43a9f7ee
    sorted_tasks = sort_tasks_by_duration(tasks)
    resource_loads = initialize_resource_loads(resources)
    assignments = []

    for task in sorted_tasks:
        resource = select_least_loaded_compatible_resource(task, resources, resource_loads)

        resource_id = resource["id"]
        start_time = resource_loads[resource_id]
        end_time = start_time + task["duration"]

        assignment = {
            "task_id": task["id"],
            "resource_id": resource_id,
            "start": start_time,
            "end": end_time,
            "duration": task["duration"],
            "category": task["category"]
        }

        assignments.append(assignment)
        resource_loads[resource_id] = end_time

    makespan = max(resource_loads.values()) if resource_loads else 0

    return assignments, resource_loads, makespan


def print_schedule(
    assignments: List[Dict],
    resource_loads: Dict[str, int],
    makespan: int,
<<<<<<< HEAD
    instance: str,
    objective_makespan: int
=======
    instance: str
>>>>>>> 8037717b9a2f53165763a8ee06b874ca43a9f7ee
) -> None:
    print("\n--- PLANIFICACIÓN GREEDY INSTANCIA {} ---".format(instance))

    print("\nASIGNACIONES:")
    for assignment in assignments:
        print(
            "{} | recurso={} | inicio={} | fin={} | duración={} | categoría={}".format(
                assignment["task_id"],
                assignment["resource_id"],
                assignment["start"],
                assignment["end"],
                assignment["duration"],
                assignment["category"]
            )
        )

    print("\nCARGA FINAL POR RECURSO:")
    for resource_id, load in sorted(resource_loads.items()):
        print("{}: {}".format(resource_id, load))

    print("\nMAKESPAN:")
    print("Makespan final instancia {}: {}".format(instance, makespan))
<<<<<<< HEAD
    print("Makespan objetivo instancia {}: {}".format(instance, objective_makespan))

    if makespan <= objective_makespan:
        print("Se cumplió el makespan objetivo.")
    else:
        print("No se cumplió el makespan objetivo.")


def write_output(assignments: List[Dict], filename: str) -> None:
=======


def write_output(assignments: List[Dict], filename: str) -> None:
    """
    Escribe la solución:
    ID_Tarea,ID_Recurso,Tiempo_Inicio,Tiempo_Fin
    """
>>>>>>> 8037717b9a2f53165763a8ee06b874ca43a9f7ee
    with open(filename, "w", encoding="utf-8") as file:
        for assignment in assignments:
            file.write(
                "{},{},{},{}\n".format(
                    assignment["task_id"],
                    assignment["resource_id"],
                    assignment["start"],
                    assignment["end"]
                )
            )


<<<<<<< HEAD
def process_instance(instance: str, objective_makespan: int) -> None:
=======
def process_instance(instance: str) -> None:
    """
    Ejecuta el flujo completo de una instancia.
    """
>>>>>>> 8037717b9a2f53165763a8ee06b874ca43a9f7ee
    tasks_file, resources_file = get_instance_files(instance)

    tasks = load_tasks(tasks_file)
    resources = load_resources(resources_file)

    print_analysis(tasks, resources, instance)

    assignments, resource_loads, makespan = schedule_tasks(tasks, resources)

<<<<<<< HEAD
    print_schedule(assignments, resource_loads, makespan, instance, objective_makespan)
=======
    print_schedule(assignments, resource_loads, makespan, instance)
>>>>>>> 8037717b9a2f53165763a8ee06b874ca43a9f7ee

    output_filename = "output_{}.txt".format(instance)
    write_output(assignments, output_filename)

    print("\nSe generó el archivo {}".format(output_filename))


def main() -> None:
<<<<<<< HEAD
    if len(sys.argv) == 2:
        try:
            makespan_1 = int(sys.argv[1])
        except ValueError:
            print("Uso para una instancia: python main.py <makespan_instancia_1>")
            return

        try:
            process_instance("1", makespan_1)
=======
    if len(sys.argv) < 2:
        print("Uso: python main.py <instancia>")
        print("Ejemplos:")
        print("  python main.py 1")
        print("  python main.py 2")
        print("  python main.py all")
        return

    instance = sys.argv[1].strip().lower()

    if instance == "all":
        for inst in ["1", "2"]:
            try:
                process_instance(inst)
            except ValueError as error:
                print(error)
                return
        return

    if instance in ["1", "2"]:
        try:
            process_instance(instance)
>>>>>>> 8037717b9a2f53165763a8ee06b874ca43a9f7ee
        except ValueError as error:
            print(error)
        return

<<<<<<< HEAD
    if len(sys.argv) == 3:
        try:
            makespan_1 = int(sys.argv[1])
            makespan_2 = int(sys.argv[2])
        except ValueError:
            print("Uso para ambas instancias: python main.py <makespan_1> <makespan_2>")
            return

        try:
            process_instance("1", makespan_1)
            process_instance("2", makespan_2)
        except ValueError as error:
            print(error)
        return

    print("Uso:")
    print("  python main.py <makespan_instancia_1>")
    print("  python main.py <makespan_instancia_1> <makespan_instancia_2>")
=======
    print("Instancia no válida. Usa '1', '2' o 'all'.")
>>>>>>> 8037717b9a2f53165763a8ee06b874ca43a9f7ee


if __name__ == "__main__":
    main()
    