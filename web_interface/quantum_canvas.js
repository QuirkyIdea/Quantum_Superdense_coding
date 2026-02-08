// High-fidelity Three.js visualization for Quantum Superdense Coding
// Scene: starfield, glowing Alice/Bob orbs, animated entanglement beam, particle qubit flow

(function(){
	let THREERef = window.THREE;
	let scene, camera, renderer, clock;
	let starfield, alice, bob, beam, particles, aliceRings, bobRings;
	let containerEl;
	let currentState = { message: '00', pauli: 'I', stego: false, active: false };
	let measurementBits = null;
	let isTransmitting = false;
	let isInitialized = false;

	const colors = {
		bg: 0x03060f,
		alice: 0xff6b6b,
		bob: 0x00d4ff,
		beam: 0x9b59ff,
		noise: 0x777777,
		I: 0x4CAF50,
		X: 0xff6b6b,
		Z: 0x00d4ff,
		Y: 0xffd700,
		measurement: 0x00ff88
	};

	function init(container) {
		console.log('QCanvas.init called with container:', container);
		containerEl = container;
		if (!containerEl) {
			console.error('No container provided to QCanvas.init');
			return;
		}

		// Remove loading spinner
		const loadingSpinner = containerEl.querySelector('.loading');
		if (loadingSpinner) {
			loadingSpinner.remove();
		}

		// Check if Three.js is available
		if (!THREERef) {
			console.log('Three.js not available, using 2D fallback');
			initFallback2D(containerEl);
			return;
		}
		
		console.log('Initializing 3D scene...');
		try {
			// Renderer
			renderer = new THREERef.WebGLRenderer({ antialias: true, alpha: true });
			renderer.setSize(containerEl.clientWidth, containerEl.clientHeight);
			renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
			containerEl.appendChild(renderer.domElement);

			// Scene & Camera
			scene = new THREERef.Scene();
			camera = new THREERef.PerspectiveCamera(55, containerEl.clientWidth / containerEl.clientHeight, 0.1, 1000);
			camera.position.set(0, 1.2, 7);
			clock = new THREERef.Clock();

			// Lighting
			const ambient = new THREERef.AmbientLight(0xffffff, 0.25);
			scene.add(ambient);
			const dir = new THREERef.DirectionalLight(0xffffff, 0.6);
			dir.position.set(3, 5, 2);
			scene.add(dir);

			// Starfield
			starfield = createStarfield(1000, 30);
			scene.add(starfield);

			// Alice and Bob avatars (enhanced orbs)
			alice = createAvatar(colors.alice, 'Alice');
			alice.position.set(-2.5, 0, 0);
			scene.add(alice);

			bob = createAvatar(colors.bob, 'Bob');
			bob.position.set(2.5, 0, 0);
			scene.add(bob);

			// Decorative rings around avatars
			aliceRings = createRings(alice.position, colors.alice);
			bobRings = createRings(bob.position, colors.bob);
			aliceRings.forEach(r => scene.add(r));
			bobRings.forEach(r => scene.add(r));

			// Enhanced Bell state entanglement beam
			beam = createBellStateBeam(alice.position, bob.position, colors.beam);
			scene.add(beam.group);

			// Particles along beam (qubits)
			particles = createBeamParticles(alice.position, bob.position, 120);
			scene.add(particles);

			// Add orbit controls for interactive viewing
			const controls = new THREERef.OrbitControls(camera, renderer.domElement);
			controls.enableDamping = true;
			controls.dampingFactor = 0.05;
			controls.maxDistance = 15;
			controls.minDistance = 3;

			// Resize
			window.addEventListener('resize', onResize);

			isInitialized = true;
			animate();
			console.log('3D scene initialized successfully!');
		} catch (error) {
			console.error('3D initialization failed:', error);
			initFallback2D(containerEl);
		}
	}

	function createStarfield(count, radius) {
		const geom = new THREERef.BufferGeometry();
		const positions = new Float32Array(count * 3);
		const colors = new Float32Array(count * 3);
		const sizes = new Float32Array(count);
		const speeds = new Float32Array(count);
		
		for (let i = 0; i < count; i++) {
			const r = radius * Math.sqrt(Math.random());
			const theta = Math.random() * Math.PI * 2;
			const phi = Math.acos(2 * Math.random() - 1);
			positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
			positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
			positions[i * 3 + 2] = r * Math.cos(phi);
			
			// Random colors for stars
			const color = new THREERef.Color();
			color.setHSL(Math.random() * 0.1 + 0.6, 0.8, 0.5 + Math.random() * 0.5);
			colors[i * 3] = color.r;
			colors[i * 3 + 1] = color.g;
			colors[i * 3 + 2] = color.b;
			
			sizes[i] = Math.random() * 0.03 + 0.01;
			speeds[i] = Math.random() * 0.5 + 0.1;
		}
		
		geom.setAttribute('position', new THREERef.BufferAttribute(positions, 3));
		geom.setAttribute('color', new THREERef.BufferAttribute(colors, 3));
		geom.setAttribute('size', new THREERef.BufferAttribute(sizes, 1));
		geom.setAttribute('speed', new THREERef.BufferAttribute(speeds, 1));
		
		const mat = new THREERef.PointsMaterial({ 
			size: 0.02, 
			transparent: true, 
			opacity: 0.8,
			vertexColors: true,
			sizeAttenuation: true
		});
		
		const points = new THREERef.Points(geom, mat);
		points.userData = { speeds: speeds };
		return points;
	}

	function createAvatar(color, name) {
		const group = new THREERef.Group();
		group.name = name;
		
		// Core sphere with metallic material
		const coreGeom = new THREERef.SphereGeometry(0.35, 32, 32);
		const coreMat = new THREERef.MeshStandardMaterial({ 
			color, 
			emissive: color, 
			emissiveIntensity: 0.8, 
			metalness: 0.8, 
			roughness: 0.1,
			envMapIntensity: 1.5
		});
		const core = new THREERef.Mesh(coreGeom, coreMat);
		group.add(core);
		
		// Multiple glow layers
		for (let i = 1; i <= 3; i++) {
			const glowGeom = new THREERef.SphereGeometry(0.35 + i * 0.2, 32, 32);
			const glowMat = new THREERef.MeshBasicMaterial({ 
				color, 
				transparent: true, 
				opacity: 0.1 / i,
				side: THREERef.BackSide
			});
			const glow = new THREERef.Mesh(glowGeom, glowMat);
			group.add(glow);
		}
		
		// Energy field particles around the avatar
		const particleCount = 20;
		const particleGeom = new THREERef.BufferGeometry();
		const particlePositions = new Float32Array(particleCount * 3);
		const particleSizes = new Float32Array(particleCount);
		
		for (let i = 0; i < particleCount; i++) {
			const angle = (i / particleCount) * Math.PI * 2;
			const radius = 0.6 + Math.random() * 0.3;
			particlePositions[i * 3] = Math.cos(angle) * radius;
			particlePositions[i * 3 + 1] = Math.sin(angle) * radius;
			particlePositions[i * 3 + 2] = (Math.random() - 0.5) * 0.2;
			particleSizes[i] = Math.random() * 0.05 + 0.02;
		}
		
		particleGeom.setAttribute('position', new THREERef.BufferAttribute(particlePositions, 3));
		particleGeom.setAttribute('size', new THREERef.BufferAttribute(particleSizes, 1));
		
		const particleMat = new THREERef.PointsMaterial({
			color: color,
			size: 0.05,
			transparent: true,
			opacity: 0.8,
			sizeAttenuation: true
		});
		
		const particles = new THREERef.Points(particleGeom, particleMat);
		group.add(particles);
		group.userData = { particles: particles, particleCount: particleCount, color: color };
		
		return group;
	}

	function createRings(position, color) {
		const rings = [];
		for (let i = 0; i < 3; i++) {
			const ringGeom = new THREERef.RingGeometry(0.6 + i * 0.2, 0.7 + i * 0.2, 32);
			const ringMat = new THREERef.MeshBasicMaterial({ 
				color, 
				transparent: true, 
				opacity: 0.1 - i * 0.02,
				side: THREERef.DoubleSide 
			});
			const ring = new THREERef.Mesh(ringGeom, ringMat);
			ring.position.copy(position);
			ring.rotation.x = Math.PI / 2;
			rings.push(ring);
		}
		return rings;
	}

	function createBellStateBeam(start, end, color) {
		const group = new THREERef.Group();
		
		// Main entanglement line
		const pts = [ start.clone(), end.clone() ];
		const geom = new THREERef.BufferGeometry().setFromPoints(pts);
		const mat = new THREERef.LineBasicMaterial({ color, transparent: true, opacity: 0.8 });
		const line = new THREERef.Line(geom, mat);
		group.add(line);
		
		// Cylindrical beam for thickness
		const dir = new THREERef.Vector3().subVectors(end, start);
		const length = dir.length();
		const cylGeom = new THREERef.CylinderGeometry(0.03, 0.03, length, 16, 1, true);
		const cylMat = new THREERef.MeshBasicMaterial({ color, transparent: true, opacity: 0.2 });
		const cylinder = new THREERef.Mesh(cylGeom, cylMat);
		const midpoint = new THREERef.Vector3().addVectors(start, end).multiplyScalar(0.5);
		cylinder.position.copy(midpoint);
		cylinder.quaternion.setFromUnitVectors(new THREERef.Vector3(0, 1, 0), dir.clone().normalize());
		group.add(cylinder);
		
		// Add pulsing energy nodes along the beam
		const nodeCount = 5;
		for (let i = 0; i < nodeCount; i++) {
			const t = i / (nodeCount - 1);
			const nodePos = new THREERef.Vector3().lerpVectors(start, end, t);
			
			const nodeGeom = new THREERef.SphereGeometry(0.05, 16, 16);
			const nodeMat = new THREERef.MeshBasicMaterial({ 
				color, 
				transparent: true, 
				opacity: 0.6 
			});
			const node = new THREERef.Mesh(nodeGeom, nodeMat);
			node.position.copy(nodePos);
			node.userData = { originalScale: 1, pulsePhase: i * 0.5 };
			group.add(node);
		}
		
		return { group, line, halo: cylinder };
	}

	function createBeamParticles(start, end, count) {
		const geom = new THREERef.BufferGeometry();
		const positions = new Float32Array(count * 3);
		const speeds = new Float32Array(count);
		const sizes = new Float32Array(count);
		const colors = new Float32Array(count * 3);
		const phases = new Float32Array(count);
		
		for (let i = 0; i < count; i++) {
			const t = Math.random();
			const x = start.x + (end.x - start.x) * t;
			const y = start.y + (end.y - start.y) * t + (Math.random() - 0.5) * 0.3;
			const z = start.z + (end.z - start.z) * t + (Math.random() - 0.5) * 0.3;
			positions[i * 3] = x;
			positions[i * 3 + 1] = y;
			positions[i * 3 + 2] = z;
			speeds[i] = 0.3 + Math.random() * 0.8;
			sizes[i] = Math.random() * 0.08 + 0.03;
			phases[i] = Math.random() * Math.PI * 2;
			
			// Color gradient from start to end
			const color = new THREERef.Color();
			color.setHSL(0.7 + t * 0.1, 0.8, 0.5 + t * 0.3);
			colors[i * 3] = color.r;
			colors[i * 3 + 1] = color.g;
			colors[i * 3 + 2] = color.b;
		}
		
		geom.setAttribute('position', new THREERef.BufferAttribute(positions, 3));
		geom.setAttribute('speed', new THREERef.BufferAttribute(speeds, 1));
		geom.setAttribute('size', new THREERef.BufferAttribute(sizes, 1));
		geom.setAttribute('color', new THREERef.BufferAttribute(colors, 3));
		geom.setAttribute('phase', new THREERef.BufferAttribute(phases, 1));
		
		const mat = new THREERef.PointsMaterial({ 
			size: 0.06, 
			transparent: true, 
			opacity: 0.9,
			vertexColors: true,
			sizeAttenuation: true,
			blending: THREERef.AdditiveBlending
		});
		
		const pts = new THREERef.Points(geom, mat);
		pts.frustumCulled = false;
		return pts;
	}

	function setState(message, pauli, stego) {
		currentState.message = message;
		currentState.pauli = pauli;
		currentState.stego = stego;
		
		// Update beam color per Pauli
		if (beam && beam.line) {
			const color = colors[pauli] || colors.beam;
			beam.line.material.color.setHex(color);
			if (beam.halo && beam.halo.material) beam.halo.material.color.setHex(color);
		}
		
		// Update Alice's avatar based on Pauli operation
		updateAvatarForPauli(alice, pauli);
		
		// Noise visual
		if (particles) {
			const material = particles.material;
			material.color.setHex(stego ? colors.noise : colors.beam);
			material.opacity = stego ? 0.5 : 0.9;
		}
	}

	function updateAvatarForPauli(avatar, pauli) {
		if (!avatar) return;
		
		const color = colors[pauli] || colors.alice;
		avatar.userData.color = color;
		
		// Update core material
		avatar.children.forEach(child => {
			if (child.material) {
				child.material.color.setHex(color);
				if (child.material.emissive) {
					child.material.emissive.setHex(color);
				}
			}
		});
		
		// Add rotation effect based on Pauli
		avatar.userData.pauliRotation = {
			X: { axis: 'x', speed: 2.0 },
			Z: { axis: 'z', speed: 1.5 },
			Y: { axis: 'y', speed: 2.5 },
			I: { axis: 'y', speed: 0.5 }
		}[pauli] || { axis: 'y', speed: 0.5 };
	}

	function animateBellPair(active) {
		currentState.active = active;
	}

	function playSendAnimation() {
		if (!alice || !bob) return;
		
		// Reset transmission state to allow multiple animations
		isTransmitting = false;
		
		// Small delay to ensure state is reset
		setTimeout(() => {
			if (isTransmitting) return; // Double check
			isTransmitting = true;
			
			// Create main qubit ball that Alice "throws" to Bob
			const qubitBall = createGlowingOrb(colors.alice);
			qubitBall.position.copy(alice.position);
			qubitBall.scale.set(0.5, 0.5, 0.5); // Larger ball for better visibility
			scene.add(qubitBall);
			
			// Create energy wave effect at Alice's position
			const waveGeometry = new THREERef.RingGeometry(0.1, 0.3, 32);
			const waveMaterial = new THREERef.MeshBasicMaterial({
				color: colors.alice,
				transparent: true,
				opacity: 0.9,
				side: THREERef.DoubleSide
			});
			const wave = new THREERef.Mesh(waveGeometry, waveMaterial);
			wave.position.copy(alice.position);
			wave.rotation.x = Math.PI / 2;
			scene.add(wave);
			
			// Create particle trail system
			const trailParticles = [];
			
			// Animate the qubit transmission
			const startTime = clock.getElapsedTime();
			const duration = 2.5; // Longer duration for clearer movement
			
			function animateTransmission() {
				const elapsed = clock.getElapsedTime() - startTime;
				const progress = Math.min(elapsed / duration, 1);
				
				// Move qubit ball from Alice to Bob with clear arc
				const newPos = new THREERef.Vector3();
				newPos.lerpVectors(alice.position, bob.position, progress);
				
				// Add pronounced arc motion (ball goes up and down)
				const arcHeight = 1.5; // Higher arc for better visibility
				const arcProgress = Math.sin(progress * Math.PI);
				newPos.y += arcHeight * arcProgress;
				
				qubitBall.position.copy(newPos);
				
				// Scale and rotate qubit during transmission
				const scale = 0.5 + progress * 0.8;
				qubitBall.scale.set(scale, scale, scale);
				qubitBall.rotation.y = progress * Math.PI * 8; // More rotation
				qubitBall.rotation.x = progress * Math.PI * 3;
				
				// Animate energy wave at Alice's position
				const waveProgress = Math.min(progress * 3, 1);
				wave.scale.setScalar(0.5 + waveProgress * 10);
				wave.material.opacity = 0.9 * (1 - waveProgress);
				
				// Create more frequent particle trail effect
				if (progress < 0.95 && Math.random() > 0.5) {
					const trailParticle = new THREERef.Mesh(
						new THREERef.SphereGeometry(0.04, 8, 8),
						new THREERef.MeshBasicMaterial({
							color: colors.alice,
							transparent: true,
							opacity: 0.9
						})
					);
					
					const trailPos = new THREERef.Vector3();
					trailPos.lerpVectors(alice.position, bob.position, progress);
					trailPos.y += arcHeight * arcProgress;
					trailParticle.position.copy(trailPos);
					trailParticle.userData = { startTime: clock.getElapsedTime(), life: 1.0 };
					scene.add(trailParticle);
					trailParticles.push(trailParticle);
				}
				
				// Animate existing trail particles
				for (let i = trailParticles.length - 1; i >= 0; i--) {
					const particle = trailParticles[i];
					const particleAge = clock.getElapsedTime() - particle.userData.startTime;
					const particleLife = particle.userData.life;
					
					if (particleAge > particleLife) {
						scene.remove(particle);
						trailParticles.splice(i, 1);
					} else {
						// Fade out and shrink
						const fadeProgress = particleAge / particleLife;
						particle.material.opacity = 0.9 * (1 - fadeProgress);
						particle.scale.setScalar(0.04 * (1 - fadeProgress * 0.5));
						
						// Add slight upward drift
						particle.position.y += 0.015;
					}
				}
				
				// Add pulsing effect to the main ball
				const pulse = Math.sin(progress * Math.PI * 10) * 0.15 + 1;
				qubitBall.scale.set(scale * pulse, scale * pulse, scale * pulse);
				
				if (progress < 1) {
					requestAnimationFrame(animateTransmission);
				} else {
					// Clean up transmission effects
					scene.remove(qubitBall);
					scene.remove(wave);
					
					// Clean up any remaining trail particles
					trailParticles.forEach(particle => {
						scene.remove(particle);
					});
					trailParticles.length = 0;
					
					// Reset transmission state
					isTransmitting = false;
					
					// Trigger Bell measurement
					setTimeout(() => {
						performBellMeasurement();
					}, 500);
				}
			}
			
			animateTransmission();
		}, 100);
	}

	function performBellMeasurement() {
		if (!bob) return;
		
		// Create measurement effect
		const measurementBurst = createGlowingOrb(colors.measurement);
		measurementBurst.position.copy(bob.position);
		measurementBurst.scale.set(0.5, 0.5, 0.5);
		scene.add(measurementBurst);
		
		// Generate measurement result (00, 01, 10, 11)
		const possibleResults = ['00', '01', '10', '11'];
		const result = possibleResults[Math.floor(Math.random() * possibleResults.length)];
		measurementBits = result;
		
		// Create glowing classical bits
		createMeasurementBits(result, bob.position);
		
		// Animate measurement burst
		const startTime = clock.getElapsedTime();
		const duration = 1.0;
		
		function animateMeasurement() {
			const elapsed = clock.getElapsedTime() - startTime;
			const progress = Math.min(elapsed / duration, 1);
			
			measurementBurst.scale.setScalar(0.5 + progress * 2);
			measurementBurst.children.forEach(child => {
				if (child.material) {
					child.material.opacity = 1 - progress * 0.8;
				}
			});
			
			if (progress < 1) {
				requestAnimationFrame(animateMeasurement);
			} else {
				scene.remove(measurementBurst);
				isTransmitting = false;
			}
		}
		
		animateMeasurement();
	}

	function createMeasurementBits(bits, position) {
		const bitGroup = new THREERef.Group();
		
		// Create two glowing spheres for the bits
		for (let i = 0; i < 2; i++) {
			const bitGeom = new THREERef.SphereGeometry(0.15, 16, 16);
			const bitMat = new THREERef.MeshBasicMaterial({
				color: colors.measurement,
				emissive: colors.measurement,
				emissiveIntensity: 0.8,
				transparent: true,
				opacity: 0.9
			});
			const bit = new THREERef.Mesh(bitGeom, bitMat);
			
			// Position bits side by side
			bit.position.x = (i - 0.5) * 0.4;
			bit.position.y = 0.8;
			bit.position.z = 0;
			
			// Add text label for the bit value
			const canvas = document.createElement('canvas');
			canvas.width = 64;
			canvas.height = 64;
			const ctx = canvas.getContext('2d');
			ctx.fillStyle = '#ffffff';
			ctx.font = 'bold 48px Arial';
			ctx.textAlign = 'center';
			ctx.textBaseline = 'middle';
			ctx.fillText(bits[i], 32, 32);
			
			const texture = new THREERef.CanvasTexture(canvas);
			const labelGeom = new THREERef.PlaneGeometry(0.2, 0.2);
			const labelMat = new THREERef.MeshBasicMaterial({
				map: texture,
				transparent: true,
				side: THREERef.DoubleSide
			});
			const label = new THREERef.Mesh(labelGeom, labelMat);
			label.position.copy(bit.position);
			label.position.z += 0.16;
			
			bitGroup.add(bit);
			bitGroup.add(label);
		}
		
		bitGroup.position.copy(position);
		scene.add(bitGroup);
		
		// Animate bits floating up
		const startTime = clock.getElapsedTime();
		const duration = 2.0;
		
		function animateBits() {
			const elapsed = clock.getElapsedTime() - startTime;
			const progress = Math.min(elapsed / duration, 1);
			
			bitGroup.position.y = position.y + progress * 1.5;
			bitGroup.rotation.y = progress * Math.PI * 2;
			
			// Fade out
			if (progress > 0.7) {
				const fadeProgress = (progress - 0.7) / 0.3;
				bitGroup.children.forEach(child => {
					if (child.material) {
						child.material.opacity = 1 - fadeProgress;
					}
				});
			}
			
			if (progress < 1) {
				requestAnimationFrame(animateBits);
			} else {
				scene.remove(bitGroup);
			}
		}
		
		animateBits();
	}

	function createGlowingOrb(color) {
		const group = new THREERef.Group();
		
		// Core sphere with enhanced material
		const coreGeom = new THREERef.SphereGeometry(0.2, 24, 24);
		const coreMat = new THREERef.MeshStandardMaterial({ 
			color, 
			emissive: color, 
			emissiveIntensity: 1.0,
			metalness: 0.3,
			roughness: 0.2,
			transparent: true,
			opacity: 0.95
		});
		const core = new THREERef.Mesh(coreGeom, coreMat);
		group.add(core);
		
		// Enhanced glow layers
		for (let i = 1; i <= 3; i++) {
			const glowGeom = new THREERef.SphereGeometry(0.2 + i * 0.08, 24, 24);
			const glowMat = new THREERef.MeshBasicMaterial({ 
				color, 
				transparent: true, 
				opacity: 0.15 / i,
				side: THREERef.BackSide,
				blending: THREERef.AdditiveBlending
			});
			const glow = new THREERef.Mesh(glowGeom, glowMat);
			group.add(glow);
		}
		
		// Add sparkle effect
		const sparkleCount = 8;
		for (let i = 0; i < sparkleCount; i++) {
			const sparkleGeom = new THREERef.SphereGeometry(0.02, 8, 8);
			const sparkleMat = new THREERef.MeshBasicMaterial({
				color: 0xffffff,
				transparent: true,
				opacity: 0.8,
				blending: THREERef.AdditiveBlending
			});
			const sparkle = new THREERef.Mesh(sparkleGeom, sparkleMat);
			
			// Position sparkles around the orb
			const angle = (i / sparkleCount) * Math.PI * 2;
			const radius = 0.25;
			sparkle.position.set(
				Math.cos(angle) * radius,
				Math.sin(angle) * radius,
				0
			);
			sparkle.userData = { angle: angle, radius: radius };
			group.add(sparkle);
		}
		
		return group;
	}

	function showMeasurement(bits, success) {
		if (!bob) return;
		
		const burst = createGlowingOrb(success ? 0x4CAF50 : 0xf44336);
		burst.position.copy(bob.position);
		scene.add(burst);
		
		setTimeout(() => { 
			scene.remove(burst); 
		}, 600);
	}

	function updateParticles(delta) {
		if (!particles) return;
		const pos = particles.geometry.attributes.position;
		const sizes = particles.geometry.attributes.size;
		const phases = particles.geometry.attributes.phase;
		const count = pos.count;
		const t = clock.getElapsedTime();
		
		for (let i = 0; i < count; i++) {
			let x = pos.getX(i);
			let y = pos.getY(i);
			let z = pos.getZ(i);
			const speed = particles.geometry.attributes.speed.getX(i);
			const phase = phases.getX(i);
			
			x += speed * delta * 2.0;
			
			// Add wave-like motion
			const waveOffset = Math.sin(t * 2 + phase) * 0.1;
			y += waveOffset * delta;
			z += Math.cos(t * 1.5 + phase) * 0.1 * delta;
			
			// Add spiral motion
			const spiralRadius = 0.05;
			const spiralSpeed = 3.0;
			const spiralAngle = t * spiralSpeed + phase;
			y += Math.sin(spiralAngle) * spiralRadius * delta;
			z += Math.cos(spiralAngle) * spiralRadius * delta;
			
			// Animate particle sizes
			const sizePulse = Math.sin(t * 4 + phase) * 0.02;
			sizes.setX(i, 0.06 + sizePulse);
			
			// Reset particle when it reaches Bob
			if (x > bob.position.x) {
				x = alice.position.x;
				y = (Math.random() - 0.5) * 0.3;
				z = (Math.random() - 0.5) * 0.3;
				phases.setX(i, Math.random() * Math.PI * 2);
			}
			
			pos.setXYZ(i, x, y, z);
		}
		pos.needsUpdate = true;
		sizes.needsUpdate = true;
		phases.needsUpdate = true;
	}

	function animate() {
		if (!renderer) return;
		requestAnimationFrame(animate);
		try {
			const t = clock.getElapsedTime();
			const delta = clock.getDelta();

		// Enhanced avatar animations with Pauli-specific effects
		if (alice) {
			alice.position.y = Math.sin(t * 1.3) * 0.15 + Math.sin(t * 0.7) * 0.05;
			
			// Pauli-specific rotation
			if (alice.userData.pauliRotation) {
				const rotation = alice.userData.pauliRotation;
				const angle = t * rotation.speed;
				switch (rotation.axis) {
					case 'x': alice.rotation.x = angle; break;
					case 'y': alice.rotation.y = angle; break;
					case 'z': alice.rotation.z = angle; break;
				}
			}
			
			// Animate avatar particles
			if (alice.userData.particles) {
				const particlePositions = alice.userData.particles.geometry.attributes.position;
				for (let i = 0; i < alice.userData.particleCount; i++) {
					const angle = (i / alice.userData.particleCount) * Math.PI * 2 + t * 0.5;
					const radius = 0.6 + Math.sin(t * 2 + i) * 0.1;
					particlePositions.setXYZ(i, 
						Math.cos(angle) * radius,
						Math.sin(angle) * radius,
						Math.sin(t * 3 + i) * 0.1
					);
				}
				particlePositions.needsUpdate = true;
			}
			
			// Animate sparkles on Alice's avatar
			alice.children.forEach(child => {
				if (child.userData && child.userData.angle !== undefined) {
					// Rotate sparkles around the avatar
					const sparkleAngle = child.userData.angle + t * 2;
					const radius = child.userData.radius;
					child.position.set(
						Math.cos(sparkleAngle) * radius,
						Math.sin(sparkleAngle) * radius,
						Math.sin(t * 3 + child.userData.angle) * 0.05
					);
					
					// Pulse sparkle opacity
					child.material.opacity = 0.6 + Math.sin(t * 4 + child.userData.angle) * 0.3;
				}
			});
		}
		
		if (bob) {
			bob.position.y = Math.cos(t * 1.1) * 0.15 + Math.cos(t * 0.8) * 0.05;
			bob.rotation.y = Math.cos(t * 0.6) * 0.1;
			
			// Animate avatar particles
			if (bob.userData.particles) {
				const particlePositions = bob.userData.particles.geometry.attributes.position;
				for (let i = 0; i < bob.userData.particleCount; i++) {
					const angle = (i / bob.userData.particleCount) * Math.PI * 2 - t * 0.7;
					const radius = 0.6 + Math.cos(t * 2.5 + i) * 0.1;
					particlePositions.setXYZ(i, 
						Math.cos(angle) * radius,
						Math.sin(angle) * radius,
						Math.cos(t * 2.5 + i) * 0.1
					);
				}
				particlePositions.needsUpdate = true;
			}
		}
		
		// Enhanced ring rotations with pulsing
		if (aliceRings) aliceRings.forEach((ring, i) => {
			ring.rotation.z = t * (0.5 + i * 0.2);
			ring.scale.setScalar(1 + Math.sin(t * 2 + i) * 0.1);
		});
		if (bobRings) bobRings.forEach((ring, i) => {
			ring.rotation.z = -t * (0.5 + i * 0.2);
			ring.scale.setScalar(1 + Math.cos(t * 2.5 + i) * 0.1);
		});

		// Enhanced Bell state beam with pulsing nodes
		if (beam && currentState.active) {
			const pulseIntensity = Math.sin(t * 8) * 0.3 + 0.7;
			beam.line.material.opacity = 0.6 + Math.sin(t * 6) * 0.3;
			
			if (beam.halo && beam.halo.material) {
				beam.halo.material.opacity = 0.25 + Math.sin(t * 5) * 0.15;
				beam.halo.material.emissive = new THREERef.Color(colors.beam).multiplyScalar(pulseIntensity * 0.5);
			}
			
			// Animate beam nodes
			beam.group.children.forEach(child => {
				if (child.userData && child.userData.pulsePhase !== undefined) {
					const pulse = Math.sin(t * 3 + child.userData.pulsePhase) * 0.3 + 0.7;
					child.scale.setScalar(child.userData.originalScale * pulse);
					child.material.opacity = 0.6 * pulse;
				}
			});
			
			// Add color cycling effect
			const hue = (t * 0.5) % 1;
			const color = new THREERef.Color().setHSL(hue, 0.8, 0.6);
			beam.line.material.color.copy(color);
		} else if (beam) {
			beam.line.material.opacity = 0.4 + Math.sin(t * 2) * 0.1;
			if (beam.halo && beam.halo.material) {
				beam.halo.material.opacity = 0.15 + Math.sin(t * 1.5) * 0.05;
			}
		}

		updateParticles(delta);
		
		// Animate starfield
		if (starfield && starfield.userData.speeds) {
			const starPositions = starfield.geometry.attributes.position;
			const speeds = starfield.userData.speeds;
			for (let i = 0; i < starPositions.count; i++) {
				const z = starPositions.getZ(i);
				const speed = speeds[i];
				starPositions.setZ(i, z - speed * delta * 0.5);
				if (z < -30) {
					starPositions.setZ(i, 30);
				}
			}
			starPositions.needsUpdate = true;
		}
		
		renderer.render(scene, camera);
		} catch (error) {
			console.error('Animation error:', error);
		}
	}

	function onResize() {
		if (!renderer || !camera || !containerEl) return;
		camera.aspect = containerEl.clientWidth / containerEl.clientHeight;
		camera.updateProjectionMatrix();
		renderer.setSize(containerEl.clientWidth, containerEl.clientHeight);
	}

	// Enhanced visualization functions
	function updateAvatarForPauli(avatar, pauli) {
		if (!avatar) return;
		
		const color = colors[pauli] || colors.alice;
		avatar.userData.color = color;
		
		// Update core material
		avatar.children.forEach(child => {
			if (child.material) {
				child.material.color.setHex(color);
				if (child.material.emissive) {
					child.material.emissive.setHex(color);
				}
			}
		});
		
		// Add rotation effect based on Pauli
		avatar.userData.pauliRotation = {
			X: { axis: 'x', speed: 2.0 },
			Z: { axis: 'z', speed: 1.5 },
			Y: { axis: 'y', speed: 2.5 },
			I: { axis: 'y', speed: 0.5 }
		}[pauli] || { axis: 'y', speed: 0.5 };
	}

	function performBellMeasurement() {
		if (!bob) return;
		
		// Create measurement effect
		const measurementBurst = createGlowingOrb(colors.measurement);
		measurementBurst.position.copy(bob.position);
		measurementBurst.scale.set(0.5, 0.5, 0.5);
		scene.add(measurementBurst);
		
		// Generate measurement result (00, 01, 10, 11)
		const possibleResults = ['00', '01', '10', '11'];
		const result = possibleResults[Math.floor(Math.random() * possibleResults.length)];
		measurementBits = result;
		
		// Create glowing classical bits
		createMeasurementBits(result, bob.position);
		
		// Animate measurement burst
		const startTime = clock.getElapsedTime();
		const duration = 1.0;
		
		function animateMeasurement() {
			const elapsed = clock.getElapsedTime() - startTime;
			const progress = Math.min(elapsed / duration, 1);
			
			measurementBurst.scale.setScalar(0.5 + progress * 2);
			measurementBurst.children.forEach(child => {
				if (child.material) {
					child.material.opacity = 1 - progress * 0.8;
				}
			});
			
			if (progress < 1) {
				requestAnimationFrame(animateMeasurement);
			} else {
				scene.remove(measurementBurst);
				// Ensure transmission state is reset
				isTransmitting = false;
			}
		}
		
		animateMeasurement();
	}

	function createMeasurementBits(bits, position) {
		const bitGroup = new THREERef.Group();
		
		// Create two glowing spheres for the bits
		for (let i = 0; i < 2; i++) {
			const bitGeom = new THREERef.SphereGeometry(0.15, 16, 16);
			const bitMat = new THREERef.MeshBasicMaterial({
				color: colors.measurement,
				emissive: colors.measurement,
				emissiveIntensity: 0.8,
				transparent: true,
				opacity: 0.9
			});
			const bit = new THREERef.Mesh(bitGeom, bitMat);
			
			// Position bits side by side
			bit.position.x = (i - 0.5) * 0.4;
			bit.position.y = 0.8;
			bit.position.z = 0;
			
			bitGroup.add(bit);
		}
		
		bitGroup.position.copy(position);
		scene.add(bitGroup);
		
		// Animate bits floating up
		const startTime = clock.getElapsedTime();
		const duration = 2.0;
		
		function animateBits() {
			const elapsed = clock.getElapsedTime() - startTime;
			const progress = Math.min(elapsed / duration, 1);
			
			bitGroup.position.y = position.y + progress * 1.5;
			bitGroup.rotation.y = progress * Math.PI * 2;
			
			// Fade out
			if (progress > 0.7) {
				const fadeProgress = (progress - 0.7) / 0.3;
				bitGroup.children.forEach(child => {
					if (child.material) {
						child.material.opacity = 1 - fadeProgress;
					}
				});
			}
			
			if (progress < 1) {
				requestAnimationFrame(animateBits);
			} else {
				scene.remove(bitGroup);
			}
		}
		
		animateBits();
	}

	// Public API
	window.QCanvas = { 
		init, 
		setState, 
		animateBellPair, 
		showMeasurement, 
		playSendAnimation,
		getMeasurementBits: () => measurementBits,
		isInitialized: () => isInitialized
	};

	// Fallback 2D canvas if WebGL/THREE unavailable
	function initFallback2D(container) {
		console.log('Initializing 2D fallback canvas...');
		const canvas = document.createElement('canvas');
		canvas.width = container.clientWidth;
		canvas.height = container.clientHeight;
		canvas.style.width = '100%';
		canvas.style.height = '100%';
		canvas.style.borderRadius = '10px';
		container.appendChild(canvas);
		const ctx = canvas.getContext('2d');
		let t = 0;
		function draw() {
			const w = canvas.width, h = canvas.height;
			ctx.clearRect(0, 0, w, h);
			// gradient bg
			const g = ctx.createRadialGradient(w*0.5, h*0.5, 0, w*0.5, h*0.5, Math.max(w,h)*0.6);
			g.addColorStop(0, '#060b1e');
			g.addColorStop(1, '#0a0f28');
			ctx.fillStyle = g;
			ctx.fillRect(0,0,w,h);
			// stars
			for (let i=0;i<120;i++) {
				const x = (i*97)%w, y=(i*57)%h; const a = 0.3+0.7*Math.abs(Math.sin((t+i)*0.02));
				ctx.fillStyle = `rgba(180,190,255,${a})`;
				ctx.fillRect(x, y, 2, 2);
			}
			// alice orb
			const ay = h*0.5 + Math.sin(t*0.05)*8;
			drawOrb(ctx, w*0.25, ay, 26, '#ff6b6b');
			// bob orb
			const by = h*0.5 + Math.cos(t*0.05)*8;
			drawOrb(ctx, w*0.75, by, 26, '#00d4ff');
			// beam
			ctx.strokeStyle = '#9b59ff';
			ctx.globalAlpha = 0.5 + 0.3*Math.sin(t*0.15);
			ctx.lineWidth = 3;
			ctx.beginPath(); ctx.moveTo(w*0.25, ay); ctx.lineTo(w*0.75, by); ctx.stroke();
			ctx.globalAlpha = 1;
			t++;
			requestAnimationFrame(draw);
		}
		function drawOrb(ctx, x, y, r, color){
			const glow = ctx.createRadialGradient(x, y, r*0.2, x, y, r*1.6);
			glow.addColorStop(0, hexToRgba(color,0.8));
			glow.addColorStop(1, hexToRgba(color,0.0));
			ctx.fillStyle = glow; ctx.beginPath(); ctx.arc(x,y,r*1.6,0,Math.PI*2); ctx.fill();
			ctx.fillStyle = color; ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.fill();
		}
		function hexToRgba(hex, a){
			const c = hex.replace('#','');
			const r = parseInt(c.substring(0,2),16);
			const g = parseInt(c.substring(2,4),16);
			const b = parseInt(c.substring(4,6),16);
			return `rgba(${r},${g},${b},${a})`;
		}
		draw();
	}
})();
