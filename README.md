# 🚀 Quantum Superdense Coding + Steganography + VR Visualizer

A revolutionary quantum communication project that implements **Quantum Superdense Coding with Steganography** - encoding 2-bit messages inside entangled Bell states while disguising transmissions as random noise to outsiders.

## 🌟 Project Highlights

**"We don't just send 2 classical bits per qubit—we hide them invisibly in entanglement. Looks like noise to an eavesdropper!"**

This project demonstrates:
- **2-bit message encoding** using Bell pairs
- **Cryptographic layer** that makes transmissions look like noise
- **Secret watermarking** capability
- **Eavesdropper-resistant** communication
- **Immersive VR/AR visualization** with 3D web application
- **Interactive quantum messaging** simulator

## 🔬 Core Features

### 1. Superdense Coding + Quantum Steganography
- **2-bit message encoding** using Bell pairs
- **Cryptographic layer** that makes transmissions look like noise
- **Secret watermarking** capability (team name/logo hidden across runs)
- **Eavesdropper-resistant** communication

### 2. Immersive VR/AR Visualizer
- **3D web application** with Alice and Bob avatars
- **Real-time Bell pair visualization** as glowing connections
- **Interactive Pauli operations** with click/gesture controls
- **Dynamic Bloch sphere morphing** with color changes
- **Gamified messaging** between users in VR space

### 3. Quantum Communication Game
- **Interactive quantum messaging** simulator
- **Steganography challenges** for participants
- **Real-time quantum state visualization**
- **Educational quantum mechanics** learning tool

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "amravati quantum valley"
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Key** (Optional - for AI chatbot feature)
   ```bash
   # Set environment variable
   # On Windows (PowerShell)
   $env:GEMINI_API_KEY="your-api-key-here"
   
   # On macOS/Linux
   export GEMINI_API_KEY="your-api-key-here"
   
   # Or create a .env file (not tracked by git)
   echo "GEMINI_API_KEY=your-api-key-here" > .env
   ```
   
   > **Note:** Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## 🎮 Usage

### Start the Quantum Server

```bash
python quantum_server.py
```

The server will start on `http://localhost:5000`

### Access the Web Interface

1. **Main Dashboard**: Open `http://localhost:5000/dashboard` in your browser
2. **API Documentation**: Visit `http://localhost:5000/` for API endpoints

### Launch the VR Visualizer

```bash
python vr_visualizer.py
```

### Run the Steganography Demo

```bash
python steganography_demo.py
```

## 🏗️ Project Structure

```
├── quantum_core/              # Core quantum implementation
│   ├── __init__.py
│   ├── superdense_coding.py   # Main superdense coding protocol
│   ├── steganography.py       # Quantum steganography layer
│   └── bell_states.py         # Bell state operations
│
├── vr_visualizer/             # VR/AR visualization
│   ├── __init__.py
│   └── app.py                 # Dash-based VR application
│
├── web_interface/             # Web interface
│   ├── dashboard.html         # Main 3D web interface
│   ├── chatbot.html           # AI chatbot interface
│   ├── quantum_canvas.js     # 3D quantum visualization
│   ├── api.py                 # API endpoints
│   └── assets/                # JavaScript libraries (Three.js)
│
├── backend/                   # Backend services
│   └── static/
│       └── index.html
│
├── quantum_server.py         # Flask server for quantum operations
├── vr_visualizer.py          # VR application launcher
├── steganography_demo.py     # Demo script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 📚 API Documentation

### Main Endpoints

#### Encode Message
```http
POST /api/encode
Content-Type: application/json

{
  "message": "01",
  "apply_steganography": true,
  "watermark": "QUANTUM_TEAM"
}
```

#### Decode Message
```http
POST /api/decode
Content-Type: application/json

{
  "session_id": "..."
}
```

#### Steganography - Hide Message
```http
POST /api/steganography/hide
Content-Type: application/json

{
  "message": "Secret message",
  "watermark": "TEAM_NAME"
}
```

#### Steganography - Extract Message
```http
POST /api/steganography/extract
Content-Type: application/json

{
  "session_id": "..."
}
```

#### Server Status
```http
GET /api/status
```

For complete API documentation, visit `http://localhost:5000/` when the server is running.

## 🎯 Technical Highlights

### Quantum Steganography
- **Entanglement-based hiding**: Messages encoded in Bell state transformations
- **Noise camouflage**: Transmissions appear as random quantum noise
- **Cryptographic security**: Only intended recipient can decode
- **Watermark embedding**: Team identity hidden across multiple runs

### VR Visualization
- **Real-time 3D rendering**: Quantum states as visual objects
- **Interactive controls**: Gesture-based quantum operations
- **Educational gamification**: Learning through play
- **Multi-user support**: Collaborative quantum experiments

## 🔐 Security Features

- **Quantum key distribution** principles
- **Entanglement-based authentication**
- **Steganographic message hiding**
- **Eavesdropper detection**
- **Environment variable** for API keys (never hardcode secrets!)

## 🎓 Educational Resources

This project includes comprehensive guides:

- **[Complete Beginner's Guide](Quantum_Superdense_Coding_Complete_Guide.md)** - Full introduction to quantum computing and superdense coding
- **[Visual Guide](Quantum_Visual_Guide.md)** - ASCII diagrams and visual representations
- **[Interactive Features Guide](INTERACTIVE_FEATURES_GUIDE.md)** - How to use all interactive features
- **[Exercises Guide](Quantum_Exercises_Guide.md)** - Hands-on learning activities

## 🛡️ Security Best Practices

1. **Never commit API keys** - Use environment variables
2. **Use `.env` files** for local development (already in `.gitignore`)
3. **Rotate API keys** regularly if exposed
4. **Review code** before pushing to public repositories

## 🧪 Technologies Used

- **Python 3.8+**
- **Qiskit** - Quantum computing framework
- **Flask** - Web server framework
- **Three.js** - 3D graphics library
- **Dash/Plotly** - Interactive visualizations
- **NumPy, SciPy** - Scientific computing
- **Cryptography** - Security libraries

## 📋 Requirements

See `requirements.txt` for complete list. Key dependencies:
- qiskit==0.44.1
- flask==2.2.5
- numpy==1.24.3
- plotly==5.15.0
- dash==2.11.1

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source. Please check the repository for license information.

## 🏆 Hackathon Impact

This project demonstrates:
- **Innovative quantum communication** beyond standard protocols
- **Practical quantum steganography** implementation
- **Immersive quantum education** through VR
- **Real-world quantum security** applications

## 🐛 Troubleshooting

### Server won't start
- Check if port 5000 is already in use
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Ensure Python 3.8+ is being used

### API key not working
- Verify the API key is set correctly: `echo $GEMINI_API_KEY` (Linux/Mac) or `$env:GEMINI_API_KEY` (Windows)
- Check API key format (should start with "AIza...")
- Verify internet connectivity

### Import errors
- Activate your virtual environment
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

## 📞 Support

For issues, questions, or contributions:
1. Check existing documentation in the repository
2. Review the troubleshooting section above
3. Open an issue on GitHub

---

**Built with ❤️ for Quantum Innovation**

*"Exploring the quantum realm, one qubit at a time!"*
