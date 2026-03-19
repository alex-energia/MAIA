// ==============================
// ESTADO GLOBAL
// ==============================
let vozActiva = false;
let reconocimiento = null;

// ==============================
// ESPERAR CARGA COMPLETA
// ==============================
window.addEventListener("load", () => {

    const vozBtn = document.getElementById("voz-btn");
    const chatToggle = document.getElementById("chat-toggle");
    const chatContainer = document.getElementById("chat-container");
    const chatClose = document.getElementById("chat-close");
    const sendBtn = document.getElementById("send-btn");
    const input = document.getElementById("mensaje-input");
    const mensajes = document.getElementById("chat-messages");
    const uploadBtn = document.getElementById("upload-toggle");
    const uploadInput = document.getElementById("upload-input");

    // 🔥 FORZAR CARGA DE VOCES
    let vocesDisponibles = [];

    function cargarVoces() {
        vocesDisponibles = speechSynthesis.getVoices();
    }

    speechSynthesis.onvoiceschanged = cargarVoces;

    // ==============================
    // VOZ FEMENINA REAL
    // ==============================
    function hablar(texto) {
        if (!vozActiva) return;

        const utter = new SpeechSynthesisUtterance(texto);
        utter.lang = "es-ES";

        let voz = vocesDisponibles.find(v =>
            v.lang.includes("es") &&
            (v.name.toLowerCase().includes("female") ||
             v.name.toLowerCase().includes("maria") ||
             v.name.toLowerCase().includes("paulina"))
        );

        if (!voz) voz = vocesDisponibles.find(v => v.lang.includes("es"));

        if (voz) utter.voice = voz;

        utter.rate = 1;
        utter.pitch = 1;

        speechSynthesis.cancel(); // 🔥 limpia voz anterior
        speechSynthesis.speak(utter);
    }

    // ==============================
    // MENSAJES
    // ==============================
    function agregarMensaje(texto, tipo) {
        let div = document.createElement("div");
        div.className = "message " + tipo;
        div.innerText = texto;
        mensajes.appendChild(div);
        mensajes.scrollTop = mensajes.scrollHeight;
    }

    // ==============================
    // CONECTAR CON BACKEND
    // ==============================
    function enviar(pregunta) {
        fetch("/maia_voz", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({pregunta})
        })
        .then(r => r.json())
        .then(data => {
            agregarMensaje(data.respuesta, "maia");
            hablar(data.respuesta); // 🔥 aquí habla
        })
        .catch(() => {
            agregarMensaje("Error conectando con MAIA", "maia");
        });
    }

    // ==============================
    // BOTÓN VOZ
    // ==============================
    vozBtn.onclick = () => {
        vozActiva = !vozActiva;

        vozBtn.style.background = vozActiva ? "green" : "red";
        vozBtn.innerText = vozActiva ? "Voz ON" : "Voz OFF";

        if (vozActiva) {
            if ('webkitSpeechRecognition' in window) {
                reconocimiento = new webkitSpeechRecognition();
                reconocimiento.lang = "es-ES";
                reconocimiento.continuous = true;

                reconocimiento.onresult = (e) => {
                    let texto = e.results[e.results.length - 1][0].transcript;
                    agregarMensaje(texto, "user");
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
    chatToggle.onclick = () => chatContainer.style.display = "flex";
    chatClose.onclick = () => chatContainer.style.display = "none";

    // ==============================
    // ENVIAR TEXTO
    // ==============================
    sendBtn.onclick = () => {
        let texto = input.value.trim();
        if (!texto) return;

        agregarMensaje(texto, "user");
        enviar(texto);
        input.value = "";
    };

    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") sendBtn.click();
    });

    // ==============================
    // SUBIR ARCHIVOS
    // ==============================
    uploadBtn.onclick = () => uploadInput.click();

    uploadInput.onchange = () => {
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
            agregarMensaje("Archivos subidos: " + data.archivos.join(", "), "maia");
        })
        .catch(() => {
            agregarMensaje("Error subiendo archivos", "maia");
        });
    };

});