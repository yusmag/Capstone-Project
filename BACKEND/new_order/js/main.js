import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';


let scene, camera, renderer, controls;
let board; // will hold the loaded GLB scene
init();
animate();

function init() {
  const container = document.getElementById('viewer');

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0xf5f5f5);

  const width = container.clientWidth;
  const height = container.clientHeight || window.innerHeight;

  camera = new THREE.PerspectiveCamera(35, width / height, 0.1, 100);
  camera.position.set(0, 1.2, 3);

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(width, height);
  container.appendChild(renderer.domElement);

  // OrbitControls AFTER camera & renderer are created
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;

  // Lights
  const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 1.2);
  scene.add(hemiLight);

  const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
  dirLight.position.set(5, 10, 7);
  scene.add(dirLight);

  // Handle resize
  window.addEventListener('resize', onWindowResize);

  // Load your skimboard
  loadBoard();

  // Hook up HTML inputs to update colors
  setupUI();
}

function onWindowResize() {
  const container = document.getElementById('viewer');
  const width = container.clientWidth;
  const height = container.clientHeight || window.innerHeight;

  camera.aspect = width / height;
  camera.updateProjectionMatrix();
  renderer.setSize(width, height);
}

function animate() {
  requestAnimationFrame(animate);
  if (controls) controls.update();
  renderer.render(scene, camera);
}

/* ---------- Load skimboard model ---------- */

function loadBoard() {
  const loader = new GLTFLoader();

  loader.load(
    'assets/skimboard.glb',
    (gltf) => {
      board = gltf.scene;

      // Log meshes so you can see names
      board.traverse((child) => {
        if (child.isMesh) {
          console.log('Mesh:', child.name);
        }
      });

      scene.add(board);

      // Default colors
      updateDeckColor('#b19f00ff');
      updateTractionPadColor('white');
    },
    undefined,
    (error) => {
      console.error('Error loading model:', error);
    }
  );
}

/* ---------- Color update helpers ---------- */
const deckMeshNames = [
  'deck_top_deck_img_0',
  'stripes_top_deck_img_0',
  'stripes1_top_deck_img_0',
  'stripes2_top_deck_img_0',
  'stripes3_top_deck_img_0',
];

function updateDeckColor(hexColor) {
  if (!board) return;

  board.traverse((child) => {
    if (child.isMesh && deckMeshNames.includes(child.name)) {
      if (!child.material) return;
      child.material.color.set(hexColor);
      child.material.needsUpdate = true;
    }
  });
}

function updateTractionPadColor(option) {
  if (!board) return;

  const color = option === 'red' ? '#111111' : '#ffffff';

  board.traverse((child) => {
    if (child.isMesh && child.name === 'pCube3_pad__0') {
      if (!child.material) return;
      child.material.color.set(color);
      child.material.needsUpdate = true;
    }
  });
}

/* ---------- Hook up HTML UI ---------- */

function setupUI() {
  const deckColorInput = document.getElementById('deckColor');
  const padRadios = document.querySelectorAll('input[name="padColor"]');
  const textInput = document.getElementById('customText');
  const saveBtn = document.getElementById('saveConfig');

  deckColorInput.addEventListener('input', (e) => {
    updateDeckColor(e.target.value);
  });

  padRadios.forEach((radio) => {
    radio.addEventListener('change', (e) => {
      updateTractionPadColor(e.target.value);
    });
  });

  textInput.addEventListener('input', (e) => {
    console.log('Custom text (we’ll use this for texture later):', e.target.value);
  });

  saveBtn.addEventListener('click', () => {
    const padColor = document.querySelector('input[name="padColor"]:checked').value;
    const config = {
      deckColor: deckColorInput.value,
      padColor,
      customText: textInput.value,
    };
    console.log('Config to save:', config);
  });
}
