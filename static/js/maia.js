// ==============================
// ESTADO GLOBAL
// ==============================
let vozActiva = false;
let reconocimiento = null;
let vocesDisponibles = [];

// ==============================
// 🔥 CARGAR VOCES CORRECTAMENTE
// ==============================
function cargarVoces() {
    vocesDisponibles = speechSynthesis.getVoices();
}
cargarVoces();
speechSynthesis.onvoiceschanged = cargarVoces;

// ==============================
// ESPERAR DOM
// ==============================
window.addEventListener("load", () => {

    // 🔥 IDs CORREGIDOS (CLAVE)
    const vozBtn = document.getElementById("maia-voz-btn");
    const chatToggle = document.getElementById("abrir-chat");
    const chatContainer = document.getElementById("maia-chat");
    const input = document.getElementById("chat-input");
    const mensajes = document.getElementById("chat-mensajes");
    const uploadInput = document.getElementById("subir-archivo");

    if (!vozBtn) {
        console.error("❌ MAIA no se cargó en esta página");
        return;
    }

    // ==============================
    // 🔊 HABLAR (VOZ REAL FUNCIONANDO)
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

        speechSynthesis.cancel();
        speechSynthesis.resume();

        setTimeout(() => {
            speechSynthesis.speak(utter);
        }, 100);
    }

    // ==============================
    function agregarMensaje(texto, tipo = "") {
        let div = document.createElement("div");
        div.innerText = texto;
        div.style.marginBottom = "5px";
        mensajes.appendChild(div);
        mensajes.scrollTop = mensajes.scrollHeight;
    }

    // ==============================
    function enviar(pregunta) {
        fetch("/maia_voz", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({pregunta})
        })
        .then(r => r.json())
        .then(data => {
            agregarMensaje("MAIA: " + data.respuesta);
            hablar(data.respuesta);
        })
        .catch(() => {
            agregarMensaje("Error conectando con MAIA");
        });
    }

    // ==============================
    // 🎤 BOTÓN VOZ (ARREGLADO)
    // ==============================
    vozBtn.onclick = () => {

        vozActiva = !vozActiva;

        vozBtn.style.background = vozActiva ? "green" : "red";
        vozBtn.innerText = vozActiva ? "MAIA ON" : "Activar MAIA";

        // 🔥 DESBLOQUEA AUDIO (CRÍTICO)
        speechSynthesis.resume();

        if (vozActiva) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

            if (SpeechRecognition) {
                reconocimiento = new SpeechRecognition();
                reconocimiento.lang = "es-ES";
                reconocimiento.continuous = true;

                reconocimiento.onresult = (e) => {
                    let texto = e.results[e.results.length - 1][0].transcript;
                    agregarMensaje("Tú: " + texto);
                    enviar(texto);
                };

                reconocimiento.start();
            }
        } else {
            if (reconocimiento) reconocimiento.stop();
        }
    };

    // ==============================
    // CHAT
    // ==============================
    chatToggle.onclick = () => {
        chatContainer.style.display =
            chatContainer.style.display === "none" ? "block" : "none";
    };

    // ==============================
    // ENVIAR TEXTO
    // ==============================
    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            let texto = input.value.trim();
            if (!texto) return;

            agregarMensaje("Tú: " + texto);
            enviar(texto);
            input.value = "";
        }
    });

    // ==============================
    // SUBIR ARCHIVOS
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
            agregarMensaje("MAIA: Archivos subidos: " + data.archivos.join(", "));
        })
        .catch(() => {
            agregarMensaje("Error subiendo archivos");
        });
    });

});