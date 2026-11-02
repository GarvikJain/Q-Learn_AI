import { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Sphere, Line, Text } from '@react-three/drei';
import * as THREE from 'three';

interface BlochSphereProps {
  alpha?: { real: number, imag: number };
  beta?: { real: number, imag: number };
  numQubits: number;
}

function SphereContent({ alpha, beta }: { alpha: any, beta: any }) {
  const arrowRef = useRef<THREE.Group>(null);
  
  // Calculate spherical coordinates
  const theta = 2 * Math.acos(Math.sqrt(alpha.real**2 + alpha.imag**2));
  // Simplification for phi: just use beta phase if alpha is real and positive
  const phi = Math.atan2(beta.imag, beta.real) - Math.atan2(alpha.imag, alpha.real);

  // Convert to Cartesian for the arrow tip
  const r = 1;
  const x = r * Math.sin(theta) * Math.cos(phi);
  const y = r * Math.sin(theta) * Math.sin(phi);
  const z = r * Math.cos(theta); // Z is usually up in Bloch sphere

  // Rotate axes for Three.js (Y is up)
  const vec = new THREE.Vector3(x, z, y); 

  useFrame(() => {
    // Optional gentle rotation or animation could go here
  });

  return (
    <group>
      {/* Wireframe Sphere */}
      <Sphere args={[1, 32, 32]} position={[0,0,0]}>
        <meshBasicMaterial color="#ffffff" wireframe transparent opacity={0.15} />
      </Sphere>

      {/* Axes */}
      <Line points={[[-1.2, 0, 0], [1.2, 0, 0]]} color="#ff4444" lineWidth={1} /> {/* X */}
      <Line points={[[0, -1.2, 0], [0, 1.2, 0]]} color="#44ff44" lineWidth={1} /> {/* Z (up in ThreeJS Y) */}
      <Line points={[[0, 0, -1.2], [0, 0, 1.2]]} color="#4444ff" lineWidth={1} /> {/* Y */}

      {/* Axis Labels */}
      <Text position={[1.3, 0, 0]} fontSize={0.15} color="#ff4444">X</Text>
      <Text position={[0, 1.3, 0]} fontSize={0.15} color="#44ff44">|0⟩ (Z)</Text>
      <Text position={[0, -1.3, 0]} fontSize={0.15} color="#44ff44">|1⟩ (-Z)</Text>
      <Text position={[0, 0, 1.3]} fontSize={0.15} color="#4444ff">Y</Text>

      {/* State Vector Arrow */}
      <group ref={arrowRef}>
        <Line points={[[0, 0, 0], [vec.x, vec.y, vec.z]]} color="#a855f7" lineWidth={4} />
        <mesh position={[vec.x, vec.y, vec.z]}>
          <sphereGeometry args={[0.05, 16, 16]} />
          <meshBasicMaterial color="#a855f7" />
        </mesh>
      </group>
    </group>
  );
}

export default function BlochSphere({ alpha = {real: 1, imag: 0}, beta = {real: 0, imag: 0}, numQubits }: BlochSphereProps) {
  if (numQubits > 1) {
    return (
      <div className="w-full h-[300px] flex items-center justify-center bg-gray-900 rounded-lg border border-gray-800">
        <p className="text-gray-400 text-sm">Bloch sphere available for single-qubit states only.</p>
      </div>
    );
  }

  return (
    <div className="w-full h-[300px] bg-gray-900 rounded-lg border border-gray-800 overflow-hidden relative">
      <Canvas camera={{ position: [2, 1.5, 2], fov: 45 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />
        <SphereContent alpha={alpha} beta={beta} />
        <OrbitControls enableZoom={false} autoRotate autoRotateSpeed={1} />
      </Canvas>
    </div>
  );
}
