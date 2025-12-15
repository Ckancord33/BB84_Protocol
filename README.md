# Simulación del Protocolo BB84 en Qiskit

**Universidad del Valle**  
**Autor:** Nicolás Córdoba  
**Código:** 2343576  
**Proyecto:** Proyecto Final de Investigación - Computación Cuántica

---

## Descripción del Proyecto

Este proyecto implementa una simulación completa del **protocolo BB84** utilizando Qiskit, el framework de computación cuántica de IBM. BB84 es el primer protocolo de distribución cuántica de claves (QKD - Quantum Key Distribution) propuesto por Charles Bennett y Gilles Brassard en 1984.

### Propósito

El objetivo principal de este proyecto es crear una simulación interactiva del protocolo BB84 que permita:

- **Comprender** el funcionamiento teórico del protocolo mediante experimentación práctica
- **Visualizar** cómo Alice y Bob establecen una clave secreta compartida
- **Demostrar** la detección de escuchas (eavesdropping) mediante el análisis del QBER (Quantum Bit Error Rate)
- **Probar** diferentes escenarios: con/sin atacante, con/sin ruido, diferentes tamaños de clave
- **Verificar** que el protocolo realmente funciona según la teoría cuántica

---

## Estructura del Proyecto

El proyecto está implementado usando **Programación Orientada a Objetos** para mantener un código modular, reutilizable y fácil de entender.

### Archivos Principales

```
Proyecto Final BB84/
│
├── actors.py          # Clases de los actores (Alice, Bob, Eve)
├── protocol.py        # Clase del protocolo BB84
├── main.py           # Demostración del protocolo
├── test.py           # Pruebas de detección de Eva
└── README.md         # Este archivo
```

---

## Descripción de Archivos

### 1. `actors.py`

Define las clases de los actores que participan en el protocolo BB84.

#### **Clase `Person` (Clase Base)**

Clase padre que contiene la funcionalidad común a todos los actores.

**Atributos:**

- `name`: Nombre del actor
- `bits`: Lista de bits (0s y 1s)
- `bases`: Lista de bases utilizadas ('Z' o 'X')

**Métodos principales:**

- `choose_random_basis()`: Elige aleatoriamente base Z o X
- `measure_qubit(qc)`: Mide un circuito cuántico completo con bases aleatorias
- `store_measurement(bit, basis)`: Almacena un bit y su base
- `compare_bases(other_bases)`: Compara bases con otro actor y devuelve índices coincidentes
- `sift_key(matching_indices)`: Filtra bits según índices de bases coincidentes
- `extract_bits(indices)`: Extrae bits específicos por índice
- `get_bits()`, `get_bases()`: Obtienen bits y bases almacenados

#### **Clase `Alice(Person)`**

Representa al emisor que genera y envía la clave.

**Métodos específicos:**

- `prepare_key(length)`: Genera bits y bases aleatorios
- `send_all_qubits()`: Crea un circuito cuántico con todos los qubits codificados

**Codificación de estados:**

- Base Z, bit 0: |0⟩ (sin operación)
- Base Z, bit 1: |1⟩ (aplicar X)
- Base X, bit 0: |+⟩ (aplicar H)
- Base X, bit 1: |-⟩ (aplicar X, luego H)

#### **Clase `Bob(Person)`**

Representa al receptor que mide los qubits.

**Métodos específicos:**

- `receive_and_measure_all(qc)`: Recibe un circuito cuántico y lo mide con bases aleatorias

#### **Clase `Eve(Person)`**

Representa al atacante que intenta interceptar la comunicación.

**Métodos específicos:**

- `intercept_and_resend(qc)`: Implementa ataque intercept-resend
  1. Intercepta el circuito
  2. Mide todos los qubits con bases aleatorias
  3. Re-prepara un nuevo circuito basado en sus mediciones
  4. Reenvía el nuevo circuito a Bob

---

### 2. `protocol.py`

Define la clase `BB84Protocol` que coordina todo el protocolo.

#### **Clase `BB84Protocol`**

