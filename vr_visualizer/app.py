"""
Main VR Application for Quantum Superdense Coding Visualization
"""

import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import json
from quantum_core.superdense_coding import SuperdenseCoding
from quantum_core.steganography import QuantumSteganography
import threading
import time

class VRVisualizer:
    """Main VR/3D Visualizer for Quantum Superdense Coding"""
    
    def __init__(self):
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
        self.superdense_coding = SuperdenseCoding()
        self.steganography = QuantumSteganography()
        
        # Game state
        self.game_state = {
            'alice_position': [0, 0, 0],
            'bob_position': [5, 0, 0],
            'bell_pair_active': False,
            'current_message': None,
            'pauli_operation': None,
            'measurement_result': None,
            'game_mode': 'learning',  # 'learning' or 'challenge'
            'score': 0,
            'messages_sent': 0
        }
        
        self.setup_layout()
        self.setup_callbacks()
    
    def setup_layout(self):
        """Setup the main application layout"""
        self.app.layout = dbc.Container([
            # Header
            dbc.Row([
                dbc.Col([
                    html.H1("🚀 Quantum Superdense Coding VR Visualizer", 
                           className="text-center text-primary mb-4"),
                    html.P("Immersive 3D visualization of quantum communication with steganography",
                           className="text-center text-muted")
                ])
            ]),
            
            # Main content area
            dbc.Row([
                # 3D Visualization Panel
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("🎮 3D Quantum Space"),
                        dbc.CardBody([
                            dcc.Graph(
                                id='quantum-3d-scene',
                                style={'height': '600px'},
                                config={'displayModeBar': False}
                            )
                        ])
                    ], className="mb-4")
                ], width=8),
                
                # Control Panel
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("🎛️ Quantum Controls"),
                        dbc.CardBody([
                            # Game Mode Selection
                            html.H6("Game Mode"),
                            dbc.ButtonGroup([
                                dbc.Button("Learning", id="btn-learning", color="primary", outline=True),
                                dbc.Button("Challenge", id="btn-challenge", color="success", outline=True)
                            ], className="mb-3"),
                            
                            # Message Input
                            html.H6("Send Message"),
                            dbc.Select(
                                id="message-select",
                                options=[
                                    {"label": "00", "value": "00"},
                                    {"label": "01", "value": "01"},
                                    {"label": "10", "value": "10"},
                                    {"label": "11", "value": "11"}
                                ],
                                value="00",
                                className="mb-3"
                            ),
                            
                            # Pauli Operations
                            html.H6("Pauli Operations"),
                            dbc.ButtonGroup([
                                dbc.Button("I", id="btn-I", color="info", size="sm"),
                                dbc.Button("X", id="btn-X", color="warning", size="sm"),
                                dbc.Button("Z", id="btn-Z", color="danger", size="sm"),
                                dbc.Button("Y", id="btn-Y", color="success", size="sm")
                            ], className="mb-3"),
                            
                            # Steganography Controls
                            html.H6("Steganography"),
                            dbc.Switch(
                                id="steganography-switch",
                                label="Hide in Noise",
                                value=True,
                                className="mb-3"
                            ),
                            
                            # Watermark Input
                            dbc.Input(
                                id="watermark-input",
                                placeholder="Team Watermark",
                                value="QUANTUM_TEAM",
                                className="mb-3"
                            ),
                            
                            # Send Button
                            dbc.Button(
                                "🚀 Send Quantum Message",
                                id="send-button",
                                color="primary",
                                size="lg",
                                className="w-100 mb-3"
                            ),
                            
                            # Bell Measurement
                            dbc.Button(
                                "🔍 Perform Bell Measurement",
                                id="measure-button",
                                color="secondary",
                                size="lg",
                                className="w-100 mb-3"
                            )
                        ])
                    ], className="mb-4"),
                    
                    # Results Panel
                    dbc.Card([
                        dbc.CardHeader("📊 Results"),
                        dbc.CardBody(id="results-panel")
                    ]),
                    
                    # Game Stats
                    dbc.Card([
                        dbc.CardHeader("🏆 Game Statistics"),
                        dbc.CardBody(id="game-stats")
                    ])
                ], width=4)
            ]),
            
            # Hidden divs for storing state
            dcc.Store(id='game-state-store', data=self.game_state),
            dcc.Store(id='quantum-circuit-store'),
            dcc.Interval(id='animation-interval', interval=100, n_intervals=0)
            
        ], fluid=True)
    
    def setup_callbacks(self):
        """Setup all application callbacks"""
        
        @self.app.callback(
            Output('quantum-3d-scene', 'figure'),
            [Input('animation-interval', 'n_intervals'),
             Input('game-state-store', 'data')]
        )
        def update_3d_scene(n_intervals, game_state):
            return self.create_3d_scene(game_state)
        
        @self.app.callback(
            [Output('game-state-store', 'data'),
             Output('quantum-circuit-store', 'data')],
            [Input('send-button', 'n_clicks'),
             Input('measure-button', 'n_clicks'),
             Input('btn-I', 'n_clicks'),
             Input('btn-X', 'n_clicks'),
             Input('btn-Z', 'n_clicks'),
             Input('btn-Y', 'n_clicks')],
            [State('message-select', 'value'),
             State('steganography-switch', 'value'),
             State('watermark-input', 'value'),
             State('game-state-store', 'data')]
        )
        def handle_quantum_operations(send_clicks, measure_clicks, 
                                   i_clicks, x_clicks, z_clicks, y_clicks,
                                   message, steganography, watermark, game_state):
            
            ctx = callback_context
            if not ctx.triggered:
                return game_state, {}
            
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            
            if button_id == 'send-button' and send_clicks:
                # Send quantum message
                return self.send_quantum_message(message, steganography, watermark, game_state)
            
            elif button_id == 'measure-button' and measure_clicks:
                # Perform Bell measurement
                return self.perform_bell_measurement(game_state)
            
            elif button_id in ['btn-I', 'btn-X', 'btn-Z', 'btn-Y']:
                # Apply Pauli operation
                pauli_op = button_id.split('-')[1]
                return self.apply_pauli_operation(pauli_op, game_state)
            
            return game_state, {}
        
        @self.app.callback(
            Output('results-panel', 'children'),
            [Input('game-state-store', 'data')]
        )
        def update_results_panel(game_state):
            return self.create_results_panel(game_state)
        
        @self.app.callback(
            Output('game-stats', 'children'),
            [Input('game-state-store', 'data')]
        )
        def update_game_stats(game_state):
            return self.create_game_stats(game_state)
    
    def create_3d_scene(self, game_state):
        """Create 3D scene with quantum elements"""
        
        # Create 3D figure
        fig = go.Figure()
        
        # Add Alice (sender)
        fig.add_trace(go.Scatter3d(
            x=[game_state['alice_position'][0]],
            y=[game_state['alice_position'][1]],
            z=[game_state['alice_position'][2]],
            mode='markers+text',
            marker=dict(size=15, color='red', symbol='diamond'),
            text=['Alice'],
            textposition='top center',
            name='Alice'
        ))
        
        # Add Bob (receiver)
        fig.add_trace(go.Scatter3d(
            x=[game_state['bob_position'][0]],
            y=[game_state['bob_position'][1]],
            z=[game_state['bob_position'][2]],
            mode='markers+text',
            marker=dict(size=15, color='blue', symbol='diamond'),
            text=['Bob'],
            textposition='top center',
            name='Bob'
        ))
        
        # Add Bell pair connection if active
        if game_state['bell_pair_active']:
            fig.add_trace(go.Scatter3d(
                x=[game_state['alice_position'][0], game_state['bob_position'][0]],
                y=[game_state['alice_position'][1], game_state['bob_position'][1]],
                z=[game_state['alice_position'][2], game_state['bob_position'][2]],
                mode='lines',
                line=dict(color='purple', width=8, dash='dot'),
                name='Bell Pair'
            ))
            
            # Add quantum state visualization
            if game_state['pauli_operation']:
                self.add_quantum_state_visualization(fig, game_state)
        
        # Add measurement result if available
        if game_state['measurement_result']:
            self.add_measurement_visualization(fig, game_state)
        
        # Update layout
        fig.update_layout(
            title="Quantum Superdense Coding 3D Space",
            scene=dict(
                xaxis=dict(title="X", range=[-2, 7]),
                yaxis=dict(title="Y", range=[-2, 2]),
                zaxis=dict(title="Z", range=[-2, 2]),
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            showlegend=True,
            height=600
        )
        
        return fig
    
    def add_quantum_state_visualization(self, fig, game_state):
        """Add quantum state visualization to 3D scene"""
        
        # Create Bloch sphere representation
        phi = np.linspace(0, 2*np.pi, 100)
        theta = np.linspace(0, np.pi, 100)
        
        # Bloch sphere surface
        x_sphere = np.outer(np.cos(phi), np.sin(theta))
        y_sphere = np.outer(np.sin(phi), np.sin(theta))
        z_sphere = np.outer(np.ones_like(phi), np.cos(theta))
        
        # Scale and position the Bloch sphere
        scale = 0.5
        x_sphere = x_sphere * scale + 2.5
        y_sphere = y_sphere * scale
        z_sphere = z_sphere * scale
        
        fig.add_trace(go.Surface(
            x=x_sphere, y=y_sphere, z=z_sphere,
            colorscale='Viridis',
            opacity=0.3,
            name='Quantum State'
        ))
        
        # Add state vector
        if game_state['pauli_operation']:
            color_map = {'I': 'green', 'X': 'red', 'Z': 'blue', 'Y': 'yellow'}
            color = color_map.get(game_state['pauli_operation'], 'purple')
            
            fig.add_trace(go.Scatter3d(
                x=[2.5, 2.5 + 0.3],
                y=[0, 0.3],
                z=[0, 0],
                mode='lines',
                line=dict(color=color, width=5),
                name=f'State Vector ({game_state["pauli_operation"]})'
            ))
    
    def add_measurement_visualization(self, fig, game_state):
        """Add measurement result visualization"""
        
        result = game_state['measurement_result']
        x_pos = game_state['bob_position'][0] + 1
        
        fig.add_trace(go.Scatter3d(
            x=[x_pos],
            y=[0],
            z=[0],
            mode='markers+text',
            marker=dict(size=20, color='orange', symbol='star'),
            text=[f'Result: {result}'],
            textposition='top center',
            name='Measurement'
        ))
    
    def send_quantum_message(self, message, steganography, watermark, game_state):
        """Send quantum message with steganography"""
        
        # Update game state
        game_state['bell_pair_active'] = True
        game_state['current_message'] = message
        game_state['messages_sent'] += 1
        
        # Create quantum circuit
        if steganography:
            circuit_data = self.steganography.create_noise_circuit(message, watermark)
        else:
            circuit_data = self.superdense_coding.encode_message(message, apply_steganography=False, watermark=watermark)
        
        return game_state, circuit_data
    
    def perform_bell_measurement(self, game_state):
        """Perform Bell measurement"""
        
        if game_state['current_message']:
            # Simulate measurement
            possible_results = ['00', '01', '10', '11']
            result = np.random.choice(possible_results, p=[0.25, 0.25, 0.25, 0.25])
            
            game_state['measurement_result'] = result
            
            # Update score
            if result == game_state['current_message']:
                game_state['score'] += 10
            
            # Reset for next round
            game_state['bell_pair_active'] = False
            game_state['current_message'] = None
            game_state['pauli_operation'] = None
        
        return game_state, {}
    
    def apply_pauli_operation(self, pauli_op, game_state):
        """Apply Pauli operation"""
        
        game_state['pauli_operation'] = pauli_op
        return game_state, {}
    
    def create_results_panel(self, game_state):
        """Create results panel content"""
        
        if game_state['measurement_result']:
            success = game_state['measurement_result'] == game_state.get('current_message', '')
            
            return [
                html.H6("Last Measurement"),
                html.P(f"Result: {game_state['measurement_result']}", 
                       className=f"text-{'success' if success else 'danger'}"),
                html.P(f"Expected: {game_state.get('current_message', 'N/A')}"),
                html.Hr(),
                html.H6("Quantum State Info"),
                html.P(f"Bell Pair: {'Active' if game_state['bell_pair_active'] else 'Inactive'}"),
                html.P(f"Pauli Operation: {game_state.get('pauli_operation', 'None')}")
            ]
        
        return [html.P("No measurements yet. Send a message first!")]
    
    def create_game_stats(self, game_state):
        """Create game statistics panel"""
        
        return [
            html.H6("Game Statistics"),
            html.P(f"Score: {game_state['score']}"),
            html.P(f"Messages Sent: {game_state['messages_sent']}"),
            html.P(f"Success Rate: {game_state['score'] / max(game_state['messages_sent'], 1) * 100:.1f}%"),
            html.Hr(),
            html.H6("Current Status"),
            html.P(f"Bell Pair: {'🔗 Active' if game_state['bell_pair_active'] else '❌ Inactive'}"),
            html.P(f"Game Mode: {game_state['game_mode'].title()}")
        ]
    
    def run(self, debug=True, port=8050):
        """Run the VR visualizer application"""
        print("🚀 Starting Quantum Superdense Coding VR Visualizer...")
        print(f"🌐 Open your browser to: http://localhost:{port}")
        print("🎮 Use the controls to send quantum messages and visualize the process!")
        
        self.app.run_server(debug=debug, port=port)

if __name__ == "__main__":
    visualizer = VRVisualizer()
    visualizer.run()
