// ==============================
// ESTADO GLOBAL
// ==============================
let vozActiva = false;
let reconocimiento = null;

// ==============================
// ESPERAR CARGA COMPLETA
// ==============================
window.onload = () => {

    const vozBtn = document.getElementById("voz-btn");
    const chatToggle = document.getElementById("chat-toggle");
    const chatContainer = document.getElementById("chat-container");
    const chatClose = document.getElementById("chat-close");
    const sendBtn = document.getElementById("send-btn");
    const input = document.getElementById("mensaje-input");
    const mensajes = document.getElementById("chat-messages");
    const uploadBtn = document.getElementById("upload-toggle");
    const uploadInput = document.getElementById("upload-input");

    // ==============================
    // VOZ FEMENINA
    // ==============================
    function hablar(texto) {
        if (!vozActiva) return;

        const utter = new SpeechSynthesisUtterance(texto);
        utter.lang = "es-ES";

        let voces = speechSynthesis.getVoices();
        let voz = voces.find(v => v.lang.includes("es")) || voces[0];

        utter.voice = voz;
        utter.rate = 1;
        utter.pitch = 1;

        speechSynthesis.speak(utter);
    }

    // ==============================
    // AGREGAR MENSAJE
    // ==============================
    function agregarMensaje(texto, tipo) {
        let div = document.createElement("div");
        div.className = "message " + tipo;
        div.innerText = texto;
        mensajes.appendChild(div);
        mensajes.scrollTop = mensajes.scrollHeight;
    }

    // ==============================
    // ENVIAR A MAIA
    // ==============================
    function enviar(pregunta) {

        fetch("/maia_voz", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ pregunta })
        })
        .then(r => r.json())
        .then(data => {
            agregarMensaje(data.respuesta, "maia");
            hablar(data.respuesta);
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
    // ABRIR / CERRAR CHAT
    // ==============================
    chatToggle.onclick = () => {
        chatContainer.style.display = "flex";
    };

    chatClose.onclick = () => {
        chatContainer.style.display = "none";
    };

    // ==============================
    // BOTÓN ENVIAR
    // ==============================
    sendBtn.onclick = () => {
        let texto = input.value.trim();
        if (!texto) return;

        agregarMensaje(texto, "user");
        enviar(texto);
        input.value = "";
    };

    // ENTER
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

};