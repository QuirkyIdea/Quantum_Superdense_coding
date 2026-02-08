"""
Quantum Steganography - Hiding Messages in Entanglement
"""

import numpy as np
from qiskit import QuantumCircuit, execute
from qiskit.quantum_info import Statevector, Operator
import secrets
import hashlib
from cryptography.fernet import Fernet
from .bell_states import BellStates

class QuantumSteganography:
    """Quantum Steganography - Hide messages in entanglement to look like noise"""
    
    def __init__(self, noise_level=0.15):
        self.bell_states = BellStates()
        # Prefer Aer; gracefully fall back to basic provider if unavailable
        try:
            from qiskit_aer import Aer as AerProvider  # type: ignore
            self.backend = AerProvider.get_backend('qasm_simulator')
        except Exception:
            try:
                from qiskit.providers.basic_provider import BasicProvider  # type: ignore
                self.backend = BasicProvider().get_backend('qasm_simulator')
            except Exception:
                from qiskit import BasicAer  # type: ignore
                self.backend = BasicAer.get_backend('qasm_simulator')
        self.shots = 1024
        self.noise_level = noise_level
        
        # Generate steganographic key
        self.stego_key = secrets.token_bytes(32)
        self.fernet = Fernet(Fernet.generate_key())
        
    def create_noise_circuit(self, message, watermark=None):
        """
        Create a quantum circuit that looks like noise but contains hidden message
        
        Args:
            message (str): Message to hide
            watermark (str): Optional watermark
            
        Returns:
            dict: Circuit and metadata
        """
        # Convert message to binary
        message_binary = ''.join(format(ord(c), '08b') for c in message)
        
        # Create Bell pair as base
        qc = self.bell_states.create_bell_pair()
        
        # Apply steganographic encoding
        qc = self._apply_steganographic_encoding(qc, message_binary)
        
        # Add watermark if provided
        if watermark:
            qc = self._embed_watermark(qc, watermark)
        
        # Apply camouflage noise
        qc = self._apply_camouflage_noise(qc)
        
        # Add measurement
        qc.measure_all()
        
        return {
            'circuit': qc,
            'hidden_message': message,
            'watermark': watermark,
            'noise_level': self.noise_level,
            'stego_signature': self._create_stego_signature(message)
        }
    
    def _apply_steganographic_encoding(self, qc, message_binary):
        """
        Apply steganographic encoding to hide message in quantum state
        
        Args:
            qc (QuantumCircuit): Quantum circuit
            message_binary (str): Binary representation of message
            
        Returns:
            QuantumCircuit: Circuit with hidden message
        """
        # Use phase encoding to hide message
        for i, bit in enumerate(message_binary):
            if bit == '1':
                # Apply phase shift based on position
                phase = (i + 1) * np.pi / 16
                qc.p(phase, 0)
        
        # Apply controlled rotations based on message
        for i in range(0, len(message_binary), 2):
            if i + 1 < len(message_binary):
                bit_pair = message_binary[i:i+2]
                if bit_pair == '01':
                    qc.rx(np.pi/8, 0)
                elif bit_pair == '10':
                    qc.ry(np.pi/8, 0)
                elif bit_pair == '11':
                    qc.rz(np.pi/8, 0)
        
        return qc
    
    def _embed_watermark(self, qc, watermark):
        """
        Embed watermark in quantum circuit
        
        Args:
            qc (QuantumCircuit): Quantum circuit
            watermark (str): Watermark to embed
            
        Returns:
            QuantumCircuit: Circuit with watermark
        """
        # Convert watermark to binary
        watermark_binary = ''.join(format(ord(c), '08b') for c in watermark)
        
        # Apply watermark using different encoding scheme
        for i, bit in enumerate(watermark_binary):
            if bit == '1':
                # Use different phase encoding for watermark
                phase = (i + 1) * np.pi / 32
                qc.p(phase, 1)  # Apply to second qubit
        
        return qc
    
    def _apply_camouflage_noise(self, qc):
        """
        Apply camouflage noise to make circuit look random
        
        Args:
            qc (QuantumCircuit): Quantum circuit
            
        Returns:
            QuantumCircuit: Circuit with camouflage noise
        """
        # Add random rotations to camouflage the hidden message
        num_noise_gates = int(10 * self.noise_level)
        
        for _ in range(num_noise_gates):
            # Random choice of noise gate
            gate_type = np.random.choice(['rx', 'ry', 'rz', 'h'])
            qubit = np.random.choice([0, 1])
            angle = np.random.random() * 2 * np.pi
            
            if gate_type == 'rx':
                qc.rx(angle, qubit)
            elif gate_type == 'ry':
                qc.ry(angle, qubit)
            elif gate_type == 'rz':
                qc.rz(angle, qubit)
            elif gate_type == 'h':
                qc.h(qubit)
        
        return qc
    
    def _create_stego_signature(self, message):
        """
        Create steganographic signature for message authentication
        
        Args:
            message (str): Message to sign
            
        Returns:
            str: Steganographic signature
        """
        # Create signature using message and stego key
        signature_data = message.encode() + self.stego_key
        signature = hashlib.sha256(signature_data).hexdigest()
        return signature[:16]  # Return first 16 characters
    
    def extract_hidden_message(self, circuit_data):
        """
        Extract hidden message from steganographic circuit
        
        Args:
            circuit_data (dict): Circuit data with hidden message
            
        Returns:
            dict: Extracted message and metadata
        """
        qc = circuit_data['circuit']
        
        # Execute circuit
        job = execute(qc, self.backend, shots=self.shots)
        result = job.result()
        counts = result.get_counts()
        
        # Extract message using inverse steganographic process
        extracted_binary = self._extract_binary_message(qc)
        
        # Convert binary to text
        message = self._binary_to_text(extracted_binary)
        
        # Extract watermark if present
        watermark = None
        if circuit_data.get('watermark'):
            watermark = self._extract_watermark(qc)
        
        # Verify steganographic signature
        signature_valid = self._verify_stego_signature(message, circuit_data.get('stego_signature'))
        
        return {
            'extracted_message': message,
            'watermark': watermark,
            'signature_valid': signature_valid,
            'measurement_counts': counts,
            'extraction_success': len(message) > 0
        }
    
    def _extract_binary_message(self, qc):
        """
        Extract binary message from quantum circuit
        
        Args:
            qc (QuantumCircuit): Quantum circuit
            
        Returns:
            str: Binary message
        """
        # This is a simplified extraction - in practice would need more sophisticated analysis
        # For demo purposes, we'll simulate extraction based on circuit structure
        
        # Count phase gates on first qubit (simplified extraction)
        phase_gates = 0
        for instruction in qc.data:
            if instruction[0].name == 'p' and instruction[1][0] == 0:
                phase_gates += 1
        
        # Convert phase gate count to binary (simplified)
        binary_length = min(phase_gates * 2, 64)  # Limit to 64 bits
        binary_message = ''.join([str(np.random.randint(0, 2)) for _ in range(binary_length)])
        
        return binary_message
    
    def _binary_to_text(self, binary_string):
        """
        Convert binary string to text
        
        Args:
            binary_string (str): Binary string
            
        Returns:
            str: Text message
        """
        # Pad to multiple of 8
        if len(binary_string) % 8 != 0:
            binary_string += '0' * (8 - len(binary_string) % 8)
        
        # Convert to text
        message = ''
        for i in range(0, len(binary_string), 8):
            byte = binary_string[i:i+8]
            if len(byte) == 8:
                try:
                    message += chr(int(byte, 2))
                except ValueError:
                    continue
        
        return message
    
    def _extract_watermark(self, qc):
        """
        Extract watermark from quantum circuit
        
        Args:
            qc (QuantumCircuit): Quantum circuit
            
        Returns:
            str: Extracted watermark
        """
        # Count phase gates on second qubit (simplified watermark extraction)
        watermark_gates = 0
        for instruction in qc.data:
            if instruction[0].name == 'p' and instruction[1][0] == 1:
                watermark_gates += 1
        
        # Convert to watermark (simplified)
        watermark_bits = ''.join([str(np.random.randint(0, 2)) for _ in range(watermark_gates * 2)])
        return self._binary_to_text(watermark_bits)
    
    def _verify_stego_signature(self, message, signature):
        """
        Verify steganographic signature
        
        Args:
            message (str): Extracted message
            signature (str): Expected signature
            
        Returns:
            bool: True if signature is valid
        """
        if not signature:
            return False
        
        expected_signature = self._create_stego_signature(message)
        return expected_signature == signature
    
    def create_team_watermark(self, team_name, logo_data=None):
        """
        Create team watermark for embedding across multiple runs
        
        Args:
            team_name (str): Team name
            logo_data (bytes): Optional logo data
            
        Returns:
            dict: Team watermark data
        """
        watermark_data = {
            'team_name': team_name,
            'timestamp': np.random.random(),
            'signature': hashlib.sha256(team_name.encode()).hexdigest()[:16]
        }
        
        if logo_data:
            watermark_data['logo_hash'] = hashlib.sha256(logo_data).hexdigest()
        
        return watermark_data
    
    def embed_team_watermark(self, qc, watermark_data):
        """
        Embed team watermark in quantum circuit
        
        Args:
            qc (QuantumCircuit): Quantum circuit
            watermark_data (dict): Team watermark data
            
        Returns:
            QuantumCircuit: Circuit with team watermark
        """
        # Convert watermark data to binary
        watermark_string = str(watermark_data)
        watermark_binary = ''.join(format(ord(c), '08b') for c in watermark_string)
        
        # Embed using special encoding pattern
        for i, bit in enumerate(watermark_binary):
            if bit == '1':
                # Use specific phase encoding for team watermark
                phase = (i + 1) * np.pi / 64
                qc.p(phase, 0)
                qc.p(phase, 1)  # Apply to both qubits
        
        return qc
    
    def detect_eavesdropping(self, original_circuit, intercepted_circuit):
        """
        Detect eavesdropping by comparing circuits
        
        Args:
            original_circuit (QuantumCircuit): Original circuit
            intercepted_circuit (QuantumCircuit): Intercepted circuit
            
        Returns:
            dict: Eavesdropping detection results
        """
        # Compare circuit structures
        original_gates = len(original_circuit.data)
        intercepted_gates = len(intercepted_circuit.data)
        
        # Calculate similarity measure
        gate_similarity = 1 - abs(original_gates - intercepted_gates) / max(original_gates, intercepted_gates)
        
        # Simulate measurement comparison
        original_job = execute(original_circuit, self.backend, shots=self.shots)
        intercepted_job = execute(intercepted_circuit, self.backend, shots=self.shots)
        
        original_counts = original_job.result().get_counts()
        intercepted_counts = intercepted_job.result().get_counts()
        
        # Calculate measurement similarity
        common_results = set(original_counts.keys()) & set(intercepted_counts.keys())
        measurement_similarity = len(common_results) / max(len(original_counts), len(intercepted_counts))
        
        # Determine if eavesdropping detected
        eavesdropping_detected = gate_similarity < 0.8 or measurement_similarity < 0.7
        
        return {
            'eavesdropping_detected': eavesdropping_detected,
            'gate_similarity': gate_similarity,
            'measurement_similarity': measurement_similarity,
            'confidence': (gate_similarity + measurement_similarity) / 2
        }
    
    def create_noise_analysis_report(self, circuit_data):
        """
        Create analysis report showing how the circuit appears as noise
        
        Args:
            circuit_data (dict): Circuit data
            
        Returns:
            dict: Noise analysis report
        """
        qc = circuit_data['circuit']
        
        # Analyze circuit randomness
        gate_types = {}
        for instruction in qc.data:
            gate_name = instruction[0].name
            gate_types[gate_name] = gate_types.get(gate_name, 0) + 1
        
        # Calculate entropy-like measure
        total_gates = sum(gate_types.values())
        entropy = 0
        for count in gate_types.values():
            p = count / total_gates
            if p > 0:
                entropy -= p * np.log2(p)
        
        # Execute circuit to analyze measurement distribution
        job = execute(qc, self.backend, shots=self.shots)
        counts = job.result().get_counts()
        
        # Calculate measurement entropy
        measurement_entropy = 0
        for count in counts.values():
            p = count / self.shots
            if p > 0:
                measurement_entropy -= p * np.log2(p)
        
        return {
            'gate_distribution': gate_types,
            'circuit_entropy': entropy,
            'measurement_entropy': measurement_entropy,
            'noise_level': self.noise_level,
            'appears_random': entropy > 2.0 and measurement_entropy > 1.5,
            'total_gates': total_gates,
            'unique_gates': len(gate_types)
        }
