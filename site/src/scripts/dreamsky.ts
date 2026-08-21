/*
  The Dreamland sky, on the GPU.

  Why this exists: moving all four painted plates in the DOM cost 43% of frames
  over 20ms, because each one is a megapixel raster layer the compositor has to
  redraw every frame. hadaka.jp moves its entire scene at once because that
  scene is geometry on the GPU, where motion is nearly free. This is that, for
  our plates: every layer drifts, always, for about the price of one.

  What it is NOT allowed to do, from knowledge/craft/crawlers-and-parallax.md:
  "Googlebot does not support WebGL. Anything whose only representation is
  inside a canvas does not exist to search." So this canvas carries ONLY the
  decorative atmosphere. The mark, the headings and every word stay in the DOM
  above it. Nothing indexable is in here, and nothing in here has alt text to
  lose.

  It is also strictly an upgrade. The DOM planes are the baseline and stay in
  the markup; this hides them only once it has a working context and every
  texture decoded. No JS, no WebGL, a failed context, or prefers-reduced-motion
  all leave the original page exactly as it was.

  No three.js. Six textured quads do not need 150KB of scene graph, and
  case-study-01 is explicit that the bundle is part of the design.
*/

export interface LayerSpec {
  /** file stem in /images/dream */
  src: string;
  /** centre, in fractions of the canvas (0..1) */
  x: number;
  y: number;
  /** width, in fractions of canvas width */
  w: number;
  /** Framer-style scroll speed: 1 = page speed, lower = further away. */
  speed: number;
  /** px the layer moves across the pointer's full range. Nearer = more. */
  depth: number;
  /** seconds for one full drift traverse. 0 = still. */
  drift: number;
  /** px of drift travel, x and y */
  dx?: number;
  dy?: number;
  flip?: boolean;
}

const VERT = `
attribute vec2 a_unit;
uniform vec2 u_centre;   // px, canvas space
uniform vec2 u_size;     // px
uniform vec2 u_res;      // px
uniform float u_flip;
varying vec2 v_uv;
void main() {
  v_uv = vec2(u_flip > 0.0 ? 1.0 - a_unit.x : a_unit.x, 1.0 - a_unit.y);
  vec2 px = u_centre + (a_unit - 0.5) * u_size;
  vec2 clip = (px / u_res) * 2.0 - 1.0;
  gl_Position = vec4(clip.x, -clip.y, 0.0, 1.0);
}`;

// Straight texture sample. No tint, no fade, no exposure — the painted art is
// output exactly as authored. DESIGN_SYSTEM §6: art is never dimmed.
const FRAG = `
precision mediump float;
uniform sampler2D u_tex;
varying vec2 v_uv;
void main() {
  gl_FragColor = texture2D(u_tex, v_uv);
}`;

function compile(gl: WebGLRenderingContext, type: number, src: string) {
  const s = gl.createShader(type)!;
  gl.shaderSource(s, src);
  gl.compileShader(s);
  if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
    throw new Error(gl.getShaderInfoLog(s) || "shader");
  }
  return s;
}

/** Triangle wave in -1..1. Constant velocity, direction reverses, no seam —
 *  the profile measured off hadaka, and the only way to get constant speed out
 *  of art that does not tile. */
function tri(t: number) {
  const p = ((t % 1) + 1) % 1;
  return p < 0.5 ? p * 4 - 1 : 3 - p * 4;
}

