// ======================
// Variables y estado
// ======================
let vozActiva = false;

const vozBtn = document.getElementById('voz-btn');
const chatToggle = document.getElementById('chat-toggle');
const chatContainer = document.getElementById('chat-container');
const chatClose = document.getElementById('chat-close');
const chatMessages = document.getElementById('chat-messages');
const sendBtn = document.getElementById('send-btn');
const mensajeInput = document.getElementById('mensaje-input');
const uploadToggle = document.getElementById('upload-toggle');
const uploadInput = document.getElementById('upload-input');

// ======================
// Función para hablar
// ======================
function hablar(texto) {
    if (!vozActiva) return;
    const utter = new SpeechSynthesisUtterance(texto);
    utter.lang = 'es-ES';
    utter.voice = speechSynthesis.getVoices().find(v => v.lang === 'es-ES' && v.name.toLowerCase().includes('f')) || null;
    utter.pitch = 1;
    utter.rate = 1;
    speechSynthesis.speak(utter);
}

// ======================
// Botón Voz ON/OFF
// ======================
vozBtn.addEventListener('click', () => {
    vozActiva = !vozActiva;
    vozBtn.style.background = vozActiva ? 'green' : 'red';
    vozBtn.textContent = vozActiva ? 'Voz ON' : 'Voz OFF';

    if (vozActiva) {
        if ('webkitSpeechRecognition' in window) {
            const reconocimiento = new webkitSpeechRecognition();
            reconocimiento.lang = 'es-ES';
            reconocimiento.continuous = true;
            reconocimiento.interimResults = false;
            reconocimiento.onresult = function(event) {
                const ultimo = event.results[event.results.length - 1][0].transcript;
                agregarMensaje(ultimo, 'user');
                enviarPreguntaMAIA(ultimo);
            };
            reconocimiento.start();
            vozBtn.dataset.recognition = reconocimiento;
        }
    } else {
        const rec = vozBtn.dataset.recognition;
        if (rec) rec.stop();
    }
});

// ======================
// Chat Toggle
// ======================
chatToggle.addEventListener('click', () => chatContainer.style.display = 'flex');
chatClose.addEventListener('click', () => chatContainer.style.display = 'none');

// ======================
// Agregar mensaje al chat
// ======================
function agregarMensaje(texto, clase) {
    const div = document.createElement('div');
    div.className = `message ${clase}`;
    div.textContent = texto;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// ======================
// Enviar pregunta a MAIA
// ======================
function enviarPreguntaMAIA(pregunta) {
    fetch('/maia_voz', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pregunta })
    })
    .then(r => r.json())
    .then(data => {
        agregarMensaje(data.respuesta, 'maia');
        hablar(data.respuesta);
    })
    .catch(e => {
        agregarMensaje("Error al contactar a MAIA", 'maia');
    });
}

// ======================
// Botón Enviar
// ======================
sendBtn.addEventListener('click', () => {
    const texto = mensajeInput.value.trim();
    if (!texto) return;
    agregarMensaje(texto, 'user');
    enviarPreguntaMAIA(texto);
    mensajeInput.value = '';
});
mensajeInput.addEventListener('keydown', e => {
    if (e.key === 'Enter') sendBtn.click();
});

// ======================
// Subir archivos
// ======================
uploadToggle.addEventListener('click', () => uploadInput.click());
uploadInput.addEventListener('change', () => {
    const archivos = uploadInput.files;
    if (archivos.length === 0) return;
    const formData = new FormData();
    for (let i = 0; i < archivos.length; i++) formData.append('archivos', archivos[i]);

    fetch('/maia_subir_archivo', {
        method: 'POST',
        body: formData
    })
    .then(r => r.json())
    .then(data => {
        agregarMensaje(`Archivos subidos: ${data.archivos.join(', ')}`, 'maia');
    })
    .catch(e => {
        agregarMensaje('Error al subir archivos', 'maia');
    });
});