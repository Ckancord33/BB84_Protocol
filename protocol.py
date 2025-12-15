from actors import Alice, Bob, Eve
import random


class BB84Protocol:
    def __init__(self, n_qubits, with_eve=False, noise_level=0.0):
        self.n_qubits = n_qubits
        self.with_eve = with_eve
        self.noise_level = noise_level
        
        self.alice = Alice("Alice")
        self.bob = Bob("Bob")
        self.eve = Eve("Eve") if with_eve else None
        
        self.matching_indices = []
        self.verification_sample = []
        self.final_key_indices = []
        self.qber = 0.0
        self.eavesdropper_detected = False
        
    def run(self):
        self.alice.prepare_key(self.n_qubits)
        
        quantum_channel = self.alice.send_all_qubits()
        
        if self.with_eve:
            quantum_channel = self.eve.intercept_and_resend(quantum_channel)
        
        if self.noise_level > 0:
            quantum_channel = self._apply_noise(quantum_channel)
        
        self.bob.receive_and_measure_all(quantum_channel)
        
        self.sift_keys()
        
        if len(self.alice.get_bits()) > 0:
            self.verify_key(sample_fraction=0.5)
    
    def sift_keys(self):
        self.matching_indices = self.alice.compare_bases(self.bob.get_bases())
        
        if self.with_eve and self.eve:
            alice_original_bases = self.alice.get_bases().copy()
            eve_matching = self.eve.compare_bases(alice_original_bases)
            self.eve.sift_key(eve_matching)
        
        self.alice.sift_key(self.matching_indices)
        self.bob.sift_key(self.matching_indices)
    
    def verify_key(self, sample_fraction=0.5):
        n_sifted = len(self.alice.get_bits())
        
        if n_sifted == 0:
            self.qber = 0.0
            return
        
        n_verify = int(n_sifted * sample_fraction)
        
        if n_verify == 0:
            n_verify = min(1, n_sifted)
        
        all_indices = list(range(n_sifted))
        random.shuffle(all_indices)
        
        self.verification_sample = all_indices[:n_verify]
        self.final_key_indices = all_indices[n_verify:]
        
        errors = 0
        alice_bits = self.alice.get_bits()
        bob_bits = self.bob.get_bits()
        
        for idx in self.verification_sample:
            if alice_bits[idx] != bob_bits[idx]:
                errors += 1
        
        self.qber = errors / len(self.verification_sample) if len(self.verification_sample) > 0 else 0.0
    
    def detect_eavesdropper(self, threshold=0.11):
        self.eavesdropper_detected = self.qber > threshold
        return self.eavesdropper_detected
    
    def get_final_key(self):
        alice_final = self.alice.extract_bits(self.final_key_indices)
        bob_final = self.bob.extract_bits(self.final_key_indices)
        
        return alice_final, bob_final
    
    def calculate_qber(self):
        return self.qber
    
    def get_statistics(self):
        alice_final, bob_final = self.get_final_key()
        
        stats = {
            'n_qubits_initial': self.n_qubits,
            'n_qubits_after_sifting': len(self.matching_indices),
            'sifting_efficiency': len(self.matching_indices) / self.n_qubits if self.n_qubits > 0 else 0,
            'n_bits_verified': len(self.verification_sample),
            'n_bits_final_key': len(self.final_key_indices),
            'qber': self.qber,
            'eavesdropper_detected': self.eavesdropper_detected,
            'with_eve': self.with_eve,
            'noise_level': self.noise_level,
            'alice_final_key': alice_final,
            'bob_final_key': bob_final,
            'keys_match': alice_final == bob_final
        }
        
        if self.with_eve and self.eve:
            eve_bits = self.eve.get_bits()
            stats['eve_bits'] = eve_bits[:20] if len(eve_bits) > 20 else eve_bits
            stats['eve_bases'] = self.eve.get_bases()[:20] if len(self.eve.get_bases()) > 20 else self.eve.get_bases()
        
        return stats
    
    def _apply_noise(self, qc):
        from qiskit.circuit.library import XGate
        
        n = qc.num_qubits
        noisy_qc = qc.copy()
        
        for i in range(n):
            if random.random() < self.noise_level:
                noisy_qc.x(i)
        
        return noisy_qc
    
    def print_results(self, verbose=True):
        stats = self.get_statistics()
        
        print(f"\n{'='*60}")
        print(f"RESULTADOS DEL PROTOCOLO BB84")
        print(f"{'='*60}\n")
        
        print(f"Configuración:")
        print(f"  - Qubits iniciales: {stats['n_qubits_initial']}")
        print(f"  - Con Eva: {'SÍ' if stats['with_eve'] else 'NO'}")
        print(f"  - Nivel de ruido: {stats['noise_level']*100:.1f}%\n")
        
        print(f"Después de Sifting (comparación de bases):")
        print(f"  - Bits coincidentes: {stats['n_qubits_after_sifting']}")
        print(f"  - Eficiencia: {stats['sifting_efficiency']*100:.1f}%\n")
        
        print(f"Verificación (sacrificio para detectar errores):")
        print(f"  - Bits sacrificados: {stats['n_bits_verified']}")
        print(f"  - QBER: {stats['qber']*100:.2f}%")
        print(f"  - Atacante detectado: {'✗ SÍ' if stats['eavesdropper_detected'] else '✓ NO'}\n")
        
        print(f"Clave Final:")
        print(f"  - Longitud: {stats['n_bits_final_key']} bits")
        
        if verbose and stats['n_bits_final_key'] <= 50:
            print(f"  - Alice: {stats['alice_final_key']}")
            print(f"  - Bob:   {stats['bob_final_key']}")
        elif verbose:
            print(f"  - Alice: {stats['alice_final_key'][:30]}... (mostrando primeros 30)")
            print(f"  - Bob:   {stats['bob_final_key'][:30]}... (mostrando primeros 30)")
        
        print(f"  - Claves idénticas: {'✓ SÍ' if stats['keys_match'] else '✗ NO'}\n")
        
        if self.with_eve and verbose:
            print(f"Información de Eva:")
            print(f"  - Bases (muestra): {stats['eve_bases']}")
            print(f"  - Bits (muestra): {stats['eve_bits']}\n")
        
        print(f"{'='*60}\n")
