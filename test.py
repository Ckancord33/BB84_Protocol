from actors import Alice, Bob, Eve

n_qubits = 30
WITH_EVE = True

alice = Alice("Alice")
bob = Bob("Bob")
eve = Eve("Eve")

print("=== PROTOCOLO BB84 - PRUEBA ===")
print(f"CON EVA: {'SÍ' if WITH_EVE else 'NO'}\n")

print("1. Alice prepara su clave secreta")
alice.prepare_key(n_qubits)
print(f"   Bits de Alice:  {alice.get_bits()}")
print(f"   Bases de Alice: {alice.get_bases()}\n")

print("2. Alice codifica y envía los qubits en un solo circuito")
quantum_channel = alice.send_all_qubits()
print(f"   Circuito cuántico con {quantum_channel.num_qubits} qubits creado\n")

if WITH_EVE:
    print("3. Eva intercepta, mide y reenvía")
    quantum_channel = eve.intercept_and_resend(quantum_channel)
    print(f"   Eva midió con bases: {eve.get_bases()[:10]}...")
    print(f"   Eva obtuvo bits: {eve.get_bits()[:10]}...\n")

print(f"{'4' if WITH_EVE else '3'}. Bob recibe y mide todos los qubits")
bob.receive_and_measure_all(quantum_channel)
print(f"   Bits de Bob:  {bob.get_bits()[:10]}...")
print(f"   Bases de Bob: {bob.get_bases()[:10]}...\n")

print(f"{'5' if WITH_EVE else '4'}. Comparación de bases Alice-Bob y filtrado (sifting)")
matching_indices_alice_bob = alice.compare_bases(bob.get_bases())
print(f"   Bases coincidentes en posiciones: {matching_indices_alice_bob}")
print(f"   Total de coincidencias: {len(matching_indices_alice_bob)} de {n_qubits}\n")

if WITH_EVE:
    print("   Comparación de bases Alice-Eva:")
    matching_indices_alice_eve = [i for i in range(n_qubits) if alice.get_bases()[i] == eve.get_bases()[i]]
    eve_bits_matching_alice = [eve.get_bits()[i] for i in matching_indices_alice_eve]
    alice_bits_matching_eve = [alice.get_bits()[i] for i in matching_indices_alice_eve]
    eve_errors = sum(1 for i in range(len(eve_bits_matching_alice)) if eve_bits_matching_alice[i] != alice_bits_matching_eve[i])
    print(f"   Total coincidencias Alice-Eva: {len(matching_indices_alice_eve)} de {n_qubits}")
    print(f"   Bits de Eva (bases coincidentes con Alice): {eve_bits_matching_alice[:15]}...")
    print(f"   Bits de Alice (bases coincidentes con Eva): {alice_bits_matching_eve[:15]}...")
    print(f"   Errores Eva vs Alice: {eve_errors} de {len(eve_bits_matching_alice)}\n")

alice.sift_key(matching_indices_alice_bob)
bob.sift_key(matching_indices_alice_bob)

print(f"{'6' if WITH_EVE else '5'}. Claves finales después de sifting")
print(f"   Clave de Alice: {alice.get_bits()[:20]}{'...' if len(alice.get_bits()) > 20 else ''}")
print(f"   Clave de Bob:   {bob.get_bits()[:20]}{'...' if len(bob.get_bits()) > 20 else ''}\n")

print(f"{'7' if WITH_EVE else '6'}. Verificación")
errors = sum(1 for i in range(len(alice.get_bits())) if alice.get_bits()[i] != bob.get_bits()[i])
print(f"   Errores: {errors}")
print(f"   Claves idénticas: {'✓ SÍ' if errors == 0 else '✗ NO'}")
print(f"   QBER: {errors/len(alice.get_bits())*100:.1f}%" if len(alice.get_bits()) > 0 else "N/A")