"""
Brain Scan 3D Renderer v3 — organic, brain-like visualization.

No straight lines. No dashes. No plastic. Curves everywhere.
Muted organic palette. Glow on links. Smaller nodes.
"""

import json
import sys
from pathlib import Path


def render_html(scan_path: Path, output_path: Path):
    scan = json.loads(scan_path.read_text())
    nodes_json = json.dumps(scan["nodes"])
    links_json = json.dumps(scan["links"])
    citizen_id = scan["citizen_id"]
    stats = scan["stats"]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Brain Scan — @{citizen_id}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: #06060c; color: #c0c0c8; font-family: 'SF Mono', 'Cascadia Code', monospace; overflow: hidden; }}
  canvas {{ filter: contrast(1.15) brightness(1.05) saturate(1.2); }}
  #info {{
    position: absolute; top: 16px; left: 16px; z-index: 10;
    background: rgba(8,8,16,0.92); padding: 14px; border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.08); max-width: 240px; font-size: 10px; line-height: 1.5;
  }}
  #info h2 {{ font-size: 13px; margin-bottom: 6px; color: #e0e0e8; font-weight: 500; }}
  .stat {{ color: #666; margin: 2px 0; }}
  .legend {{ margin-top: 8px; }}
  .legend-item {{ display: flex; align-items: center; gap: 5px; margin: 2px 0; cursor: pointer; user-select: none; font-size: 10px; }}
  .legend-item.dimmed {{ opacity: 0.15; }}
  .legend-dot {{ width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }}
  #hover-info {{
    position: absolute; bottom: 16px; left: 16px; z-index: 10;
    background: rgba(8,8,16,0.95); padding: 10px 14px; border-radius: 6px;
    border: 1px solid rgba(255,255,255,0.1); font-size: 11px; display: none; max-width: 380px; line-height: 1.5;
  }}
  #controls {{
    position: absolute; top: 16px; right: 16px; z-index: 10;
    background: rgba(8,8,16,0.92); padding: 10px; border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.08); font-size: 10px;
  }}
  #controls label {{ display: block; margin: 2px 0; cursor: pointer; }}
</style>
</head>
<body>

<div id="info">
  <h2>@{citizen_id}</h2>
  <div class="stat">{stats['total_nodes']} nodes — {stats['total_links']} links</div>
  <div class="legend" id="legend"></div>
</div>

<div id="controls">
  <label><input type="checkbox" checked id="showLinks"> Links</label>
  <label><input type="checkbox" checked id="showHalos"> Relevance halos</label>
</div>

<div id="hover-info"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script>
const nodes = {nodes_json};
const links = {links_json};

// ── Organic color palette ───────────────────────────────────
// Muted, warm, desaturated — like neural tissue under soft light
const PALETTE = {{
  process:   0x5a8a6a,  // sage green
  desire:    0xc47058,  // terracotta
  narrative: 0x8a6ab0,  // muted lavender
  value:     0xc4a040,  // old gold
  concept:   0x5878a0,  // steel blue
  memory:    0x707078,  // warm gray
  state:     0xb06888,  // dusty rose
  stimulus:  0xc08050,  // burnt sienna
  frequency: 0x508888,  // teal
}};

const LINK_PALETTE = {{
  activates:    0x5a8a6a,
  supports:     0x5878a0,
  contradicts:  0xc47058,
  reminds_of:   0x8a6ab0,
  causes:       0xc4a040,
  regulates:    0x508888,
  depends_on:   0x606068,
  exemplifies:  0x5a9878,
  associates:   0x585860,
  default:      0x484850,
}};

// ── Scene ───────────────────────────────────────────────────
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x06060c);
scene.fog = new THREE.FogExp2(0x06060c, 0.4);

const camera = new THREE.PerspectiveCamera(50, innerWidth/innerHeight, 0.01, 50);
camera.position.set(0.3, 0.5, 0.8);
camera.lookAt(0, 0.3, 0);

