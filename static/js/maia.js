// ==============================
// 💥 ANEXO CRÍTICO (FUNCIONES GLOBALES PARA BOTONES)
// ==============================
window.generarDrone = async function() {
    console.log("🚀 generarDrone ejecutado");

    if (window.__maia_running) {
        console.warn("⚠️ MAIA ya está corriendo");
        return;
    }
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
    let max_iter = 20; // 🔥 evita loops infinitos

    try {
        while (max_iter-- > 0) {

            let res = await fetch("/maia_step", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    idea: idea,
                    paso: paso,
                    data: data
                })
            });

            if (!res.ok) {
                throw new Error("HTTP " + res.status);
            }

            let response = await res.json();
            console.log("🧠 Paso:", response);

            if (response.error) {
                throw new Error(response.error);
            }

            if (response.final) {
                console.log("✅ FINAL:", response.resultado);

                if (estado) estado.innerText = "✅ Drone generado";

                let salida = document.getElementById("salida");
                if (salida) {
                    salida.innerText = JSON.stringify(response.resultado, null, 2);
                }

                window.__maia_running = false;
                return;
            }

            paso = response.paso ?? paso + 1;
            data = response.data ?? data;

            // 🔥 progreso visual estable
            let barra = document.getElementById("progreso");
            if (barra) {
                let progreso = Math.min(95, paso * 15);
                barra.style.width = progreso + "%";
            }
        }

        throw new Error("MAIA se quedó en loop");

    } catch (e) {
        console.error("❌ Error MAIA:", e);

        let errorBox = document.getElementById("error_box");
        if (errorBox) {
            errorBox.innerText = "❌ Error: " + e.message;
        }

    } finally {
        window.__maia_running = false;
    }
};

window.limpiar = function() {
    console.log("🧹 limpiar ejecutado");
    if (document.getElementById("idea")) document.getElementById("idea").value = "";
    if (document.getElementById("salida")) document.getElementById("salida").innerText = "";
    if (document.getElementById("estado")) document.getElementById("estado").innerText = "";
    if (document.getElementById("progreso")) document.getElementById("progreso").style.width = "0%";
};

window.togglePanel = function() {
    console.log("⚡ togglePanel ejecutado");
    let panel = document.getElementById("panel_maia");
    if (!panel) return;
    panel.style.display = panel.style.display === "block" ? "none" : "block";
};

window.descargarZIP = function() {
    window.open("/descargar_proyecto");
};

window.guardar = async function() {
    let categoria = document.getElementById("categoria")?.value;

    if (!categoria) {
        alert("Selecciona categoría");
        return;
    }

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
};

// ==============================
// 🔥 PROTECCIÓN GLOBAL
// ==============================
window.onerror = function(msg, url, line) {
    console.error("💥 JS ERROR:", msg, "en línea", line);
};

// ==============================
// 🔥 ESTADO GLOBAL REAL
// ==============================
let vozActiva = false;
let reconocimiento = null;
let vocesDisponibles = [];
let historialConversacion = [];

// ==============================
// 🔥 VOCES
// ==============================
function cargarVoces() {
    vocesDisponibles = speechSynthesis.getVoices();
}
cargarVoces();
speechSynthesis.onvoiceschanged = cargarVoces;

// ==============================
// 🔥 DOM READY
// ==============================
window.addEventListener("DOMContentLoaded", () => {

    const vozBtn = document.getElementById("maia-voz-btn");
    const chatToggle = document.getElementById("abrir-chat");
    const chatContainer = document.getElementById("maia-chat");
    const input = document.getElementById("chat-input");
    const mensajes = document.getElementById("chat-mensajes");
    const uploadInput = document.getElementById("subir-archivo");

    function existe(el) {
        return el !== null && el !== undefined;
    }

    function hablar(texto) {
        if (!vozActiva) return;

        const utter = new SpeechSynthesisUtterance(texto);
        utter.lang = "es-ES";

        let voz = vocesDisponibles.find(v => v.lang.includes("es"));
        if (voz) utter.voice = voz;

        speechSynthesis.cancel();
        speechSynthesis.resume();

        setTimeout(() => {
            speechSynthesis.speak(utter);
        }, 100);
    }

    function agregarMensaje(texto) {
        if (!existe(mensajes)) return;

        let div = document.createElement("div");
        div.innerText = texto;
        mensajes.appendChild(div);
        mensajes.scrollTop = mensajes.scrollHeight;

        historialConversacion.push(texto);
    }

    function enviar(pregunta) {
        fetch("/maia_voz", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                pregunta: pregunta,
                historial: historialConversacion
            })
        })
        .then(r => r.json())
        .then(data => {
            let respuesta = data.respuesta || "Sin respuesta";
            agregarMensaje("MAIA: " + respuesta);
            hablar(respuesta);
        })
        .catch(() => {
            agregarMensaje("MAIA: Error conexión");
        });
    }

    if (existe(vozBtn)) {
        vozBtn.onclick = () => {

            vozActiva = !vozActiva;
            vozBtn.style.background = vozActiva ? "green" : "red";
            vozBtn.innerText = vozActiva ? "MAIA ON" : "Activar MAIA";

            speechSynthesis.resume();

            if (vozActiva) {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

                if (!SpeechRecognition) {
                    alert("Tu navegador no soporta voz");
                    return;
                }

                reconocimiento = new SpeechRecognition();
                reconocimiento.lang = "es-ES";
                reconocimiento.continuous = true;

                reconocimiento.onresult = (e) => {
                    let texto = e.results[e.results.length - 1][0].transcript;
                    agregarMensaje("Tú: " + texto);
                    enviar(texto);
                };

                reconocimiento.start();

            } else {
                if (reconocimiento) reconocimiento.stop();
            }
        };
    }

    if (existe(chatToggle) && existe(chatContainer)) {
        chatToggle.onclick = () => {
            chatContainer.style.display =
                chatContainer.style.display === "none" ? "block" : "none";
        };
    }

    if (existe(input)) {
        input.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                let texto = input.value.trim();
                if (!texto) return;

                agregarMensaje("Tú: " + texto);
                enviar(texto);
                input.value = "";
            }
        });
    }

    if (existe(uploadInput)) {
        uploadInput.addEventListener("change", () => {

            let form = new FormData();

            for (let f of uploadInput.files) {
                form.append("archivos", f);
            }

            fetch("/maia_subir_archivo", {
                method: "POST",
                body: form
            })
            .then(() => {
                agregarMensaje("MAIA: Archivos recibidos");
            })
            .catch(() => {
                agregarMensaje("MAIA: Error subida");
            });
        });
    }

    console.log("✅ maia.js cargado SIN romper la app");
});