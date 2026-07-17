(() => {
  "use strict";

  const $ = (id) => document.getElementById(id);
  const arc = $("arc");
  const circumference = 2 * Math.PI * 100;
  let timer = null;
  let step = 0;
  let previousDelta = null;
  let previousTau = null;
  let upperHistory = [];
  let lowerHistory = [];

  arc.style.strokeDasharray = String(circumference);

  function fill(input) {
    const percent = (
      (Number(input.value) - Number(input.min)) /
      (Number(input.max) - Number(input.min))
    ) * 100;
    input.style.setProperty("--fill", `${percent}%`);
  }

  function stateForRatio(ratio) {
    if (ratio >= 1) {
      return { text: "境界到達 / 超過", className: "limit", color: "#ff745e" };
    }
    if (ratio >= 0.8) {
      return { text: "境界へ接近", className: "warn", color: "#f2b84b" };
    }
    return { text: "余白あり", className: "", color: "#0c7c68" };
  }

  function setState(state) {
    $("status").textContent = state.text;
    $("status").className = `status ${state.className}`.trim();
  }

  function updatePrimary() {
    const delta = Number($("delta").value);
    const tau = Number($("tau").value);
    const ratio = delta / tau;
    const state = stateForRatio(ratio);

    $("deltaOut").textContent = delta;
    $("tauOut").textContent = tau;
    $("ratio").textContent = ratio.toFixed(2);
    $("margin").textContent = (tau - delta).toFixed(0);
    $("primaryCalc").textContent = `${delta} ÷ ${tau} = ${ratio.toFixed(2)}`;
    $("marker").style.setProperty("--x", `${Math.min((ratio / 1.2) * 100, 100)}%`);
    $("primaryJudge").classList.toggle("active", ratio >= 0.8);
    arc.style.strokeDashoffset = String(circumference * (1 - Math.min(ratio, 1)));
    arc.style.stroke = state.color;
    setState(state);
    fill($("delta"));
    fill($("tau"));
  }

  function switchMode(secondary) {
    document.body.classList.toggle("secondary-mode", secondary);
    $("tabPrimary").setAttribute("aria-selected", String(!secondary));
    $("tabSecondary").setAttribute("aria-selected", String(secondary));
    if (secondary) {
      updateSecondary(false);
    } else {
      stopAnimation();
      updatePrimary();
    }
  }

  function pathFor(values, upper) {
    return values.map((value, index) => {
      const x = values.length === 1 ? 0 : (index / 35) * 600;
      const y = 102.5 + (upper ? -1 : 1) * Math.min(value / 120, 1) * 78;
      return `${index ? "L" : "M"} ${x.toFixed(1)} ${y.toFixed(1)}`;
    }).join(" ");
  }

  function updateWave() {
    const upperLine = pathFor(upperHistory, true);
    const lowerLine = pathFor(lowerHistory, false);
    const lastX = Math.max(0, ((upperHistory.length - 1) / 35) * 600);
    $("upperPath").setAttribute("d", upperLine);
    $("lowerPath").setAttribute("d", lowerLine);
    $("upperArea").setAttribute("d", upperLine ? `${upperLine} L ${lastX} 102.5 L 0 102.5 Z` : "");
    $("lowerArea").setAttribute("d", lowerLine ? `${lowerLine} L ${lastX} 102.5 L 0 102.5 Z` : "");
  }

  function signed(value) {
    return value > 0 ? `+${value.toFixed(0)}` : value.toFixed(0);
  }

  function updateSecondary(fromAnimation) {
    const upper = Number($("upper").value);
    const lower = Number($("lower").value);
    const width = Number($("width").value);
    const upperRatio = upper / width;
    const lowerRatio = lower / width;
    const maximumRatio = Math.max(upperRatio, lowerRatio);
    const dominant = upperRatio === lowerRatio ? "同率" : upperRatio > lowerRatio ? "upper" : "lower";

    $("upperOut").textContent = upper;
    $("lowerOut").textContent = lower;
    $("widthOut").textContent = width;
    $("upperRatio").textContent = upperRatio.toFixed(2);
    $("lowerRatio").textContent = lowerRatio.toFixed(2);
    $("upperBar").style.setProperty("--w", `${Math.min(upperRatio * 100, 100)}%`);
    $("lowerBar").style.setProperty("--w", `${Math.min(lowerRatio * 100, 100)}%`);
    $("upperCard").classList.toggle("dominant", dominant === "upper" || dominant === "同率");
    $("lowerCard").classList.toggle("dominant", dominant === "lower" || dominant === "同率");
    $("secondaryCalc").innerHTML =
      `max(${upperRatio.toFixed(2)}, ${lowerRatio.toFixed(2)}) = ${maximumRatio.toFixed(2)}<br>支配側 = ${dominant}`;
    $("tick").textContent = `STEP ${String(step).padStart(2, "0")}`;
    [$("upper"), $("lower"), $("width")].forEach(fill);

    if (!fromAnimation || !upperHistory.length) {
      upperHistory.push(upper);
      lowerHistory.push(lower);
      if (upperHistory.length > 36) upperHistory.shift();
      if (lowerHistory.length > 36) lowerHistory.shift();
    }
    updateWave();

    const currentDelta = Math.max(upper, lower);
    const deltaChange = previousDelta === null ? 0 : currentDelta - previousDelta;
    const tauChange = previousTau === null ? 0 : width - previousTau;
    const detected = deltaChange > 0 && tauChange < 0;

    $("detectIcon").classList.toggle("active", detected);
    $("detectTitle").textContent = detected ? "二重ゆらぎを検出" : "二重ゆらぎは未検出";
    $("detectFormula").textContent = `Δδ = ${signed(deltaChange)}　·　Δτ = ${signed(tauChange)}`;
    $("secondaryJudge").classList.toggle("active", detected);
    setState(detected
      ? { text: "二重ゆらぎ検出", className: "limit" }
      : stateForRatio(maximumRatio));
    previousDelta = currentDelta;
    previousTau = width;
  }

  function animationFrame() {
    step += 1;
    const phase = step * 0.34;
    const pressure = Math.min(step * 1.15, 45);
    $("upper").value = String(Math.round(36 + pressure + 10 * Math.sin(phase)));
    $("lower").value = String(Math.round(27 + pressure * 0.62 + 8 * Math.sin(phase * 0.78 + 1.4)));
    $("width").value = String(Math.max(42, Math.round(96 - step * 0.85 + 3 * Math.sin(phase * 0.55))));
    upperHistory.push(Number($("upper").value));
    lowerHistory.push(Number($("lower").value));
    if (upperHistory.length > 36) upperHistory.shift();
    if (lowerHistory.length > 36) lowerHistory.shift();
    updateSecondary(true);
    if (step >= 58) resetSecondary(false);
  }

  function toggleAnimation() {
    if (timer) {
      stopAnimation();
      return;
    }
    $("play").textContent = "Ⅱ　再生を停止";
    timer = window.setInterval(animationFrame, 420);
  }

  function stopAnimation() {
    if (timer) window.clearInterval(timer);
    timer = null;
    $("play").textContent = "▶　変化を再生";
  }

  function resetSecondary(shouldStop = true) {
    if (shouldStop) stopAnimation();
    step = 0;
    previousDelta = null;
    previousTau = null;
    upperHistory = [];
    lowerHistory = [];
    $("upper").value = "46";
    $("lower").value = "32";
    $("width").value = "84";
    updateSecondary(false);
  }

  $("tabPrimary").addEventListener("click", () => switchMode(false));
  $("tabSecondary").addEventListener("click", () => switchMode(true));
  [$("delta"), $("tau")].forEach((input) => input.addEventListener("input", updatePrimary));
  [$("upper"), $("lower"), $("width")].forEach(
    (input) => input.addEventListener("input", () => updateSecondary(false))
  );
  document.querySelectorAll(".preset").forEach((button) => {
    button.addEventListener("click", () => {
      $("delta").value = button.dataset.d;
      $("tau").value = button.dataset.t;
      updatePrimary();
    });
  });
  $("play").addEventListener("click", toggleAnimation);
  $("reset").addEventListener("click", () => resetSecondary(true));

  updatePrimary();
  resetSecondary(false);
  updatePrimary();
})();
