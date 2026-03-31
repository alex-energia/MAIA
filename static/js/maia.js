// ==============================
// 💥 MAIA CORE JS LIMPIO
// ==============================

window.__maia_running = false;

window.generarDrone = async function() {

    if (window.__maia_running) return;
    window.__maia_running = true;

    let idea = document.getElementById("idea")?.value;

    if (!idea || idea.length < 3) {
        alert("Escribe una idea");
        window.__maia_running = false;
        return;
    }

    let estado = document.getElementById("estado");
    if (estado) estado.innerText = "🧠 MAIA procesando...";

    let paso = 0;
    let data = {};
    let max_iter = 25;

    try {

        while (max_iter-- > 0) {

            let res = await fetch("/maia_step", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ idea, paso, data })
            });

            if (!res.ok) throw new Error("HTTP " + res.status);

            let response = await res.json();

            if (response.error) throw new Error(response.error);

            if (response.final) {

                if (estado) estado.innerText = "✅ Drone generado";

                let salida = document.getElementById("salida");
                if (salida) {
                    salida.innerText = JSON.stringify(response.resultado, null, 2);
                }

                let barra = document.getElementById("progreso");
                if (barra) barra.style.width = "100%";

                return;
            }

            paso = response.paso ?? (paso + 1);
            data = response.data ?? data;

            let barra = document.getElementById("progreso");
            if (barra) {
                barra.style.width = Math.min(95, paso * 15) + "%";
            }
        }

        throw new Error("Loop infinito detectado");

    } catch (e) {

        console.error(e);

        let errorBox = document.getElementById("error_box");
        if (errorBox) errorBox.innerText = "❌ " + e.message;

    } finally {
        window.__maia_running = false;
    }
};


// ==============================
// 🧹 LIMPIAR
// ==============================

window.limpiar = function() {
    ["idea","salida","estado"].forEach(id => {
        let el = document.getElementById(id);
        if (el) el.value ? el.value = "" : el.innerText = "";
    });

    let barra = document.getElementById("progreso");
    if (barra) barra.style.width = "0%";
};


// ==============================
// ⚡ PANEL
// ==============================

window.togglePanel = function() {
    let panel = document.getElementById("panel_maia");
    if (!panel) return;
    panel.style.display = panel.style.display === "block" ? "none" : "block";
};


// ==============================
// 📦 ZIP
// ==============================

window.descargarZIP = function() {
    window.open("/descargar_proyecto");
};


// ==============================
// 💾 GUARDAR
// ==============================

window.guardar = async function() {

    let categoria = document.getElementById("categoria")?.value;

    if (!categoria) {
        alert("Selecciona categoría");
        return;
    }

    try {
        await fetch("/guardar_proyecto", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                nombre: "Drone MAIA",
                tecnologia: categoria
            })
        });

        let estado = document.getElementById("estado_guardado");
        if (estado) estado.innerText = "✅ Guardado";

    } catch (e) {
        console.error(e);
    }
};


// ==============================
// 🔥 DEBUG GLOBAL
// ==============================

window.onerror = function(msg, url, line) {
    console.error("JS ERROR:", msg, "línea", line);
};

console.log("✅ MAIA JS limpio cargado");
