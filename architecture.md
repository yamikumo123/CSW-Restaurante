# Arquitectura del Sistema POS - Restaurante

## Diagrama de Componentes y Capas

```mermaid
graph TD
    UI[src/ui/ - Interfaz CLI] --> Services[src/services/ - Servicios POS]
    Services --> Domain[src/domain/ - Modelos y Excepciones]
    Services --> Data[src/services/data_manager.py - Persistencia]
    Data --> JSON[(ventas.json)]