"""
Brain Scan 3D Renderer v2 — all 9 visual layers, static, interactive.

DOCS: docs/care/brain_scan/PATTERNS_Brain_Scan.md

Generates standalone HTML with Three.js. No auto-rotate (static by default).
All visual properties pre-computed by the extractor — renderer just displays.

Visual layers implemented:
  1. Node base: color (type), radius (weight), glow (energy), opacity (stability)
  2. Node affinity: inner halo (self_relevance), outer halo (partner_relevance),
     shape angularity (goal_relevance), wireframe (achievement), roughness (risk)
  3. Link base: color (relation), width (weight), opacity (trust), glow (energy)
  4. Link relational: wave (friction), dash (permanence), saturation (affinity),
     double-line (aversion), temperature (valence), jaggedness (1-stability)
  5-9: Partially — modality shapes, regions, provenance patina
"""

import json
import sys
from pathlib import Path


def render_html(scan_path: Path, output_path: Path):
    scan = json.loads(scan_path.read_text())
    nodes_json = json.dumps(scan["nodes"])
    links_json = json.dumps(scan["links"])
    regions_json = json.dumps(scan.get("regions", {}))
    citizen_id = scan["citizen_id"]
    stats = scan["stats"]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Brain Scan — @{citizen_id}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: #0a0a0a; color: #e0e0e0; font-family: 'SF Mono', 'Cascadia Code', monospace; overflow: hidden; }}
  #info {{
    position: absolute; top: 16px; left: 16px; z-index: 10;
    background: rgba(10,10,10,0.9); padding: 16px; border-radius: 8px;
    border: 1px solid #333; max-width: 280px; font-size: 11px; line-height: 1.5;
  }}
  #info h2 {{ font-size: 14px; margin-bottom: 8px; color: #fff; }}
  .stat {{ color: #888; margin: 2px 0; }}
  .legend {{ margin-top: 10px; }}
  .legend-item {{ display: flex; align-items: center; gap: 6px; margin: 2px 0; cursor: pointer; user-select: none; }}
  .legend-item.dimmed {{ opacity: 0.2; }}
  .legend-dot {{ width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }}
  #hover-info {{
    position: absolute; bottom: 16px; left: 16px; z-index: 10;
    background: rgba(10,10,10,0.92); padding: 12px; border-radius: 8px;
    border: 1px solid #444; font-size: 12px; display: none; max-width: 420px; line-height: 1.6;
  }}
  #controls {{
    position: absolute; top: 16px; right: 16px; z-index: 10;
    background: rgba(10,10,10,0.9); padding: 12px; border-radius: 8px;
    border: 1px solid #333; font-size: 11px;
  }}
  #controls label {{ display: block; margin: 3px 0; cursor: pointer; }}
  #controls hr {{ border-color: #333; margin: 6px 0; }}
  .bar {{ display: inline-block; height: 6px; border-radius: 3px; margin-right: 4px; }}
</style>
</head>
<body>

<div id="info">
  <h2>@{citizen_id}</h2>
  <div class="stat">{stats['total_nodes']} nodes — {stats['total_links']} links</div>
  <div class="stat">stem {stats['layers'].get('stem',0)} / limbic {stats['layers'].get('limbic',0)} / cortex {stats['layers'].get('cortex',0)}</div>
  <div class="legend" id="legend"></div>
</div>

<div id="controls">
  <strong>Layers</strong>
  <label><input type="checkbox" checked data-layer="stem"> Stem</label>
  <label><input type="checkbox" checked data-layer="limbic"> Limbic</label>
  <label><input type="checkbox" checked data-layer="cortex"> Cortex</label>
  <hr>
  <strong>Display</strong>
  <label><input type="checkbox" checked id="showLinks"> Links</label>
  <label><input type="checkbox" checked id="showHalos"> Halos (relevance)</label>
  <label><input type="checkbox" id="showWireframe"> Wireframe (achievement)</label>
  <hr>
  <strong>Regions</strong>
  <label><input type="checkbox" id="showSelf"> Self model</label>
  <label><input type="checkbox" id="showPartner"> Partner model</label>
  <label><input type="checkbox" id="showGoals"> Goal space</label>
</div>

<div id="hover-info"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script>
const nodes = {nodes_json};
const links = {links_json};
const regionData = {regions_json};

// ── Scene setup ─────────────────────────────────────────────
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x080810);
scene.fog = new THREE.FogExp2(0x080810, 0.25);

const camera = new THREE.PerspectiveCamera(55, innerWidth/innerHeight, 0.01, 100);
camera.position.set(0.8, 0.8, 1.8);
camera.lookAt(0, 0.4, 0);

