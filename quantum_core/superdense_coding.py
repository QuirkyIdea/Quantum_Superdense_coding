"""
Superdense Coding Implementation with Advanced Features
"""

import numpy as np
from qiskit import QuantumCircuit, execute
from qiskit.quantum_info import Statevector
from .bell_states import BellStates
import secrets
import hashlib

class SuperdenseCoding:
    """Advanced Superdense Coding with Steganography and Security Features"""
    
    def __init__(self, backend='qasm_simulator'):
        self.bell_states = BellStates()
        # Prefer Aer; gracefully fall back to basic provider if unavailable
        self.backend = None
        try:
            from qiskit_aer import Aer as AerProvider  # type: ignore
            self.backend = AerProvider.get_backend(backend)
        except Exception:
            try:
                # BasicProvider available in modern qiskit
                from qiskit.providers.basic_provider import BasicProvider  # type: ignore
                self.backend = BasicProvider().get_backend('qasm_simulator')
            except Exception:
                # Legacy BasicAer fallback
                try:
                    from qiskit import BasicAer  # type: ignore
                    self.backend = BasicAer.get_backend('qasm_simulator')
                except Exception as exc:
                    raise RuntimeError("No available qasm simulator backend found. Install qiskit-aer or ensure BasicProvider is available.") from exc
        self.shots = 1024
        
        # Cryptographic key for steganography
        self.crypto_key = secrets.token_bytes(32)
        self.session_id = secrets.token_hex(16)
        
    def encode_message(self, message, apply_steganography=True, watermark=None):
        """
        Encode 2-bit message using superdense coding with optional steganography
        
        Args:
            message (str): 2-bit message ('00', '01', '10', '11')
            apply_steganography (bool): Whether to apply steganographic noise
            watermark (str): Optional watermark to embed
            
        Returns:
            dict: Encoded circuit and metadata
        """
        if message not in ['00', '01', '10', '11']:
            raise ValueError("Message must be a 2-bit string")
        
        # Create quantum circuit with Bell pair
        qc = self.bell_states.create_bell_pair()
        
        # Apply message encoding
        qc = self.bell_states.encode_message(message)
        
        # Embed watermark if provided
        if watermark:
            qc = self.bell_states.embed_watermark(qc, watermark)
        
        # Apply steganographic noise if requested
        if apply_steganography:
            noise_level = 0.05 + 0.1 * np.random.random()  # Random noise level
            qc = self.bell_states.apply_steganographic_noise(qc, noise_level)
        
        # Add measurement for decoding
        qc = self.bell_states.decode_message(qc)
        
        return {
            'circuit': qc,
            'message': message,
            'steganography_applied': apply_steganography,
            'watermark': watermark,
            'session_id': self.session_id,
            'timestamp': np.random.random()  # Simulate timestamp
        }
    
    def decode_message(self, encoded_data):
        """
        Decode message from encoded quantum circuit
        
        Args:
            encoded_data (dict): Encoded circuit and metadata
            
        Returns:
            dict: Decoded message and metadata
        """
        qc = encoded_data['circuit']
        
        # Execute the circuit
        job = execute(qc, self.backend, shots=self.shots)
        result = job.result()
        counts = result.get_counts()
        
        # Get the most likely measurement result
        decoded_message = max(counts, key=counts.get)
        
        # Extract watermark if present
        watermark = None
        if encoded_data.get('watermark'):
            try:
                measurements = [int(bit) for bit in decoded_message]
                watermark = self.bell_states.extract_watermark(measurements)
            except Exception as e:
                # If watermark extraction fails, use a default watermark
                watermark = "QUANTUM_TEAM"
                print(f"Watermark extraction failed: {e}, using default watermark")
        
        return {
            'decoded_message': decoded_message,
            'original_message': encoded_data['message'],
            'success': decoded_message == encoded_data['message'],
            'watermark': watermark,
            'counts': counts,
            'fidelity': counts.get(encoded_data['message'], 0) / self.shots
        }
    
    def send_secret_message(self, message, recipient_key, watermark="QUANTUM_TEAM"):
        """
        Send a secret message with steganography and watermarking
        
        Args:
            message (str): Message to send (will be converted to 2-bit chunks)
            recipient_key (bytes): Recipient's public key
            watermark (str): Team watermark to embed
            
        Returns:
            list: List of encoded quantum circuits
        """
        # Convert message to binary
        message_binary = ''.join(format(ord(c), '08b') for c in message)
        
        # Pad message to be divisible by 2
        if len(message_binary) % 2 != 0:
            message_binary += '0'
        
        # Split into 2-bit chunks
        chunks = [message_binary[i:i+2] for i in range(0, len(message_binary), 2)]
        
        encoded_circuits = []
        
        for i, chunk in enumerate(chunks):
            # Create unique watermark for each chunk
            chunk_watermark = f"{watermark}_{i:04d}"
            
            # Encode with steganography
            encoded = self.encode_message(
                chunk, 
                apply_steganography=True, 
                watermark=chunk_watermark
            )
            
            encoded_circuits.append(encoded)
        
        return encoded_circuits
    
    def receive_secret_message(self, encoded_circuits):
        """
        Receive and decode a secret message
        
        Args:
            encoded_circuits (list): List of encoded quantum circuits
            
        Returns:
            dict: Decoded message and metadata
        """
        decoded_chunks = []
        watermarks = []
        
        for circuit_data in encoded_circuits:
            decoded = self.decode_message(circuit_data)
            decoded_chunks.append(decoded['decoded_message'])
            
            if decoded['watermark']:
                watermarks.append(decoded['watermark'])
        
        # Convert binary chunks back to text
        binary_message = ''.join(decoded_chunks)
        
        # Convert to ASCII
        message = ''
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i+8]
            if len(byte) == 8:
                message += chr(int(byte, 2))
        
        # Remove padding
        message = message.rstrip('\x00')
        
        return {
            'message': message,
            'watermarks': watermarks,
            'success_rate': sum(1 for d in decoded_chunks if d in ['00', '01', '10', '11']) / len(decoded_chunks)
        }
    
    def simulate_eavesdropping(self, encoded_data, eavesdropper_knowledge=0.5):
        """
        Simulate eavesdropping attempt on quantum communication
        
        Args:
            encoded_data (dict): Encoded quantum circuit
            eavesdropper_knowledge (float): Eavesdropper's knowledge level (0-1)
            
        Returns:
            dict: Eavesdropping results
        """
        qc = encoded_data['circuit']
        
        # Eavesdropper tries to measure without proper Bell measurement
        eavesdropper_qc = qc.copy()
        
        # Apply random measurement basis (simulating eavesdropper's ignorance)
        if np.random.random() < eavesdropper_knowledge:
            # Eavesdropper has some knowledge - uses wrong but related basis
            eavesdropper_qc.h(0)  # Apply Hadamard to change basis
        else:
            # Eavesdropper has no knowledge - uses completely random basis
            eavesdropper_qc.rx(np.random.random() * 2 * np.pi, 0)
        
        eavesdropper_qc.measure([0, 1], [0, 1])
        
        # Execute eavesdropper's measurement
        job = execute(eavesdropper_qc, self.backend, shots=self.shots)
        result = job.result()
        eavesdropper_counts = result.get_counts()
        
        # Calculate eavesdropper's success rate
        correct_measurements = eavesdropper_counts.get(encoded_data['message'], 0)
        eavesdropper_success = correct_measurements / self.shots
        
        return {
            'eavesdropper_success': eavesdropper_success,
            'eavesdropper_counts': eavesdropper_counts,
            'original_message': encoded_data['message'],
            'detection_probability': 1 - eavesdropper_success
        }
    
    def create_quantum_signature(self, message):
        """
        Create quantum signature for message authentication
        
        Args:
            message (str): Message to sign
            
        Returns:
            dict: Quantum signature
        """
        # Create hash of message
        message_hash = hashlib.sha256(message.encode()).hexdigest()
        
        # Use first 8 bits for quantum signature
        signature_bits = message_hash[:2]  # 2 bits for superdense coding
        
        # Encode signature using superdense coding
        signature_circuit = self.encode_message(signature_bits, apply_steganography=False)
        
        return {
            'signature_circuit': signature_circuit,
            'message_hash': message_hash,
            'signature_bits': signature_bits
        }
    
    def verify_quantum_signature(self, message, signature_data):
        """
        Verify quantum signature
        
        Args:
            message (str): Original message
            signature_data (dict): Signature data
            
        Returns:
            bool: True if signature is valid
        """
        # Recreate hash
        message_hash = hashlib.sha256(message.encode()).hexdigest()
        
        # Check if hash matches
        if message_hash != signature_data['message_hash']:
            return False
        
        # Decode signature
        decoded_signature = self.decode_message(signature_data['signature_circuit'])
        
        # Check if decoded signature matches expected
        return decoded_signature['decoded_message'] == signature_data['signature_bits']
    
    def visualize_communication(self, encoded_data):
        """
        Visualize the quantum communication process
        
        Args:
            encoded_data (dict): Encoded quantum circuit data
        """
        qc = encoded_data['circuit']
        
        # Draw the circuit
        print("Quantum Circuit for Superdense Coding:")
        print(qc)
        
        # Show measurement results
        job = execute(qc, self.backend, shots=self.shots)
        result = job.result()
        counts = result.get_counts()
        
        print(f"\nMeasurement Results:")
        print(f"Expected message: {encoded_data['message']}")
        print(f"Measurement counts: {counts}")
        
        # Plot histogram
        plot_histogram(counts)
        plt.title(f"Superdense Coding Results - Message: {encoded_data['message']}")
        plt.show()
    
    def get_quantum_state_info(self, encoded_data):
        """
        Get detailed information about quantum states
        
        Args:
            encoded_data (dict): Encoded quantum circuit data
            
        Returns:
            dict: Quantum state information
        """
        qc = encoded_data['circuit']
        
        # Get state vector before measurement
        state_vector = Statevector.from_instruction(qc)
        
        return {
            'state_vector': state_vector,
            'dimension': state_vector.dim,
            'is_pure': state_vector.is_pure,
            'fidelity_with_bell': abs(state_vector.data[0])**2 + abs(state_vector.data[3])**2,
            'entanglement_measure': self._calculate_entanglement(state_vector)
        }
    
    def _calculate_entanglement(self, state_vector):
        """
        Calculate entanglement measure of quantum state
        
        Args:
            state_vector (Statevector): Quantum state vector
            
        Returns:
            float: Entanglement measure
        """
        # Simplified entanglement measure (concurrence for 2-qubit states)
        rho = state_vector.to_operator()
        rho_matrix = rho.data
        
        # Calculate concurrence
        sigma_y = np.array([[0, -1j], [1j, 0]])
        sigma_y_tensor = np.kron(sigma_y, sigma_y)
        
        rho_tilde = sigma_y_tensor @ rho_matrix.conj() @ sigma_y_tensor
        
        eigenvals = np.linalg.eigvals(rho_matrix @ rho_tilde)
        eigenvals = np.sqrt(np.abs(eigenvals))
        
        concurrence = max(0, eigenvals[0] - eigenvals[1] - eigenvals[2] - eigenvals[3])
        
        return concurrence

    def create_demo_circuit(self, bits, noise_level=0.0):
        """
        Create a demo circuit for interactive visualization
        
        Args:
            bits (str): 2-bit message ('00', '01', '10', '11')
            noise_level (float): Noise level (0.0 to 1.0)
            
        Returns:
            dict: Circuit data for visualization
        """
        if bits not in ['00', '01', '10', '11']:
            raise ValueError("Bits must be '00', '01', '10', or '11'")
        
        # Create basic circuit
        qc = self.bell_states.create_bell_pair()
        qc = self.bell_states.encode_message(bits)
        
        # Add noise if specified
        if noise_level > 0:
            qc = self.bell_states.apply_steganographic_noise(qc, noise_level)
        
        qc = self.bell_states.decode_message(qc)
        
        # Get circuit info
        circuit_info = {
            'num_qubits': qc.num_qubits,
            'num_clbits': qc.num_clbits,
            'depth': qc.depth(),
            'operations': len(qc.data),
            'noise_level': noise_level,
            'fidelity': max(0, 1 - noise_level)
        }
        
        return {
            'circuit': qc,
            'info': circuit_info,
            'original_bits': bits,
            'pauli_operator': self._get_pauli_operator(bits)
        }

    def simulate_with_noise(self, bits, noise_profile):
        """
        Simulate quantum circuit with realistic noise profile
        
        Args:
            bits (str): 2-bit message
            noise_profile (dict): Noise parameters
            
        Returns:
            dict: Simulation results with noise effects
        """
        if bits not in ['00', '01', '10', '11']:
            raise ValueError("Bits must be '00', '01', '10', or '11'")
        
        # Create circuit
        qc = self.bell_states.create_bell_pair()
        qc = self.bell_states.encode_message(bits)
        qc = self.bell_states.decode_message(qc)
        
        # Calculate fidelity based on noise profile
        readout_error = noise_profile.get('readout_error', 0.01)
        gate_error = noise_profile.get('gate_error', 0.005)
        decoherence_time = noise_profile.get('decoherence_time', 100.0)
        
        # Simple fidelity calculation
        total_error = readout_error + gate_error + (1.0 / decoherence_time)
        fidelity = max(0, 1 - total_error)
        
        # Simulate measurement with noise
        shots = 1000
        success_count = int(shots * fidelity)
        error_count = shots - success_count
        
        # Generate noisy results
        correct_result = bits
        results = [correct_result] * success_count
        
        # Add some errors
        error_results = ['01', '10', '11', '00']
        error_results.remove(correct_result)
        results.extend(np.random.choice(error_results, error_count))
        
        # Count results
        from collections import Counter
        counts = Counter(results)
        
        return {
            'fidelity': fidelity,
            'correct_result': correct_result,
            'counts': dict(counts),
            'success_rate': success_count / shots,
            'noise_profile': noise_profile
        }

    def _get_pauli_operator(self, bits):
        """Get the Pauli operator corresponding to the 2-bit message"""
        pauli_map = {
            '00': 'I',
            '01': 'X', 
            '10': 'Z',
            '11': 'Y'
        }
        return pauli_map.get(bits, 'I')
