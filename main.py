from protocol import BB84Protocol


def main():
    """
    Ejecuta una simulación del protocolo BB84.
    
    Configura y ejecuta el protocolo con:
    - n_qubits: Número de qubits iniciales
    - with_eve: Si hay atacante interceptando
    - noise_level: Nivel de ruido del canal (0.0-1.0)
    - threshold: Umbral QBER para detectar atacante (típicamente 0.11)
    """
    protocol1 = BB84Protocol(n_qubits=100, with_eve=True, noise_level=0.00)
    protocol1.run()
    protocol1.detect_eavesdropper(threshold=0.11)
    protocol1.print_results()

if __name__ == "__main__":
    main()
