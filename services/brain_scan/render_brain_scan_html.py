"""
Brain Scan 3D Renderer — generates interactive HTML from scan JSON.

Uses Three.js for 3D rendering. Pre-computed positions, interactive rotation/zoom.
No live computation — load JSON, render, explore.

Features:
  - 3D rotatable brain with anatomy layers (stem/limbic/cortex)
  - Nodes colored by type, sized by weight, glowing by energy
  - Links colored by relation type, opacity by weight
  - Layer toggles (show/hide stem, limbic, cortex)
  - Type filter (show only desires, only concepts, etc.)
  - Hover info on nodes
"""

import json
import sys
from pathlib import Path


def render_html(scan_path: Path, output_path: Path):
    """Generate standalone HTML file with Three.js brain visualization."""
    scan = json.loads(scan_path.read_text())

    nodes_json = json.dumps(scan["nodes"])
    links_json = json.dumps(scan["links"])
    stats_json = json.dumps(scan["stats"], indent=2)
    citizen_id = scan["citizen_id"]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Brain Scan — @{citizen_id}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: #0a0a0a; color: #e0e0e0; font-family: 'SF Mono', monospace; overflow: hidden; }}
  #info {{
    position: absolute; top: 16px; left: 16px; z-index: 10;
    background: rgba(10,10,10,0.85); padding: 16px; border-radius: 8px;
    border: 1px solid #333; max-width: 300px; font-size: 12px;
  }}
  #info h2 {{ font-size: 16px; margin-bottom: 8px; color: #fff; }}
  #info .stat {{ color: #888; margin: 2px 0; }}
  #info .legend {{ margin-top: 12px; }}
  .legend-item {{ display: flex; align-items: center; gap: 6px; margin: 3px 0; cursor: pointer; }}
  .legend-dot {{ width: 10px; height: 10px; border-radius: 50%; }}
  .legend-item.dimmed {{ opacity: 0.3; }}
  #hover-info {{
    position: absolute; bottom: 16px; left: 16px; z-index: 10;
    background: rgba(10,10,10,0.9); padding: 12px; border-radius: 8px;
    border: 1px solid #444; font-size: 13px; display: none; max-width: 400px;
  }}
  #controls {{
    position: absolute; top: 16px; right: 16px; z-index: 10;
    background: rgba(10,10,10,0.85); padding: 12px; border-radius: 8px;
    border: 1px solid #333; font-size: 12px;
  }}
  #controls label {{ display: block; margin: 4px 0; cursor: pointer; }}
  canvas {{ display: block; }}
</style>
</head>
<body>

<div id="info">
  <h2>Brain Scan — @{citizen_id}</h2>
  <div class="stat">Nodes: {scan['stats']['total_nodes']}</div>
  <div class="stat">Links: {scan['stats']['total_links']}</div>
  <div class="stat">Stem: {scan['stats']['layers'].get('stem',0)} | Limbic: {scan['stats']['layers'].get('limbic',0)} | Cortex: {scan['stats']['layers'].get('cortex',0)}</div>
  <div class="legend" id="legend"></div>
</div>

<div id="controls">
  <strong>Layers</strong>
  <label><input type="checkbox" checked data-layer="stem"> Stem (processes)</label>
  <label><input type="checkbox" checked data-layer="limbic"> Limbic (desires, emotions)</label>
  <label><input type="checkbox" checked data-layer="cortex"> Cortex (values, concepts)</label>
  <hr style="border-color:#333;margin:8px 0">
  <strong>Links</strong>
  <label><input type="checkbox" checked id="showLinks"> Show links</label>
</div>

<div id="hover-info"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script>
const nodes = {nodes_json};
const links = {links_json};

// Scene
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a0a);
scene.fog = new THREE.FogExp2(0x0a0a0a, 0.3);

const camera = new THREE.PerspectiveCamera(60, window.innerWidth/window.innerHeight, 0.01, 100);
camera.position.set(0, 0.5, 2.0);

const renderer = new THREE.WebGLRenderer({{ antialias: true }});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
document.body.appendChild(renderer.domElement);

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.5;

// Lights
scene.add(new THREE.AmbientLight(0x404040, 0.5));
const pointLight = new THREE.PointLight(0xffffff, 1, 10);
pointLight.position.set(0, 2, 2);
scene.add(pointLight);

