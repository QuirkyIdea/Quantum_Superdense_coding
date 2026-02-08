"""
VR Visualizer Launcher for Quantum Superdense Coding
"""

from vr_visualizer.app import VRVisualizer
import sys
import argparse

def main():
    """Launch the VR visualizer"""
    parser = argparse.ArgumentParser(description='Quantum Superdense Coding VR Visualizer')
    parser.add_argument('--port', type=int, default=8050, help='Port to run the visualizer on')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    parser.add_argument('--host', type=str, default='localhost', help='Host to bind to')
    
    args = parser.parse_args()
    
    print("🚀 Launching Quantum Superdense Coding VR Visualizer...")
    print("=" * 60)
    print()
    print("🎮 Features:")
    print("   • 3D visualization of quantum communication")
    print("   • Interactive Alice and Bob avatars")
    print("   • Real-time Bell pair visualization")
    print("   • Pauli operations with gesture controls")
    print("   • Steganography mode (hide in noise)")
    print("   • Team watermarking")
    print("   • Gamified learning experience")
    print()
    print("🎯 How to use:")
    print("   1. Select a 2-bit message (00, 01, 10, 11)")
    print("   2. Choose Pauli operations (I, X, Z, Y)")
    print("   3. Enable steganography to hide in noise")
    print("   4. Add team watermark")
    print("   5. Send quantum message")
    print("   6. Perform Bell measurement")
    print("   7. Watch the 3D visualization!")
    print()
    
    try:
        # Create and run visualizer
        visualizer = VRVisualizer()
        visualizer.run(debug=args.debug, port=args.port)
        
    except KeyboardInterrupt:
        print("\n⏹️ VR Visualizer stopped by user")
    except Exception as e:
        print(f"\n❌ Error launching VR Visualizer: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
