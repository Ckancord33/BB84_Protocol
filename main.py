from protocol import BB84Protocol


def main():
    protocol1 = BB84Protocol(n_qubits=100, with_eve=True, noise_level=0.00)
    protocol1.run()
    protocol1.detect_eavesdropper(threshold=0.11)
    protocol1.print_results()

if __name__ == "__main__":
    main()