// Build legend
const typeColors = {json.dumps({k: v for k, v in {
    "process": "#22c55e", "desire": "#ef4444", "narrative": "#a855f7",
    "value": "#eab308", "concept": "#3b82f6"
}.items()})};
const legend = document.getElementById('legend');
for (const [type, color] of Object.entries(typeColors)) {{
  const item = document.createElement('div');
  item.className = 'legend-item';
  item.dataset.type = type;
  item.innerHTML = `<span class="legend-dot" style="background:${{color}}"></span>${{type}}`;
  item.onclick = () => {{
    item.classList.toggle('dimmed');
    toggleType(type, !item.classList.contains('dimmed'));
  }};
  legend.appendChild(item);
}}

// Node meshes
const nodeGroup = new THREE.Group();
const nodeMeshes = [];
const nodeById = {{}};

nodes.forEach((n, i) => {{
  const geo = new THREE.SphereGeometry(n.size * 0.003, 12, 12);
  const mat = new THREE.MeshPhongMaterial({{
    color: new THREE.Color(n.color),
    emissive: n.glow ? new THREE.Color(n.color).multiplyScalar(0.4) : new THREE.Color(0),
    transparent: true,
    opacity: 0.85,
  }});
  const mesh = new THREE.Mesh(geo, mat);
  mesh.position.set(n.x, n.z, n.y);  // z→y for upward axis
  mesh.userData = n;
  nodeGroup.add(mesh);
  nodeMeshes.push(mesh);
  nodeById[n.id] = mesh;
}});
scene.add(nodeGroup);

// Link lines
const linkGroup = new THREE.Group();
links.forEach(l => {{
  const src = nodeById[l.source];
  const tgt = nodeById[l.target];
  if (!src || !tgt) return;

  const geo = new THREE.BufferGeometry().setFromPoints([src.position, tgt.position]);
  const mat = new THREE.LineBasicMaterial({{
    color: new THREE.Color(l.color),
    transparent: true,
    opacity: l.opacity * 0.5,
    linewidth: 1,
  }});
  const line = new THREE.Line(geo, mat);
  line.userData = l;
  linkGroup.add(line);
}});
scene.add(linkGroup);

// Layer toggles
document.querySelectorAll('[data-layer]').forEach(cb => {{
  cb.addEventListener('change', () => {{
    const layer = cb.dataset.layer;
    nodeMeshes.forEach(m => {{
      if (m.userData.layer === layer) m.visible = cb.checked;
    }});
  }});
}});

document.getElementById('showLinks').addEventListener('change', (e) => {{
  linkGroup.visible = e.target.checked;
}});

// Type filter
function toggleType(type, visible) {{
  nodeMeshes.forEach(m => {{
    if (m.userData.node_type === type) m.visible = visible;
  }});
}}

// Hover detection
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
const hoverInfo = document.getElementById('hover-info');

renderer.domElement.addEventListener('mousemove', (e) => {{
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  const hits = raycaster.intersectObjects(nodeMeshes);
  if (hits.length > 0) {{
    const n = hits[0].object.userData;
    hoverInfo.style.display = 'block';
    hoverInfo.innerHTML = `
      <strong style="color:${{n.color}}">${{n.node_type}}</strong> — ${{n.label}}<br>
      <span style="color:#888">weight: ${{n.weight.toFixed(2)}} | energy: ${{n.energy.toFixed(2)}} | layer: ${{n.layer}}</span>
    `;
  }} else {{
    hoverInfo.style.display = 'none';
  }}
}});

// Resize
window.addEventListener('resize', () => {{
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}});

// Animate
function animate() {{
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}}
animate();
</script>
</body>
</html>"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html)
    print(f"Brain scan rendered to {output_path}")
    print(f"Open in browser: file://{output_path.resolve()}")


if __name__ == "__main__":
    handle = sys.argv[1] if len(sys.argv) > 1 else "dragon_slayer"
    scan_path = Path(f"data/brain_scans/{handle}_scan.json")
    output_path = Path(f"data/brain_scans/{handle}_brain.html")
    render_html(scan_path, output_path)
