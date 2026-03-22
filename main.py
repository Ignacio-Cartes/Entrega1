import sys


def get_instance_files(instance: str) -> tuple[str, str]:
    """
    Retorna los nombres de archivos de tareas y recursos
    según la instancia elegida.
    """
    if instance == "1":
        return "tareas.txt", "recursos.txt"
    if instance == "2":
        return "tareas_2.txt", "recursos_2.txt"

    raise ValueError("Instancia no válida. Usa '1' o '2'.")


def load_tasks(filename: str) -> list[dict]:
    """
    Lee tareas desde archivo y las retorna como una lista de diccionarios.
    Cada tarea tiene: id, duration, category.
    """
    tasks: list[dict] = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            parts = line.split(",")
            task = {
                "id": parts[0],
                "duration": int(parts[1]),
                "category": parts[2],
            }
            tasks.append(task)

    return tasks

def load_resources(filename: str) -> list[dict]:
    """
    Lee recursos desde archivo y los retorna como lista de diccionarios.
    Cada recurso tiene: id, categories.
    """
    resources: list[dict] = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            parts = line.split(",")
            resource = {
                "id": parts[0],
                "categories": parts[1:],
            }
            resources.append(resource)

    return resources


def get_task_categories(tasks: list[dict]) -> set[str]:
    categories: set[str] = set()

    for task in tasks:
        categories.add(task["category"])

    return categories


def get_resource_categories(resources: list[dict]) -> set[str]:
    categories: set[str] = set()

    for resource in resources:
        for category in resource["categories"]:
            categories.add(category)

    return categories


def compatible_resources_count(task: dict, resources: list[dict]) -> int:
    count = 0

    for resource in resources:
        if task["category"] in resource["categories"]:
            count += 1

    return count


def analyze_tasks_by_category(tasks: list[dict]) -> dict[str, int]:
    result: dict[str, int] = {}

    for task in tasks:
        category = task["category"]
        result[category] = result.get(category, 0) + 1

    return result


def analyze_resources_by_category(resources: list[dict]) -> dict[str, int]:
    result: dict[str, int] = {}

    for resource in resources:
        for category in resource["categories"]:
            result[category] = result.get(category, 0) + 1

    return result


def get_longest_tasks(tasks: list[dict], top_n: int = 5) -> list[dict]:
    return sorted(tasks, key=lambda task: task["duration"], reverse=True)[:top_n]


def get_most_restrictive_tasks(tasks: list[dict], resources: list[dict], top_n: int = 5) -> list[tuple[str, int, str]]:
    restrictive_tasks: list[tuple[str, int, str]] = []

    for task in tasks:
        count = compatible_resources_count(task, resources)
        restrictive_tasks.append((task["id"], count, task["category"]))

    restrictive_tasks.sort(key=lambda item: item[1])
    return restrictive_tasks[:top_n]


def get_duration_stats(tasks: list[dict]) -> tuple[int, int, float]:
    durations = [task["duration"] for task in tasks]

    minimum = min(durations)
    maximum = max(durations)
    average = sum(durations) / len(durations)

    return minimum, maximum, average


def print_analysis(tasks: list[dict], resources: list[dict], instance: str) -> None:
    print(f"\n=== ANÁLISIS DE LA INSTANCIA {instance} ===")

    print("\n--- RESUMEN GENERAL ---")
    print(f"Cantidad de tareas: {len(tasks)}")
    print(f"Cantidad de recursos: {len(resources)}")

    task_categories = get_task_categories(tasks)
    resource_categories = get_resource_categories(resources)

    print(f"Categorías en tareas: {sorted(task_categories)}")
    print(f"Categorías en recursos: {sorted(resource_categories)}")

    print("\n--- ESTADÍSTICAS DE DURACIÓN ---")
    minimum, maximum, average = get_duration_stats(tasks)
    print(f"Duración mínima: {minimum}")
    print(f"Duración máxima: {maximum}")
    print(f"Duración promedio: {average:.2f}")

    print("\n--- TAREAS MÁS LARGAS ---")
    for task in get_longest_tasks(tasks):
        print(f"{task['id']} | duración={task['duration']} | categoría={task['category']}")

    print("\n--- TAREAS POR CATEGORÍA ---")
    tasks_by_category = analyze_tasks_by_category(tasks)
    for category, count in sorted(tasks_by_category.items()):
        print(f"{category}: {count}")

    print("\n--- RECURSOS POR CATEGORÍA ---")
    resources_by_category = analyze_resources_by_category(resources)
    for category, count in sorted(resources_by_category.items()):
        print(f"{category}: {count}")

    print("\n--- TAREAS MÁS RESTRICTIVAS ---")
    for task_id, count, category in get_most_restrictive_tasks(tasks, resources):
        print(f"{task_id} | categoría={category} | recursos compatibles={count}")

    print("\n--- ALERTAS ---")
    tasks_without_resource: list[str] = []

    for task in tasks:
        count = compatible_resources_count(task, resources)
        if count == 0:
            tasks_without_resource.append(task["id"])

    if tasks_without_resource:
        print("Tareas sin recurso compatible:")
        for task_id in tasks_without_resource:
            print(f"- {task_id}")
    else:
        print("Todas las tareas tienen al menos un recurso compatible.")       