Orquesta la comunicación entre Alice, Bob y opcionalmente Eve.

**Parámetros de inicialización:**

- `n_qubits`: Número de qubits en la clave inicial
- `with_eve`: Booleano para incluir atacante (default: False)
- `noise_level`: Nivel de ruido del canal 0.0-1.0 (default: 0.0)

**Métodos principales:**

- `run()`: Ejecuta el protocolo completo

  1. Alice prepara la clave
  2. Alice codifica y envía qubits
  3. (Opcional) Eva intercepta, mide y reenvía
  4. (Opcional) Se aplica ruido al canal
  5. Bob recibe y mide
  6. Sifting de claves
  7. Verificación de errores

- `sift_keys()`: Compara bases de Alice y Bob, descarta bits con bases diferentes

- `verify_key(sample_fraction=0.5)`: Sacrifica una fracción de bits para verificar errores

  - Divide bits en muestra de verificación y clave final
  - Calcula QBER usando la muestra sacrificada

- `detect_eavesdropper(threshold=0.11)`: Determina si hay atacante según QBER

  - QBER < 11%: Canal seguro
  - QBER > 11%: Posible atacante

- `get_final_key()`: Devuelve las claves finales de Alice y Bob

- `get_statistics()`: Devuelve diccionario con todas las métricas

- `print_results(verbose=True)`: Imprime resultados formateados

- `_apply_noise(qc)`: Simula ruido del canal aplicando bit-flips aleatorios

---

### 3. `main.py`

Archivo principal de demostración del protocolo.

#### Ejecución

```bash
python main.py
```

#### Configuración

Dentro del archivo puedes modificar los parámetros:

```python
protocol = BB84Protocol(
    n_qubits=100,      # Número de qubits iniciales
    with_eve=True,     # True: con atacante, False: sin atacante
    noise_level=0.00   # 0.0 = sin ruido, 0.05 = 5% ruido
)
protocol.run()
protocol.detect_eavesdropper(threshold=0.11)  # Umbral de detección
protocol.print_results()
```

**Parámetros explicados:**

- `n_qubits`: Cuantos más qubits, mayor probabilidad de detectar a Eve
- `with_eve`: Simula presencia de atacante
- `noise_level`: Simula errores del canal (0.0 = perfecto, 0.1 = 10% error)
- `threshold`: QBER máximo tolerado (típicamente 11% para BB84)

#### Salida

El programa imprime:

- Configuración del protocolo
- Bits coincidentes después del sifting
- Eficiencia del protocolo
- QBER calculado
- Si se detectó atacante
- Longitud de clave final
- Si las claves de Alice y Bob coinciden

---

### 4. `test.py`

Archivo de pruebas estadísticas para evaluar la detección de Eva.

#### Ejecución

```bash
python test.py
```

Este archivo ejecuta automáticamente tres pruebas con diferentes cantidades de qubits:

- 50 qubits, 100 pruebas
- 100 qubits, 100 pruebas
- 200 qubits, 100 pruebas

**Modificar parámetros:** Puedes editar fácilmente las cantidades de qubits directamente en el archivo [test.py](test.py) en la sección `if __name__ == "__main__"` para probar con diferentes valores:

```python
# Ejemplo: cambiar a 300 qubits
test_eve_detection(n_qubits=300, threshold=0.11, k_trials=100)
```

#### Funcionalidad

`test.py` ejecuta múltiples simulaciones del protocolo **con Eva presente** y cuenta:

- Cuántas veces Eva fue detectada
- Cuántas veces Eva NO fue detectada
- QBER promedio, mínimo y máximo
- Tasa de detección

**Objetivo:** Demostrar que con suficientes qubits, Eva es detectada en prácticamente el 100% de los casos.

#### Función principal

- `test_eve_detection(n_qubits, threshold, k_trials)`:
  - Ejecuta k pruebas con Eva presente
  - Devuelve diccionario con estadísticas de detección
  - Imprime resultados formateados con QBER y tasas de detección

---

## Instalación y Requisitos

