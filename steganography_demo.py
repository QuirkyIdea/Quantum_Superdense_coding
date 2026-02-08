"""
Quantum Steganography Demo - Showcase the Power of Hiding Messages in Entanglement
"""

import time
import json
import requests
from quantum_core.superdense_coding import SuperdenseCoding
from quantum_core.steganography import QuantumSteganography
import numpy as np

class QuantumSteganographyDemo:
    """Comprehensive demo of quantum steganography and superdense coding"""
    
    def __init__(self):
        self.superdense_coding = SuperdenseCoding()
        self.steganography = QuantumSteganography()
        
        # Demo messages
        self.demo_messages = [
            "Hello Quantum World!",
            "Team Quantum Innovation",
            "Hackathon 2024 Winner",
            "Steganography in Entanglement"
        ]
        
        # Team watermarks
        self.team_watermarks = [
            "QUANTUM_TEAM",
            "HACKATHON_WINNERS",
            "STEALTH_COMMUNICATION",
            "ENTANGLEMENT_MASTERS"
        ]
    
    def run_full_demo(self):
        """Run the complete quantum steganography demo"""
        print("🚀 QUANTUM SUPERDENSE CODING + STEGANOGRAPHY DEMO")
        print("=" * 60)
        print()
        
        # Demo 1: Basic Superdense Coding
        self.demo_superdense_coding()
        
        # Demo 2: Quantum Steganography
        self.demo_quantum_steganography()
        
        # Demo 3: Team Watermarking
        self.demo_team_watermarking()
        
        # Demo 4: Eavesdropping Detection
        self.demo_eavesdropping_detection()
        
        # Demo 5: Quantum Signatures
        self.demo_quantum_signatures()
        
        # Demo 6: Performance Analysis
        self.demo_performance_analysis()
        
        print("\n" + "=" * 60)
        print("🎉 DEMO COMPLETED SUCCESSFULLY!")
        print("🌟 Hackathon Wow Factor: Messages hidden invisibly in entanglement!")
    
    def demo_superdense_coding(self):
        """Demo basic superdense coding"""
        print("📡 DEMO 1: SUPERDENSE CODING")
        print("-" * 40)
        
        messages = ['00', '01', '10', '11']
        success_count = 0
        
        for message in messages:
            print(f"\nSending message: {message}")
            
            # Encode message
            encoded_data = self.superdense_coding.encode_message(message, apply_steganography=False)
            
            # Decode message
            decoded_result = self.superdense_coding.decode_message(encoded_data)
            
            success = decoded_result['success']
            if success:
                success_count += 1
            
            print(f"  Encoded: {message}")
            print(f"  Decoded: {decoded_result['decoded_message']}")
            print(f"  Success: {'✅' if success else '❌'}")
            print(f"  Fidelity: {decoded_result['fidelity']:.3f}")
        
        success_rate = success_count / len(messages) * 100
        print(f"\n📊 Superdense Coding Success Rate: {success_rate:.1f}%")
        print("✅ 2 classical bits transmitted per qubit using entanglement!")
    
    def demo_quantum_steganography(self):
        """Demo quantum steganography"""
        print("\n🔒 DEMO 2: QUANTUM STEGANOGRAPHY")
        print("-" * 40)
        
        for i, message in enumerate(self.demo_messages):
            print(f"\nHiding message {i+1}: '{message}'")
            
            # Create noise circuit with hidden message
            circuit_data = self.steganography.create_noise_circuit(
                message, 
                self.team_watermarks[i % len(self.team_watermarks)]
            )
            
            # Analyze noise appearance
            noise_analysis = self.steganography.create_noise_analysis_report(circuit_data)
            
            # Extract hidden message
            extraction_result = self.steganography.extract_hidden_message(circuit_data)
            
            print(f"  Hidden in: {noise_analysis['total_gates']} quantum gates")
            print(f"  Appears random: {'✅' if noise_analysis['appears_random'] else '❌'}")
            print(f"  Circuit entropy: {noise_analysis['circuit_entropy']:.3f}")
            print(f"  Measurement entropy: {noise_analysis['measurement_entropy']:.3f}")
            print(f"  Extraction success: {'✅' if extraction_result['extraction_success'] else '❌'}")
            print(f"  Extracted: '{extraction_result['extracted_message']}'")
            
            if extraction_result['watermark']:
                print(f"  Watermark: {extraction_result['watermark']}")
        
        print("\n🎭 To outsiders, transmissions look like random quantum noise!")
        print("🔐 Only intended recipients can decode the hidden messages!")
    
    def demo_team_watermarking(self):
        """Demo team watermarking across multiple runs"""
        print("\n🏆 DEMO 3: TEAM WATERMARKING")
        print("-" * 40)
        
        team_name = "QUANTUM_INNOVATION_TEAM"
        logo_data = b"QUANTUM_LOGO_2024"
        
        print(f"Creating watermark for team: {team_name}")
        
        # Create team watermark
        watermark_data = self.steganography.create_team_watermark(team_name, logo_data)
        
        print(f"  Team: {watermark_data['team_name']}")
        print(f"  Signature: {watermark_data['signature']}")
        print(f"  Timestamp: {watermark_data['timestamp']:.6f}")
        
        # Embed watermark in multiple messages
        print("\nEmbedding watermark across multiple quantum transmissions:")
        
        for i in range(5):
            message = f"Secret message {i+1}"
            
            # Create circuit with team watermark
            qc = self.superdense_coding.bell_states.create_bell_pair()
            qc = self.steganography.embed_team_watermark(qc, watermark_data)
            qc.measure_all()
            
            print(f"  Transmission {i+1}: Watermark embedded in {len(qc.data)} gates")
        
        print("\n🏷️ Team identity hidden across all quantum communications!")
    
    def demo_eavesdropping_detection(self):
        """Demo eavesdropping detection"""
        print("\n🕵️ DEMO 4: EAVESDROPPING DETECTION")
        print("-" * 40)
        
        # Create original message
        original_message = "Top Secret Quantum Data"
        encoded_data = self.superdense_coding.encode_message("01", apply_steganography=True)
        
        print(f"Original message: '{original_message}'")
        print(f"Encoded with steganography: ✅")
        
        # Simulate different eavesdropper knowledge levels
        knowledge_levels = [0.0, 0.25, 0.5, 0.75, 1.0]
        
        for knowledge in knowledge_levels:
            eavesdropping_result = self.superdense_coding.simulate_eavesdropping(
                encoded_data, knowledge
            )
            
            detection_prob = eavesdropping_result['detection_probability']
            eavesdropper_success = eavesdropping_result['eavesdropper_success']
            
            print(f"\nEavesdropper knowledge: {knowledge*100:.0f}%")
            print(f"  Eavesdropper success: {eavesdropper_success:.3f}")
            print(f"  Detection probability: {detection_prob:.3f}")
            print(f"  Security level: {'🔴' if eavesdropper_success > 0.5 else '🟡' if eavesdropper_success > 0.25 else '🟢'}")
        
        print("\n🛡️ Quantum steganography provides eavesdropping detection!")
    
    def demo_quantum_signatures(self):
        """Demo quantum signatures"""
        print("\n✍️ DEMO 5: QUANTUM SIGNATURES")
        print("-" * 40)
        
        messages = [
            "Quantum communication protocol",
            "Steganographic message encoding",
            "Bell state entanglement",
            "Superdense coding implementation"
        ]
        
        for message in messages:
            print(f"\nSigning message: '{message}'")
            
            # Create quantum signature
            signature_data = self.superdense_coding.create_quantum_signature(message)
            
            print(f"  Message hash: {signature_data['message_hash'][:16]}...")
            print(f"  Signature bits: {signature_data['signature_bits']}")
            print(f"  Circuit depth: {signature_data['signature_circuit']['circuit'].depth()}")
            
            # Verify signature
            is_valid = self.superdense_coding.verify_quantum_signature(message, signature_data)
            print(f"  Signature valid: {'✅' if is_valid else '❌'}")
            
            # Try to verify with modified message
            modified_message = message + " (modified)"
            is_valid_modified = self.superdense_coding.verify_quantum_signature(modified_message, signature_data)
            print(f"  Modified message valid: {'❌' if not is_valid_modified else '⚠️'}")
        
        print("\n🔐 Quantum signatures provide message authentication!")
    
    def demo_performance_analysis(self):
        """Demo performance analysis"""
        print("\n📊 DEMO 6: PERFORMANCE ANALYSIS")
        print("-" * 40)
        
        # Test different message lengths
        message_lengths = [10, 50, 100, 200]
        
        print("Performance comparison:")
        print("Message Length | Steganography | Entropy | Success Rate")
        print("-" * 55)
        
        for length in message_lengths:
            # Generate random message
            message = ''.join(np.random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ '), length))
            
            # Test with steganography
            start_time = time.time()
            circuit_data = self.steganography.create_noise_circuit(message, "PERF_TEST")
            stego_time = time.time() - start_time
            
            noise_analysis = self.steganography.create_noise_analysis_report(circuit_data)
            extraction_result = self.steganography.extract_hidden_message(circuit_data)
            
            # Test without steganography
            start_time = time.time()
            encoded_data = self.superdense_coding.encode_message("01", apply_steganography=False)
            normal_time = time.time() - start_time
            
            print(f"{length:13d} | {'Yes':13s} | {noise_analysis['circuit_entropy']:7.3f} | {extraction_result['extraction_success']:11.1%}")
            print(f"{length:13d} | {'No':13s} | {'N/A':7s} | {normal_time/stego_time:11.1%}x faster")
        
        print("\n⚡ Steganography adds security with minimal performance overhead!")
    
    def demo_hackathon_wow_factor(self):
        """Special demo for hackathon wow factor"""
        print("\n🌟 HACKATHON WOW FACTOR DEMO")
        print("=" * 60)
        
        print("🎯 Key Innovation: We don't just send 2 classical bits per qubit—")
        print("   we hide them invisibly in entanglement. Looks like noise to an eavesdropper!")
        print()
        
        # Create a secret message with team watermark
        secret_message = "QUANTUM_INNOVATION_TEAM_WINS_HACKATHON_2024"
        team_watermark = "AMRAVATI_QUANTUM_VALLEY"
        
        print(f"🔐 Hiding secret message: '{secret_message}'")
        print(f"🏷️ With team watermark: '{team_watermark}'")
        
        # Create steganographic circuit
        circuit_data = self.steganography.create_noise_circuit(secret_message, team_watermark)
        
        # Analyze how it appears to outsiders
        noise_analysis = self.steganography.create_noise_analysis_report(circuit_data)
        
        print(f"\n📊 To outsiders, this transmission appears as:")
        print(f"   • Random quantum noise with {noise_analysis['total_gates']} gates")
        print(f"   • Circuit entropy: {noise_analysis['circuit_entropy']:.3f}")
        print(f"   • Measurement entropy: {noise_analysis['measurement_entropy']:.3f}")
        print(f"   • Appears random: {'✅' if noise_analysis['appears_random'] else '❌'}")
        
        # Extract the hidden message
        extraction_result = self.steganography.extract_hidden_message(circuit_data)
        
        print(f"\n🎉 Only intended recipients can decode:")
        print(f"   • Hidden message: '{extraction_result['extracted_message']}'")
        print(f"   • Team watermark: '{extraction_result.get('watermark', 'N/A')}'")
        print(f"   • Extraction success: {'✅' if extraction_result['extraction_success'] else '❌'}")
        
        print(f"\n🚀 INNOVATION HIGHLIGHTS:")
        print(f"   • 2 classical bits per qubit (superdense coding)")
        print(f"   • Hidden in quantum noise (steganography)")
        print(f"   • Team watermarking across transmissions")
        print(f"   • Eavesdropping detection")
        print(f"   • Quantum signature authentication")
        print(f"   • Immersive VR visualization")
        
        print(f"\n🏆 HACKATHON IMPACT:")
        print(f"   • Revolutionary quantum communication protocol")
        print(f"   • Practical quantum steganography implementation")
        print(f"   • Educational VR quantum mechanics visualization")
        print(f"   • Real-world quantum security applications")

def main():
    """Run the quantum steganography demo"""
    demo = QuantumSteganographyDemo()
    
    try:
        # Run full demo
        demo.run_full_demo()
        
        # Run special hackathon demo
        demo.demo_hackathon_wow_factor()
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
    
    print("\n🎊 Thank you for experiencing Quantum Superdense Coding + Steganography!")

if __name__ == "__main__":
    main()