def sort_tasks_by_duration(tasks: list[dict]) -> list[dict]:
    """
    Ordena las tareas de mayor a menor duración.
    Complejidad: O(n log n)
    """
    return sorted(tasks, key=lambda task: task["duration"], reverse=True)


def initialize_resource_loads(resources: list[dict]) -> dict[str, int]:
    """
    Inicializa la carga de cada recurso en 0.
    """
    resource_loads: dict[str, int] = {}

    for resource in resources:
        resource_loads[resource["id"]] = 0

    return resource_loads


def select_least_loaded_compatible_resource(
    task: dict, resources: list[dict], resource_loads: dict[str, int]
) -> dict:
    """
    Selecciona el recurso compatible con menor carga actual.
    Si no existe recurso compatible, lanza error.
    Complejidad por tarea: O(m)
    """
    selected_resource: dict | None = None
    selected_load: int | None = None

    for resource in resources:
        if task["category"] not in resource["categories"]:
            continue

        current_load = resource_loads[resource["id"]]

        if selected_resource is None or current_load < selected_load:
            selected_resource = resource
            selected_load = current_load

    if selected_resource is None:
        raise ValueError(
            f"La tarea {task['id']} no tiene recursos compatibles."
        )

    return selected_resource


def schedule_tasks(tasks: list[dict], resources: list[dict]) -> tuple[list[dict], dict[str, int], int]:
    """
    Construye una planificación greedy:
    - ordena tareas por duración descendente
    - asigna cada tarea al recurso compatible menos cargado

    Retorna:
    - lista de asignaciones
    - cargas finales por recurso
    - makespan final
    """
    sorted_tasks = sort_tasks_by_duration(tasks)
    resource_loads = initialize_resource_loads(resources)
    assignments: list[dict] = []

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
            "category": task["category"],
        }
        assignments.append(assignment)

        resource_loads[resource_id] = end_time

    makespan = max(resource_loads.values()) if resource_loads else 0

    return assignments, resource_loads, makespan


def print_schedule(assignments: list[dict], resource_loads: dict[str, int], makespan: int) -> None:
    """
    Imprime la planificación generada.
    """
    print("\n=== PLANIFICACIÓN GREEDY ===")
    print("\n--- ASIGNACIONES ---")

    for assignment in assignments:
        print(
            f"{assignment['task_id']} | "
            f"recurso={assignment['resource_id']} | "
            f"inicio={assignment['start']} | "
            f"fin={assignment['end']} | "
            f"duración={assignment['duration']}"
        )

    print("\n--- CARGA FINAL POR RECURSO ---")
    for resource_id, load in sorted(resource_loads.items()):
        print(f"{resource_id}: {load}")

    print("\n--- MAKESPAN ---")
    print(f"Makespan final: {makespan}")


def write_output(assignments: list[dict], filename: str = "output.txt") -> None:
    """
    Escribe la solución en formato de salida:
    ID_Tarea,ID_Recurso,Tiempo_Inicio,Tiempo_Fin
    """
    with open(filename, "w", encoding="utf-8") as file:
        for assignment in assignments:
            line = (
                f"{assignment['task_id']},"
                f"{assignment['resource_id']},"
                f"{assignment['start']},"
                f"{assignment['end']}\n"
            )
            file.write(line)


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: python main.py <instancia>")
        print("Ejemplo: python main.py 1")
        return

    instance = sys.argv[1]

    try:
        tasks_file, resources_file = get_instance_files(instance)
    except ValueError as error:
        print(error)
        return

    tasks = load_tasks(tasks_file)
    resources = load_resources(resources_file)

    print_analysis(tasks, resources, instance)

    assignments, resource_loads, makespan = schedule_tasks(tasks, resources)

    print_schedule(assignments, resource_loads, makespan)
    write_output(assignments)

    print("\nSe generó el archivo output.txt")


if __name__ == "__main__":
    main()