from protocol import BB84Protocol


def test_eve_detection(n_qubits, threshold, k_trials):
    """
    Ejecuta k pruebas del protocolo BB84 con Eva presente.
    Cuenta cuántas veces Eva NO es detectada.
    
    Args:
        n_qubits: Número de qubits en la clave inicial
        threshold: Umbral de QBER para detectar atacante (típicamente 0.11)
        k_trials: Número de pruebas a realizar
    
    Returns:
        dict: Resultados con estadísticas de detección
    """
    eve_not_detected = 0
    eve_detected = 0
    qber_values = []
    
    print(f"\n{'='*70}")
    print(f"PRUEBA DE DETECCIÓN DE EVA")
    print(f"{'='*70}")
    print(f"Parámetros:")
    print(f"  - Qubits por prueba: {n_qubits}")
    print(f"  - Umbral de detección: {threshold*100:.1f}%")
    print(f"  - Número de pruebas: {k_trials}")
    print(f"\nEjecutando pruebas...")
    
    for i in range(k_trials):
        protocol = BB84Protocol(n_qubits=n_qubits, with_eve=True, noise_level=0.0)
        protocol.run()
        detected = protocol.detect_eavesdropper(threshold=threshold)
        qber = protocol.calculate_qber()
        
        qber_values.append(qber)
        
        if detected:
            eve_detected += 1
        else:
            eve_not_detected += 1
        
        if (i + 1) % 10 == 0:
            print(f"  Completadas {i + 1}/{k_trials} pruebas...")
    
    detection_rate = (eve_detected / k_trials) * 100
    avg_qber = sum(qber_values) / len(qber_values)
    min_qber = min(qber_values)
    max_qber = max(qber_values)
    
    print(f"\n{'='*70}")
    print(f"RESULTADOS")
    print(f"{'='*70}")
    print(f"\nEstadísticas de Detección:")
    print(f"  - Eva detectada: {eve_detected}/{k_trials} veces ({detection_rate:.1f}%)")
    print(f"  - Eva NO detectada: {eve_not_detected}/{k_trials} veces ({100-detection_rate:.1f}%)")
    print(f"\nEstadísticas de QBER:")
    print(f"  - QBER promedio: {avg_qber*100:.2f}%")
    print(f"  - QBER mínimo: {min_qber*100:.2f}%")
    print(f"  - QBER máximo: {max_qber*100:.2f}%")
    print(f"  - Umbral usado: {threshold*100:.1f}%")
    print(f"\n{'='*70}\n")
    
    results = {
        'n_qubits': n_qubits,
        'threshold': threshold,
        'k_trials': k_trials,
        'eve_detected': eve_detected,
        'eve_not_detected': eve_not_detected,
        'detection_rate': detection_rate,
        'avg_qber': avg_qber,
        'min_qber': min_qber,
        'max_qber': max_qber,
        'qber_values': qber_values
    }
    
    return results


if __name__ == "__main__":

    print("\nEjecutando pruebas con parámetros por defecto...\n")
    
    print("### PRUEBA 1: 50 qubits, 100 pruebas ###")
    test_eve_detection(n_qubits=50, threshold=0.11, k_trials=100)
    
    print("\n### PRUEBA 2: 100 qubits, 100 pruebas ###")
    test_eve_detection(n_qubits=100, threshold=0.11, k_trials=100)
    
    print("\n### PRUEBA 3: 200 qubits, 100 pruebas ###")
    test_eve_detection(n_qubits=200, threshold=0.11, k_trials=100)