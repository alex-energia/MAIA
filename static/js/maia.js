// ==============================
// 🔥 ESTADO GLOBAL REAL
// ==============================
let vozActiva = false;
let reconocimiento = null;
let vocesDisponibles = [];
let historialConversacion = [];

// ==============================
// 🔥 CARGAR VOCES (CRÍTICO)
// ==============================
function cargarVoces() {
    vocesDisponibles = speechSynthesis.getVoices();
}
cargarVoces();
speechSynthesis.onvoiceschanged = cargarVoces;

// ==============================
// 🔥 ESPERAR DOM COMPLETO
// ==============================
window.addEventListener("DOMContentLoaded", () => {

    const vozBtn = document.getElementById("maia-voz-btn");
    const chatToggle = document.getElementById("abrir-chat");
    const chatContainer = document.getElementById("maia-chat");
    const input = document.getElementById("chat-input");
    const mensajes = document.getElementById("chat-mensajes");
    const uploadInput = document.getElementById("subir-archivo");

    // 🔥 SI NO EXISTE MAIA, NO ROMPER LA APP
    if (!vozBtn || !chatToggle || !chatContainer) {
        console.warn("⚠️ MAIA no está cargado en esta página");
        return;
    }

    // ==============================
    // 🔊 VOZ FEMENINA REAL (100% FUNCIONAL)
    // ==============================
    function hablar(texto) {
        if (!vozActiva) return;

        const utter = new SpeechSynthesisUtterance(texto);
        utter.lang = "es-ES";

        let voz = vocesDisponibles.find(v =>
            v.lang.includes("es") &&
            (
                v.name.toLowerCase().includes("female") ||
                v.name.toLowerCase().includes("maria") ||
                v.name.toLowerCase().includes("paulina") ||
                v.name.toLowerCase().includes("google")
            )
        );

        if (!voz) voz = vocesDisponibles.find(v => v.lang.includes("es"));

        if (voz) utter.voice = voz;

        utter.rate = 1;
        utter.pitch = 1;

        // 🔥 CLAVE: limpiar y reactivar audio
        speechSynthesis.cancel();
        speechSynthesis.resume();

        setTimeout(() => {
            speechSynthesis.speak(utter);
        }, 100);
    }

    // ==============================
    // 💬 MENSAJES + MEMORIA
    // ==============================
    function agregarMensaje(texto, tipo = "maia") {
        let div = document.createElement("div");
        div.innerText = texto;
        div.style.marginBottom = "5px";

        mensajes.appendChild(div);
        mensajes.scrollTop = mensajes.scrollHeight;

        // 🔥 GUARDAR EN MEMORIA
        historialConversacion.push(texto);
    }

    // ==============================
    // 🔗 BACKEND + MEMORIA
    // ==============================
    function enviar(pregunta) {

        historialConversacion.push("Usuario: " + pregunta);

        fetch("/maia_voz", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                pregunta: pregunta,
                historial: historialConversacion   // 🔥 memoria enviada
            })
        })
        .then(r => r.json())
        .then(data => {

            let respuesta = data.respuesta;

            agregarMensaje("MAIA: " + respuesta);
            hablar(respuesta);

        })
        .catch(() => {
            agregarMensaje("MAIA: Error de conexión");
        });
    }

    // ==============================
    // 🎤 BOTÓN VOZ (100% ARREGLADO)
    // ==============================
    vozBtn.onclick = () => {

        vozActiva = !vozActiva;

        vozBtn.style.background = vozActiva ? "green" : "red";
        vozBtn.innerText = vozActiva ? "MAIA ON" : "Activar MAIA";

        // 🔥 DESBLOQUEA AUDIO EN NAVEGADOR
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

                agregarMensaje("Tú: " + texto, "user");
                enviar(texto);
            };

            reconocimiento.start();

        } else {
            if (reconocimiento) reconocimiento.stop();
        }
    };

    // ==============================
    // 💬 CHAT (+)
    // ==============================
    chatToggle.onclick = () => {
        chatContainer.style.display =
            chatContainer.style.display === "none" ? "block" : "none";
    };

    // ==============================
    // ⌨️ INPUT TEXTO
    // ==============================
    input.addEventListener("keydown", (e) => {

        if (e.key === "Enter") {

            let texto = input.value.trim();
            if (!texto) return;

            agregarMensaje("Tú: " + texto, "user");
            enviar(texto);

            input.value = "";
        }
    });

    // ==============================
    // 📎 SUBIR ARCHIVOS
    // ==============================
    uploadInput.addEventListener("change", () => {

        let form = new FormData();

        for (let f of uploadInput.files) {
            form.append("archivos", f);
        }

        fetch("/maia_subir_archivo", {
            method: "POST",
            body: form
        })
        .then(r => r.json())
        .then(data => {
            agregarMensaje("MAIA: Archivos recibidos: " + data.archivos.join(", "));
        })
        .catch(() => {
            agregarMensaje("MAIA: Error subiendo archivos");
        });
    });

});