const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
renderer.setSize(innerWidth, innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
document.body.appendChild(renderer.domElement);

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.autoRotate = false;  // STATIC by default
controls.target.set(0, 0.4, 0);

// Lights
const ambient = new THREE.AmbientLight(0x404060, 0.4);
scene.add(ambient);
const key = new THREE.PointLight(0xffeedd, 0.8, 8);
key.position.set(1, 2, 2);
scene.add(key);
const fill = new THREE.PointLight(0x4466aa, 0.3, 6);
fill.position.set(-1, 0.5, -1);
scene.add(fill);

// ── Legend ───────────────────────────────────────────────────
const typeColors = {{
  process: "#22c55e", desire: "#ef4444", narrative: "#a855f7",
  value: "#f59e0b", concept: "#3b82f6", memory: "#6b7280"
}};
const legend = document.getElementById('legend');
const activeTypes = new Set(Object.keys(typeColors));
for (const [type, color] of Object.entries(typeColors)) {{
  const item = document.createElement('div');
  item.className = 'legend-item';
  item.innerHTML = `<span class="legend-dot" style="background:${{color}}"></span>${{type}}`;
  item.onclick = () => {{
    if (activeTypes.has(type)) {{ activeTypes.delete(type); item.classList.add('dimmed'); }}
    else {{ activeTypes.add(type); item.classList.remove('dimmed'); }}
    updateVisibility();
  }};
  legend.appendChild(item);
}}

// ── Node meshes ─────────────────────────────────────────────
const nodeGroup = new THREE.Group();
const haloGroup = new THREE.Group();
const nodeMeshes = [];
const nodeById = {{}};

nodes.forEach(n => {{
  // Base geometry (sphere for now — modality shapes in Phase 2)
  const geo = new THREE.SphereGeometry(n.radius * 0.003, 14, 14);

  // Color with patina (old nodes get brownish tint)
  const baseColor = new THREE.Color(n.color);
  const patinaColor = new THREE.Color(0x8b7355);
  const finalColor = baseColor.clone().lerp(patinaColor, n.patina * 0.4);

  const mat = new THREE.MeshPhongMaterial({{
    color: finalColor,
    emissive: n.glow > 0 ? baseColor.clone().multiplyScalar(n.glow * 0.5) : new THREE.Color(0),
    transparent: true,
    opacity: n.opacity,
    shininess: n.sharpness * 80,  // recency → shininess (sharp = shiny)
  }});

  // Roughness via flatShading for high risk_affinity
  if (n.roughness > 0.3) {{
    mat.flatShading = true;
  }}

  const mesh = new THREE.Mesh(geo, mat);
  mesh.position.set(n.x, n.z, n.y);
  mesh.userData = n;
  nodeGroup.add(mesh);
  nodeMeshes.push(mesh);
  nodeById[n.id] = mesh;

  // Inner halo (self_relevance → amber ring)
  if (n.inner_halo > 0.2) {{
    const haloGeo = new THREE.RingGeometry(n.radius * 0.004, n.radius * 0.006, 24);
    const haloMat = new THREE.MeshBasicMaterial({{
      color: 0xf59e0b, transparent: true, opacity: n.inner_halo * 0.5, side: THREE.DoubleSide
    }});
    const halo = new THREE.Mesh(haloGeo, haloMat);
    halo.position.copy(mesh.position);
    halo.lookAt(camera.position);
    halo.userData = {{ type: 'inner_halo' }};
    haloGroup.add(halo);
  }}

  // Outer halo (partner_relevance → cyan ring)
  if (n.outer_halo > 0.2) {{
    const haloGeo = new THREE.RingGeometry(n.radius * 0.006, n.radius * 0.008, 24);
    const haloMat = new THREE.MeshBasicMaterial({{
      color: 0x06b6d4, transparent: true, opacity: n.outer_halo * 0.4, side: THREE.DoubleSide
    }});
    const halo = new THREE.Mesh(haloGeo, haloMat);
    halo.position.copy(mesh.position);
    halo.lookAt(camera.position);
    halo.userData = {{ type: 'outer_halo' }};
    haloGroup.add(halo);
  }}

  // Wireframe overlay (achievement_affinity)
  if (n.wireframe > 0.3) {{
    const wfGeo = new THREE.WireframeGeometry(geo);
    const wfMat = new THREE.LineBasicMaterial({{ color: finalColor, transparent: true, opacity: n.wireframe * 0.6 }});
    const wf = new THREE.LineSegments(wfGeo, wfMat);
    wf.position.copy(mesh.position);
    wf.scale.setScalar(1.15);
    wf.userData = {{ type: 'wireframe' }};
    haloGroup.add(wf);
  }}

  // Ring count (activation_count → torus rings)
  for (let r = 0; r < n.ring_count; r++) {{
    const ringGeo = new THREE.TorusGeometry(n.radius * 0.003 * (1.3 + r * 0.3), 0.0005, 6, 24);
    const ringMat = new THREE.MeshBasicMaterial({{ color: finalColor, transparent: true, opacity: 0.2 }});
    const ring = new THREE.Mesh(ringGeo, ringMat);
    ring.position.copy(mesh.position);
    ring.rotation.x = Math.PI / 2 + r * 0.3;
    haloGroup.add(ring);
  }}
}});

scene.add(nodeGroup);
scene.add(haloGroup);

// ── Link lines ──────────────────────────────────────────────
const linkGroup = new THREE.Group();

links.forEach(l => {{
  const src = nodeById[l.source];
  const tgt = nodeById[l.target];
  if (!src || !tgt) return;

  const srcPos = src.position;
  const tgtPos = tgt.position;

  let points;
  if (l.wave > 0.5) {{
    // Curved link (friction → bezier)
    const mid = new THREE.Vector3().addVectors(srcPos, tgtPos).multiplyScalar(0.5);
    const offset = new THREE.Vector3(
      (Math.random() - 0.5) * l.wave * 0.02,
      (Math.random() - 0.5) * l.wave * 0.02,
      (Math.random() - 0.5) * l.wave * 0.02
    );
    mid.add(offset);
    const curve = new THREE.QuadraticBezierCurve3(srcPos, mid, tgtPos);
    points = curve.getPoints(12);
  }} else {{
    points = [srcPos, tgtPos];
  }}

  // Jaggedness (1-stability → noise on vertices)
  if (l.jaggedness > 0.5 && points.length > 2) {{
    for (let i = 1; i < points.length - 1; i++) {{
      points[i].x += (Math.random() - 0.5) * l.jaggedness * 0.005;
      points[i].y += (Math.random() - 0.5) * l.jaggedness * 0.005;
      points[i].z += (Math.random() - 0.5) * l.jaggedness * 0.005;
    }}
  }}

  const geo = new THREE.BufferGeometry().setFromPoints(points);

  // Color with valence temperature shift and affinity saturation
  let linkColor = new THREE.Color(l.color);
  if (l.temp_shift !== 0) {{
    const hsl = {{}};
    linkColor.getHSL(hsl);
    hsl.h += l.temp_shift / 360;
    linkColor.setHSL(hsl.h, hsl.s * l.saturation, hsl.l);
  }} else {{
    const hsl = {{}};
    linkColor.getHSL(hsl);
    linkColor.setHSL(hsl.h, hsl.s * l.saturation, hsl.l);
  }}

  let mat;
  if (l.dash_gap > 2) {{
    mat = new THREE.LineDashedMaterial({{
      color: linkColor, transparent: true, opacity: l.opacity * 0.6,
      dashSize: 0.01, gapSize: l.dash_gap * 0.001,
    }});
  }} else {{
    mat = new THREE.LineBasicMaterial({{
      color: linkColor, transparent: true, opacity: l.opacity * 0.6,
    }});
  }}

  const line = new THREE.Line(geo, mat);
  if (l.dash_gap > 2) line.computeLineDistances();
  line.userData = l;
  linkGroup.add(line);

  // Double line for aversion
  if (l.has_aversion) {{
    const offsetDir = new THREE.Vector3().subVectors(tgtPos, srcPos).cross(new THREE.Vector3(0,1,0)).normalize().multiplyScalar(0.008);
    const points2 = points.map(p => p.clone().add(offsetDir));
    const geo2 = new THREE.BufferGeometry().setFromPoints(points2);
    const mat2 = new THREE.LineBasicMaterial({{ color: 0xef4444, transparent: true, opacity: 0.3 }});
    const line2 = new THREE.Line(geo2, mat2);
    linkGroup.add(line2);
  }}
}});

scene.add(linkGroup);

// ── Region membranes ────────────────────────────────────────
const regionMeshes = {{}};

function createRegionMembrane(nodeIds, color, opacity, name) {{
  if (!nodeIds || nodeIds.length < 3) return null;
  // Compute bounding sphere of region nodes
  const positions = nodeIds.map(id => nodeById[id]?.position).filter(Boolean);
  if (positions.length < 3) return null;

  const center = new THREE.Vector3();
  positions.forEach(p => center.add(p));
  center.divideScalar(positions.length);

  let maxDist = 0;
  positions.forEach(p => {{ maxDist = Math.max(maxDist, center.distanceTo(p)); }});

  const geo = new THREE.SphereGeometry(maxDist * 1.3, 16, 16);
  const mat = new THREE.MeshBasicMaterial({{
    color: new THREE.Color(color), transparent: true, opacity: opacity,
    wireframe: false, side: THREE.BackSide, depthWrite: false,
  }});
  const mesh = new THREE.Mesh(geo, mat);
  mesh.position.copy(center);
  mesh.visible = false;
  scene.add(mesh);
  return mesh;
}}

// Build region node ID lists
const selfIds = nodes.filter(n => n.self_relevance > 0.5).map(n => n.id);
const partnerIds = nodes.filter(n => n.partner_relevance > 0.5).map(n => n.id);
const goalIds = nodes.filter(n => n.goal_relevance > 0.5).map(n => n.id);

regionMeshes.self = createRegionMembrane(selfIds, '#f59e0b', 0.06, 'self');
regionMeshes.partner = createRegionMembrane(partnerIds, '#06b6d4', 0.06, 'partner');
regionMeshes.goals = createRegionMembrane(goalIds, '#22c55e', 0.05, 'goals');

// ── Controls ────────────────────────────────────────────────
function updateVisibility() {{
  nodeMeshes.forEach(m => {{
    const n = m.userData;
    m.visible = activeTypes.has(n.node_type) &&
      document.querySelector(`[data-layer="${{n.layer}}"]`)?.checked !== false;
  }});
}}

document.querySelectorAll('[data-layer]').forEach(cb => {{
  cb.addEventListener('change', updateVisibility);
}});

document.getElementById('showLinks').addEventListener('change', e => {{
  linkGroup.visible = e.target.checked;
}});

document.getElementById('showHalos').addEventListener('change', e => {{
  haloGroup.children.forEach(h => {{
    if (h.userData?.type === 'inner_halo' || h.userData?.type === 'outer_halo')
      h.visible = e.target.checked;
  }});
}});

document.getElementById('showWireframe').addEventListener('change', e => {{
  haloGroup.children.forEach(h => {{
    if (h.userData?.type === 'wireframe') h.visible = e.target.checked;
  }});
}});

document.getElementById('showSelf').addEventListener('change', e => {{
  if (regionMeshes.self) regionMeshes.self.visible = e.target.checked;
}});
document.getElementById('showPartner').addEventListener('change', e => {{
  if (regionMeshes.partner) regionMeshes.partner.visible = e.target.checked;
}});
document.getElementById('showGoals').addEventListener('change', e => {{
  if (regionMeshes.goals) regionMeshes.goals.visible = e.target.checked;
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
    hoverInfo.style.display = 'block';
    hoverInfo.innerHTML = `
      <strong style="color:${{n.color}}">${{n.node_type}}</strong> — ${{n.label}}<br>
      <span style="color:#999">
        W=${{n.weight.toFixed(2)}} E=${{n.energy.toFixed(2)}} S=${{n.stability.toFixed(2)}} R=${{n.recency.toFixed(2)}}<br>
        self=${{n.self_relevance.toFixed(2)}} partner=${{n.partner_relevance.toFixed(2)}} goal=${{n.goal_relevance.toFixed(2)}}<br>
        novelty=${{n.novelty_affinity.toFixed(2)}} care=${{n.care_affinity.toFixed(2)}} achieve=${{n.achievement_affinity.toFixed(2)}} risk=${{n.risk_affinity.toFixed(2)}}<br>
        activations=${{n.activation_count}} age=${{n.age_days.toFixed(0)}}d patina=${{n.patina.toFixed(2)}}
      </span>`;
  }} else {{
    hoverInfo.style.display = 'none';
  }}
}}

// ── Resize ──────────────────────────────────────────────────
addEventListener('resize', () => {{
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
}});

// ── Render loop ─────────────────────────────────────────────
function animate() {{
  requestAnimationFrame(animate);
  controls.update();
  updateHover();
  // Face halos toward camera
  haloGroup.children.forEach(h => {{
    if (h.userData?.type === 'inner_halo' || h.userData?.type === 'outer_halo')
      h.lookAt(camera.position);
  }});
  renderer.render(scene, camera);
}}
animate();
</script>
</body>
</html>"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html)
    print(f"Brain scan v2 → {output_path}")


if __name__ == "__main__":
    handle = sys.argv[1] if len(sys.argv) > 1 else "dragon_slayer"
    scan_path = Path(f"data/brain_scans/{handle}_scan.json")
    output_path = Path(f"data/brain_scans/{handle}_brain.html")
    render_html(scan_path, output_path)
