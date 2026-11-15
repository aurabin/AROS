# Odyssey: modern web compatibility without changing its UI

**Status: feasibility and engineering proposal; no browser engine port is claimed.**

## Non-negotiable product requirement
Preserve Odyssey's existing visual design, layout, menus, navigation, shortcuts and user workflows. Changes to web rendering must be isolated behind an engine integration layer.

## First step: source and license audit
Locate the exact Odyssey source tree, revision, supported AROS targets and dependencies. Verify which WebKit branch it uses and whether existing platform abstractions can be reused. No Odyssey or WebKit source was identified by the initial repository code search; this must be resolved before implementation.

## Architectural options to benchmark
1. Update existing WebKit port incrementally where practical; map obsolete dependencies and missing AROS APIs.
2. Port a modern WebKit/WebKitGTK-derived engine with an AROS-specific platform layer (substantial OS integration work).
3. Evaluate a Chromium/CEF backend only if its process, threading, sandbox, graphics and runtime dependencies can be supported; CEF is not presumed to run on AROS.
4. For Windows-hosted Wizard use a separate optional host rendering backend; do not confuse host browser support with native AROS support.

## Compatibility targets
- Modern HTML/CSS, ECMAScript modules, WebAssembly and current DOM APIs.
- HTTPS/TLS, HTTP/2; HTTP/3 where supported by platform networking.
- HTML5 audio/video, codecs subject to licensing, and WebRTC where feasible.
- Security updates, certificate validation, site isolation where possible.
- GPU acceleration where drivers support it; safe software fallback.

## Phased validation
1. Baseline Odyssey screenshots and keyboard/mouse behavior to detect UI regressions.
2. Establish engine build toolchain and minimal page load on target AROS ABI.
3. Run web-platform-tests subsets and compatibility sites, record pass/fail and crash logs.
4. Add rendering, JavaScript, networking, media and performance tests.
5. Ship only verified improvements with explicit unsupported-feature list.

## Constraints
Chromium parity cannot be guaranteed simply by swapping engines. AROS kernel, threading, memory protection, process model, graphics, codec and toolchain support may require significant upstream work. Keep the Odyssey look unchanged throughout.
