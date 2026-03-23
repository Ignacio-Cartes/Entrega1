# Entrega 1

## Diagrama del flujo general

```mermaid
flowchart TD
    A[main]
    B[Cargar archivos]
    C[Analizar tareas y recursos]
    D[Ordenar tareas]
    E[Asignar greedy al recurso compatible menos cargado]
    F[Calcular makespan]
    G[Mostrar y guardar salida]

    A --> B --> C --> D --> E --> F --> Ggit