const renderer = new THREE.WebGLRenderer({{ antialias: true }});
renderer.setSize(innerWidth, innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
document.body.appendChild(renderer.domElement);

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.06;
controls.autoRotate = false;
controls.target.set(0, 0.3, 0);

// Soft organic lighting
scene.add(new THREE.AmbientLight(0x2a2a3e, 0.8));
const key = new THREE.PointLight(0xffe8d0, 1.0, 6);
key.position.set(0.6, 1.2, 0.8);
scene.add(key);
const rim = new THREE.PointLight(0x4060a0, 0.5, 5);
rim.position.set(-0.6, 0.2, -0.6);
scene.add(rim);
const fill = new THREE.PointLight(0xa08060, 0.3, 4);
fill.position.set(0, -0.5, 0.5);
scene.add(fill);

// ── Legend ───────────────────────────────────────────────────
const legend = document.getElementById('legend');
const activeTypes = new Set(Object.keys(PALETTE));
for (const [type, hex] of Object.entries(PALETTE)) {{
  const c = '#' + hex.toString(16).padStart(6, '0');
  const item = document.createElement('div');
  item.className = 'legend-item';
  item.innerHTML = `<span class="legend-dot" style="background:${{c}}"></span>${{type}}`;
  item.onclick = () => {{
    if (activeTypes.has(type)) {{ activeTypes.delete(type); item.classList.add('dimmed'); }}
    else {{ activeTypes.add(type); item.classList.remove('dimmed'); }}
    nodeMeshes.forEach(m => {{
      m.visible = activeTypes.has(m.userData.node_type);
    }});
  }};
  legend.appendChild(item);
}}

// ── Nodes ───────────────────────────────────────────────────
const nodeGroup = new THREE.Group();
const haloGroup = new THREE.Group();
const nodeMeshes = [];
const nodeById = {{}};

nodes.forEach(n => {{
  const geo = new THREE.SphereGeometry(n.radius * 0.003, 10, 10);
  const baseHex = PALETTE[n.node_type] || 0x585860;
  const baseColor = new THREE.Color(baseHex);

  // Patina: old nodes get slightly warmer/darker
  const patinaColor = new THREE.Color(0x6b5b4b);
  const finalColor = baseColor.clone().lerp(patinaColor, n.patina * 0.3);

  // Matte with subtle self-glow — not shiny
  const emissiveBase = baseColor.clone().multiplyScalar(0.15 + n.glow * 0.3);

  const mat = new THREE.MeshStandardMaterial({{
    color: finalColor,
    emissive: emissiveBase,
    roughness: 0.95,
    metalness: 0.0,
    transparent: true,
    opacity: Math.max(0.8, n.opacity),
  }});

  const mesh = new THREE.Mesh(geo, mat);
  mesh.position.set(n.x, n.z, n.y);
  mesh.userData = n;
  nodeGroup.add(mesh);
  nodeMeshes.push(mesh);
  nodeById[n.id] = mesh;

  // Subtle self_relevance halo (only very high)
  if (n.inner_halo > 0.8) {{
    const hGeo = new THREE.SphereGeometry(n.radius * 0.004, 8, 8);
    const hMat = new THREE.MeshBasicMaterial({{
      color: 0xc4a040, transparent: true, opacity: 0.08, depthWrite: false
    }});
    const h = new THREE.Mesh(hGeo, hMat);
    h.position.copy(mesh.position);
    h.userData = {{ type: 'inner_halo' }};
    haloGroup.add(h);
  }}
}});
scene.add(nodeGroup);
scene.add(haloGroup);

// ── Links (curved, organic) ─────────────────────────────────
const linkGroup = new THREE.Group();

links.forEach(l => {{
  const src = nodeById[l.source];
  const tgt = nodeById[l.target];
  if (!src || !tgt) return;

  const s = src.position;
  const t = tgt.position;

  // ALWAYS curved — no straight lines
  // Control point offset based on link properties
  const mid = new THREE.Vector3().addVectors(s, t).multiplyScalar(0.5);

  // Curve direction: perpendicular to link axis, magnitude from friction + weight
  const axis = new THREE.Vector3().subVectors(t, s);
  const len = axis.length();
  const perp = new THREE.Vector3(-axis.z, 0, axis.x).normalize();
  // Use a hash of source+target to get consistent curve direction
  const hash = (l.source.length + l.target.length + l.weight * 100) % 7 - 3.5;
  const curveStrength = 0.05 + l.friction * 0.1 + Math.abs(hash) * 0.01;
  const upOffset = (l.valence * 0.03);  // positive valence curves up, negative down

  mid.add(perp.multiplyScalar(curveStrength * (hash > 0 ? 1 : -1)));
  mid.y += upOffset;

  const curve = new THREE.QuadraticBezierCurve3(s, mid, t);
  const points = curve.getPoints(8);

  const geo = new THREE.BufferGeometry().setFromPoints(points);

  // Link color from palette, muted
  const linkHex = LINK_PALETTE[l.relation] || LINK_PALETTE.default;
  let linkColor = new THREE.Color(linkHex);

  // Valence shifts temperature
  if (l.valence > 0.1) {{
    linkColor.lerp(new THREE.Color(0xc4a040), l.valence * 0.3);  // warm
  }} else if (l.valence < -0.1) {{
    linkColor.lerp(new THREE.Color(0x4060a0), Math.abs(l.valence) * 0.3);  // cool
  }}

  // Affinity → saturation (low affinity = more gray, but keep some color)
  linkColor.lerp(new THREE.Color(0x404048), (1.0 - l.saturation) * 0.6);

  // Visible — trust differentiates
  const op = 0.08 + l.opacity * 0.25;

  const mat = new THREE.LineBasicMaterial({{
    color: linkColor,
    transparent: true,
    opacity: op,
  }});

  const line = new THREE.Line(geo, mat);
  line.userData = l;
  linkGroup.add(line);

  // Glow line (energy > 0.3) — wider, brighter duplicate
  if (l.glow > 0.1) {{
    const glowMat = new THREE.LineBasicMaterial({{
      color: linkColor.clone().multiplyScalar(1.5),
      transparent: true,
      opacity: l.glow * 0.1,
    }});
    const glowLine = new THREE.Line(geo.clone(), glowMat);
    linkGroup.add(glowLine);
  }}
}});
scene.add(linkGroup);

// ── Controls ────────────────────────────────────────────────
document.getElementById('showLinks').addEventListener('change', e => {{
  linkGroup.visible = e.target.checked;
}});
document.getElementById('showHalos').addEventListener('change', e => {{
  haloGroup.visible = e.target.checked;
}});

// ── Hover ───────────────────────────────────────────────────
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
const hoverInfo = document.getElementById('hover-info');

renderer.domElement.addEventListener('mousemove', e => {{
  mouse.x = (e.clientX / innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / innerHeight) * 2 + 1;
}});

function updateHover() {{
  raycaster.setFromCamera(mouse, camera);
  const hits = raycaster.intersectObjects(nodeMeshes);
  if (hits.length > 0) {{
    const n = hits[0].object.userData;
    const c = '#' + (PALETTE[n.node_type] || 0x585860).toString(16).padStart(6, '0');
    hoverInfo.style.display = 'block';
    hoverInfo.innerHTML = `
      <strong style="color:${{c}}">${{n.node_type}}</strong> ${{n.label}}<br>
      <span style="color:#777">
        W=${{n.weight.toFixed(2)}} E=${{n.energy.toFixed(2)}} S=${{n.stability.toFixed(2)}}
        self=${{n.self_relevance.toFixed(2)}} goal=${{n.goal_relevance.toFixed(2)}}
      </span>`;
  }} else {{
    hoverInfo.style.display = 'none';
  }}
}}

// ── Resize + Render ─────────────────────────────────────────
addEventListener('resize', () => {{
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
}});

function animate() {{
  requestAnimationFrame(animate);
  controls.update();
  updateHover();
  renderer.render(scene, camera);
}}
animate();
</script>
</body>
</html>"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html)
    print(f"Brain scan v3 → {output_path}")


if __name__ == "__main__":
    handle = sys.argv[1] if len(sys.argv) > 1 else "dragon_slayer"
    scan_path = Path(f"data/brain_scans/{handle}_scan.json")
    output_path = Path(f"data/brain_scans/{handle}_brain.html")
    render_html(scan_path, output_path)
