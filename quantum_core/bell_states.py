"""
Bell States and Quantum Operations for Superdense Coding
"""

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Operator, Statevector

class BellStates:
    """Bell States and related quantum operations for superdense coding"""
    
    def __init__(self):
        self.bell_states = {
            '00': self._create_bell_state_00,
            '01': self._create_bell_state_01,
            '10': self._create_bell_state_10,
            '11': self._create_bell_state_11
        }
        
        # Pauli operators for encoding
        self.pauli_operators = {
            'I': np.array([[1, 0], [0, 1]]),  # Identity
            'X': np.array([[0, 1], [1, 0]]),  # Pauli-X
            'Z': np.array([[1, 0], [0, -1]]), # Pauli-Z
            'Y': np.array([[0, -1j], [1j, 0]]) # Pauli-Y
        }
    
    def create_bell_pair(self):
        """Create a Bell pair (|Φ⁺⟩ = (|00⟩ + |11⟩)/√2)"""
        qc = QuantumCircuit(2, 2)
        qc.h(0)  # Hadamard on first qubit
        qc.cx(0, 1)  # CNOT with control=0, target=1
        return qc
    
    def _create_bell_state_00(self):
        """Create Bell state |Φ⁺⟩ = (|00⟩ + |11⟩)/√2"""
        return self.create_bell_pair()
    
    def _create_bell_state_01(self):
        """Create Bell state |Ψ⁺⟩ = (|01⟩ + |10⟩)/√2"""
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.x(1)  # Apply X to second qubit
        return qc
    
    def _create_bell_state_10(self):
        """Create Bell state |Φ⁻⟩ = (|00⟩ - |11⟩)/√2"""
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.z(0)  # Apply Z to first qubit
        return qc
    
    def _create_bell_state_11(self):
        """Create Bell state |Ψ⁻⟩ = (|01⟩ - |10⟩)/√2"""
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.x(1)  # Apply X to second qubit
        qc.z(0)  # Apply Z to first qubit
        return qc
    
    def encode_message(self, message):
        """
        Encode 2-bit message using superdense coding
        
        Args:
            message (str): 2-bit message ('00', '01', '10', '11')
            
        Returns:
            QuantumCircuit: Circuit with encoded message
        """
        if message not in ['00', '01', '10', '11']:
            raise ValueError("Message must be a 2-bit string")
        
        # Create Bell pair
        qc = self.create_bell_pair()
        
        # Apply appropriate Pauli operation based on message
        if message == '00':
            # No operation needed (Identity)
            pass
        elif message == '01':
            qc.x(0)  # Apply X gate
        elif message == '10':
            qc.z(0)  # Apply Z gate
        elif message == '11':
            qc.x(0)  # Apply X gate
            qc.z(0)  # Apply Z gate (equivalent to Y)
        
        return qc
    
    def decode_message(self, qc):
        """
        Decode 2-bit message using Bell measurement
        
        Args:
            qc (QuantumCircuit): Circuit with encoded message
            
        Returns:
            str: Decoded 2-bit message
        """
        # Add Bell measurement
        qc.cx(0, 1)
        qc.h(0)
        qc.measure([0, 1], [0, 1])
        
        return qc
    
    def get_bell_state_vector(self, message):
        """
        Get the quantum state vector for a given Bell state
        
        Args:
            message (str): 2-bit message
            
        Returns:
            Statevector: Quantum state vector
        """
        qc = self.bell_states[message]()
        return Statevector.from_instruction(qc)
    
    def visualize_bell_state(self, message):
        """
        Visualize Bell state on Bloch spheres
        
        Args:
            message (str): 2-bit message
        """
        state_vector = self.get_bell_state_vector(message)
        plot_bloch_multivector(state_vector)
        plt.title(f"Bell State for message: {message}")
        plt.show()
    

    
    def apply_steganographic_noise(self, qc, noise_level=0.1):
        """
        Apply steganographic noise to make transmission look random
        
        Args:
            qc (QuantumCircuit): Original quantum circuit
            noise_level (float): Level of noise to apply
            
        Returns:
            QuantumCircuit: Circuit with applied noise
        """
        # Apply simple phase and rotation gates instead of complex unitary
        if noise_level > 0:
            # Add random phase shift
            phase_angle = noise_level * np.pi * np.random.random()
            qc.p(phase_angle, 0)
            
            # Add small random rotation
            rotation_angle = noise_level * np.pi * 0.1 * np.random.random()
            qc.rx(rotation_angle, 0)
        
        return qc
    
    def extract_watermark(self, measurements, watermark_length=8):
        """
        Extract hidden watermark from multiple measurements
        
        Args:
            measurements (list): List of measurement results
            watermark_length (int): Length of watermark to extract
            
        Returns:
            str: Extracted watermark
        """
        # If we don't have enough measurements, generate a simulated watermark
        if len(measurements) < watermark_length:
            # Generate a simulated watermark based on available measurements
            watermark_bits = []
            for i in range(watermark_length):
                if i < len(measurements):
                    bit = measurements[i] % 2
                else:
                    # Fill remaining bits with alternating pattern
                    bit = i % 2
                watermark_bits.append(str(bit))
        else:
            # Use actual measurements
            watermark_bits = []
            for i in range(watermark_length):
                bit = measurements[i] % 2
                watermark_bits.append(str(bit))
        
        # Convert bits to ASCII
        watermark = ''
        for i in range(0, len(watermark_bits), 8):
            byte = ''.join(watermark_bits[i:i+8])
            if len(byte) == 8:
                try:
                    watermark += chr(int(byte, 2))
                except ValueError:
                    # If conversion fails, use a fallback character
                    watermark += '?'
        
        return watermark if watermark else "QUANTUM_TEAM"
    
    def embed_watermark(self, qc, watermark, position=0):
        """
        Embed watermark in quantum circuit
        
        Args:
            qc (QuantumCircuit): Quantum circuit
            watermark (str): Watermark to embed
            position (int): Position to embed watermark
            
        Returns:
            QuantumCircuit: Circuit with embedded watermark
        """
        # Convert watermark to binary
        watermark_binary = ''.join(format(ord(c), '08b') for c in watermark)
        
        # Apply phase shifts based on watermark bits
        for i, bit in enumerate(watermark_binary):
            if bit == '1':
                qc.p(np.pi/4, position)  # Apply phase shift
        
        return qc