### Requisitos

- Python 3.8 o superior
- Qiskit
- Qiskit Aer

### Instalación

```bash
pip install qiskit qiskit-aer
```

---

## Cómo Funciona el Protocolo BB84

### Etapas del Protocolo

1. **Preparación (Alice)**

   - Alice genera bits aleatorios (0 o 1)
   - Alice elige bases aleatorias (Z o X) para cada bit
   - Alice codifica cada bit en un qubit según la base elegida

2. **Transmisión**

   - Alice envía los qubits a Bob a través del canal cuántico
   - (Si hay Eva) Eva intercepta, mide y reenvía
   - (Si hay ruido) El canal introduce errores aleatorios

3. **Medición (Bob)**

   - Bob elige bases aleatorias independientemente
   - Bob mide cada qubit con su base elegida

4. **Sifting (Tamizado)**

   - Alice y Bob comparan sus bases por canal clásico (público)
   - Descartan bits donde usaron bases diferentes
   - Quedan con ~50% de los bits originales

5. **Verificación de Errores**

   - Sacrifican la mitad de bits para verificar errores
   - Calculan QBER (tasa de error)
   - Si QBER > umbral: posible atacante

6. **Clave Final**
   - Si QBER es aceptable, usan la otra mitad como clave secreta
   - Si QBER es alto, abortan y reinician

### ¿Por Qué Funciona?

- **Sin Eva**: QBER ≈ 0% (solo ruido del canal)
- **Con Eva**: QBER ≈ 25%
  - Eva elige base incorrecta ~50% del tiempo
  - Cuando se equivoca, introduce error ~50% del tiempo
  - Total: 0.5 × 0.5 = 0.25 = 25%

La teoría cuántica garantiza que cualquier medición (por Eva) perturba el estado, introduciendo errores detectables.

---

## Ejemplos de Uso

### Ejemplo 1: Canal Seguro

```python
from protocol import BB84Protocol

protocol = BB84Protocol(n_qubits=100, with_eve=False)
protocol.run()
protocol.detect_eavesdropper()
protocol.print_results()
```

**Resultado esperado:** QBER ≈ 0%, claves idénticas

### Ejemplo 2: Con Atacante

```python
protocol = BB84Protocol(n_qubits=100, with_eve=True)
protocol.run()
protocol.detect_eavesdropper()
protocol.print_results()
```

**Resultado esperado:** QBER ≈ 25%, atacante detectado

### Ejemplo 3: Pruebas Estadísticas

```python
from test import test_eve_detection

results = test_eve_detection(n_qubits=100, threshold=0.11, k_trials=50)
print(f"Eva detectada: {results['detection_rate']:.1f}%")
```

**Resultado esperado:** Detección > 95%

---

## Resultados Esperados

### Sin Atacante

- Eficiencia de sifting: ~50%
- QBER: ~0-2%
- Detección: NO
- Claves: Idénticas

### Con Atacante (Eva)

- Eficiencia de sifting: ~50%
- QBER: ~23-27%
- Detección: SÍ
- Claves: Diferentes

### Con Ruido 5%

- Eficiencia de sifting: ~50%
- QBER: ~5%
- Detección: NO (bajo umbral)
- Claves: Casi idénticas

---

## Conclusiones

Este proyecto demuestra:

1. ✓ El protocolo BB84 funciona según la teoría
2. ✓ Eva es detectada con alta probabilidad
3. ✓ El QBER es un indicador confiable de seguridad
4. ✓ Con más qubits, la detección mejora
5. ✓ La computación cuántica permite seguridad demostrable

---

## Referencias

- Qiskit Documentation: https://qiskit.org/documentation/
- John Wiley & Sons, Inc., 2008, "Quantum Computing Explained (pp. 239-248: Quantum Cryptography)"
- "Cómo Mandar un Mensaje Secreto con Física Cuántica." YouTube, 21 de junio de 2019. https://www.youtube.com/watch?v=7R7dnT2043M

---

**Fecha:** Diciembre 2025
