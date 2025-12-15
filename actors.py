from qiskit import QuantumCircuit, transpile, ClassicalRegister
from qiskit_aer import Aer
import random


class Person():
    def __init__(self, name):

        # Inicializa un actor del protocolo BB84.
        self.name = name
        self.bits = []  # Almacena los bits (0 o 1)
        self.bases = []  # Almacena las bases usadas ('Z' o 'X')
    
    def choose_random_basis(self):

        basis = random.choice(['Z', 'X'])
        return basis
    
    def measure_qubit(self, qc):
        n = qc.num_qubits
        measurement_circuit = qc.copy()
        bases = []
        
        for i in range(n):
            basis = self.choose_random_basis()
            bases.append(basis)
            
            if basis == 'X':
                measurement_circuit.h(i)
        
        for i in range(n):
            measurement_circuit.measure(i, i)
        
        backend = Aer.get_backend('aer_simulator')
        result = backend.run(measurement_circuit, shots=1).result()
        counts = result.get_counts()
        
        measured_string = list(counts.keys())[0]
        measured_bits = [int(bit) for bit in reversed(measured_string)]
        
        return measured_bits, bases
    
    def store_measurement(self, bit, basis):
        self.bits.append(bit)
        self.bases.append(basis)
    
    def get_bits(self):
        return self.bits
    
    def get_bases(self):
        return self.bases
    
    def compare_bases(self, other_bases):
        matching_indices = []
        for i in range(len(self.bases)):
            if self.bases[i] == other_bases[i]:
                matching_indices.append(i)
        return matching_indices
    
    def sift_key(self, matching_indices):
        self.bits = [self.bits[i] for i in matching_indices]
        self.bases = [self.bases[i] for i in matching_indices]
    
    def extract_bits(self, indices):
        return [self.bits[i] for i in indices]
    
    def reset(self):
        self.bits = []
        self.bases = []


class Alice(Person):

    def prepare_key(self, length):

        #Prepara una clave secreta de bits y bases.
        for _ in range(length):
            bit = random.choice([0, 1])
            basis = self.choose_random_basis()
            self.store_measurement(bit, basis)
    
    def encode_qubit(self, index):
        #Codifica un solo qubit en un circuito cuántico según la base elegida.
        qc = QuantumCircuit(1)
        bit = self.bits[index]
        basis = self.bases[index]
        
        if basis == 'Z':
            if bit == 1:
                qc.x(0)
        elif basis == 'X':
            if bit == 0:
                qc.h(0)
            else:
                qc.x(0)
                qc.h(0)
        
        return qc
    
    def send_all_qubits(self):
        n = len(self.bits)
        qc = QuantumCircuit(n, n)
        
        for i in range(n):
            bit = self.bits[i]
            basis = self.bases[i]
            
            if basis == 'Z':
                if bit == 1:
                    qc.x(i)
            elif basis == 'X':
                if bit == 0:
                    qc.h(i)
                else:
                    qc.x(i)
                    qc.h(i)
        
        return qc

class Bob(Person):
    def receive_and_measure_all(self, qc):
        measured_bits, bases = self.measure_qubit(qc)
        self.bits = measured_bits
        self.bases = bases

class Eve(Person):
    def intercept_and_resend(self, qc):
        measured_bits, bases = self.measure_qubit(qc)
        self.bits = measured_bits
        self.bases = bases
        
        n = len(measured_bits)
        new_qc = QuantumCircuit(n, n)
        
        for i in range(n):
            bit = measured_bits[i]
            basis = bases[i]
            
            if basis == 'Z':
                if bit == 1:
                    new_qc.x(i)
            elif basis == 'X':
                if bit == 0:
                    new_qc.h(i)
                else:
                    new_qc.x(i)
                    new_qc.h(i)
        
        return new_qc