export function mountDreamSky(
  canvas: HTMLCanvasElement,
  layers: LayerSpec[],
  base: string
): { destroy: () => void } | null {
  const gl = (canvas.getContext("webgl", {
    alpha: true,
    premultipliedAlpha: true,
    antialias: false,
    depth: false,
    powerPreference: "low-power",
  }) ||
    canvas.getContext("experimental-webgl")) as WebGLRenderingContext | null;
  if (!gl) return null;

  let prog: WebGLProgram;
  try {
    prog = gl.createProgram()!;
    gl.attachShader(prog, compile(gl, gl.VERTEX_SHADER, VERT));
    gl.attachShader(prog, compile(gl, gl.FRAGMENT_SHADER, FRAG));
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return null;
  } catch {
    return null;
  }
  gl.useProgram(prog);

  const quad = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, quad);
  gl.bufferData(
    gl.ARRAY_BUFFER,
    new Float32Array([0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1]),
    gl.STATIC_DRAW
  );
  const aUnit = gl.getAttribLocation(prog, "a_unit");
  gl.enableVertexAttribArray(aUnit);
  gl.vertexAttribPointer(aUnit, 2, gl.FLOAT, false, 0, 0);

  const u = {
    centre: gl.getUniformLocation(prog, "u_centre"),
    size: gl.getUniformLocation(prog, "u_size"),
    res: gl.getUniformLocation(prog, "u_res"),
    flip: gl.getUniformLocation(prog, "u_flip"),
  };

  gl.enable(gl.BLEND);
  // Premultiplied source: the correct blend for art whose own alpha is the
  // matte. Anything else fringes the feathered cloud edges.
  gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
  gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, true);
  gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false);

  type Loaded = LayerSpec & { tex: WebGLTexture; aspect: number };
  const loaded: Loaded[] = [];
  let destroyed = false;

  function upload(img: HTMLImageElement, spec: LayerSpec) {
    const tex = gl.createTexture()!;
    gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, img);
    // CLAMP + LINEAR, no mipmaps: these plates are not power-of-two and must
    // never wrap — a wrapped edge would put a hard seam on screen.
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    loaded.push({ ...spec, tex, aspect: img.naturalHeight / img.naturalWidth });
  }

  let px = 0,
    py = 0,
    tx = 0,
    ty = 0;
  let raf = 0;
  let visible = true;
  const t0 = performance.now();

  // Fill rate is the whole cost of this renderer: every frame rasterises the
  // full canvas, so doubling density quadruples the bill. At DPR 2 two
  // viewport-sized canvases are ~10 million pixels per frame. These are soft
  // painted clouds with no fine detail — they carry no information at 2x that
  // they do not carry at 1x — so the canvas renders at 1x and CSS scales it.
  // The mark and every glyph stay DOM and stay sharp at native density.
  const DPR = 1;

  function resize() {
    const dpr = DPR;
    const w = Math.round(canvas.clientWidth * dpr);
    const h = Math.round(canvas.clientHeight * dpr);
    if (canvas.width !== w || canvas.height !== h) {
      canvas.width = w;
      canvas.height = h;
      gl.viewport(0, 0, w, h);
    }
  }

  function draw(now: number) {
    if (destroyed) return;
    raf = requestAnimationFrame(draw);
    if (!visible) return;

    resize();
    const W = canvas.width,
      H = canvas.height;
    const dpr = DPR;
    const t = (now - t0) / 1000;

    // Damped follow, matching the DOM version's feel.
    px += (tx - px) * 0.11;
    py += (ty - py) * 0.11;

    const scrolled = window.scrollY;
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.uniform2f(u.res, W, H);

    for (const L of loaded) {
      const w = L.w * W;
      const h = w * L.aspect;
      const phase = L.drift > 0 ? tri(t / L.drift) : 0;
      const cx =
        L.x * W +
        px * L.depth * dpr +
        phase * (L.dx ?? 26) * dpr;
      const cy =
        L.y * H +
        py * L.depth * dpr +
        phase * (L.dy ?? 18) * dpr +
        // the reference's speed model: the page already carries this layer at
        // 100%, so add back the shortfall
        (1 - L.speed) * scrolled * dpr;

      gl.uniform2f(u.centre, cx, cy);
      gl.uniform2f(u.size, w, h);
      gl.uniform1f(u.flip, L.flip ? 1 : 0);
      gl.bindTexture(gl.TEXTURE_2D, L.tex);
      gl.drawArrays(gl.TRIANGLES, 0, 6);
    }
  }

  function onPointer(e: PointerEvent) {
    const r = canvas.getBoundingClientRect();
    tx = ((e.clientX - r.left) / r.width - 0.5) * 2;
    ty = ((e.clientY - r.top) / r.height - 0.5) * 2;
  }
  function onLeave() {
    tx = 0;
    ty = 0;
  }

  // Stop rendering the moment the hero is off screen or the tab is hidden.
  // An always-on GPU loop behind three screens of content is pure waste.
  const io = new IntersectionObserver(
    (es) => {
      visible = es[0].isIntersecting && !document.hidden;
    },
    { threshold: 0 }
  );
  io.observe(canvas);
  const onVis = () => {
    visible = !document.hidden;
  };

  const ready = Promise.all(
    layers.map(
      (spec) =>
        new Promise<void>((res) => {
          const img = new Image();
          img.decoding = "async";
          img.onload = () => {
            try {
              upload(img, spec);
            } catch {}
            res();
          };
          img.onerror = () => res();
          img.src = `${base}/images/dream/${spec.src}.webp`;
        })
    )
  ).then(() => {
    if (destroyed || loaded.length === 0) return false;
    // Keep the authored order, which is the z-order.
    loaded.sort(
      (a, b) => layers.findIndex((l) => l.src === a.src) - layers.findIndex((l) => l.src === b.src)
    );
    window.addEventListener("pointermove", onPointer, { passive: true });
    window.addEventListener("pointerleave", onLeave, { passive: true });
    document.addEventListener("visibilitychange", onVis);
    raf = requestAnimationFrame(draw);
    return true;
  });

  return {
    destroy() {
      destroyed = true;
      cancelAnimationFrame(raf);
      io.disconnect();
      window.removeEventListener("pointermove", onPointer);
      window.removeEventListener("pointerleave", onLeave);
      document.removeEventListener("visibilitychange", onVis);
    },
    // exposed for the caller to await before hiding the DOM fallback
    ready,
  } as any;
}
