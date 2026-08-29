const API_URL = "http://127.0.0.1:8000";

let lastAnswer = "";
let mediaRecorder = null;
let audioChunks = [];
let isRecording = false;

let recentQuestions = [];


/* =========================
   LOAD HISTORY
========================= */

try {

    const savedHistory =
        localStorage.getItem("campusVoiceHistory");

    if (savedHistory) {
        recentQuestions = JSON.parse(savedHistory);
    }

} catch (error) {

    recentQuestions = [];

}


/* =========================
   ENTER KEY
========================= */

function handleEnter(event) {

    if (event.key === "Enter") {
        askQuestion();
    }

}


/* =========================
   QUICK SEARCH
========================= */

function quickSearch(query) {

    document.getElementById("queryInput").value = query;

    askQuestion();

}


/* =========================
   ASK CAMPUS QUESTION
========================= */

async function askQuestion() {

    const input =
        document.getElementById("queryInput");

    const query =
        input.value.trim();


    if (!query) {
        return;
    }


    /* Add to recent history */

    addToHistory(query);


    showLoading(true);


    try {

        const response =
            await fetch(
                `${API_URL}/query`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        query: query
                    })
                }
            );


        if (!response.ok) {
            throw new Error(
                "Backend request failed"
            );
        }


        const data =
            await response.json();


        displayResult(
            query,
            data.answer
        );


    } catch (error) {

        console.error(error);

        displayError(
            "Unable to connect to Campus VoiceOS backend."
        );


    } finally {

        showLoading(false);

    }

}


/* =========================
   DISPLAY RESULT
========================= */

function displayResult(query, answer) {

    const result =
        document.getElementById("result");


    const transcript =
        document.getElementById("transcript");


    const answers =
        document.getElementById("answers");


    result.style.display = "block";


    transcript.innerHTML = `
        <strong>You asked:</strong>
        ${escapeHtml(query)}
    `;


    answers.innerHTML = "";


    /* STRING RESPONSE */

    if (typeof answer === "string") {

        answers.innerHTML = `
            <div class="answer-item">

                <div class="answer-text">
                    ${escapeHtml(answer)}
                </div>

            </div>
        `;


        lastAnswer = answer;

        return;

    }


    /* ARRAY RESPONSE */

    if (
        Array.isArray(answer)
        &&
        answer.length > 0
    ) {

        answer.forEach(item => {

            const div =
                document.createElement("div");


            div.className =
                "answer-item";


            div.innerHTML = `

                <div class="answer-category">

                    ${escapeHtml(
                        item.category ||
                        "Campus Information"
                    )}

                </div>


                <div class="answer-text">

                    ${escapeHtml(
                        item.answer ||
                        "Information available."
                    )}

                </div>


                ${
                    item.location
                    ?
                    `
                    <span class="location">

                        📍 ${escapeHtml(
                            item.location
                        )}

                    </span>
                    `
                    :
                    ""
                }

            `;


            answers.appendChild(div);

        });


        lastAnswer =
            answer
                .map(
                    item =>
                        item.answer || ""
                )
                .join(". ");

    }


    /* NO RESULT */

    else {

        answers.innerHTML = `

            <div class="answer-item">

                No relevant information found.

            </div>

        `;


        lastAnswer =
            "No relevant information found.";

    }

}


/* =========================
   MICROPHONE
========================= */

async function startRecording() {

    if (isRecording) {

        stopRecording();

        return;

    }


    try {

        const stream =
            await navigator
                .mediaDevices
                .getUserMedia({
                    audio: true
                });


        mediaRecorder =
            new MediaRecorder(stream);


        audioChunks = [];


        mediaRecorder.ondataavailable =
            event => {

                if (event.data.size > 0) {

                    audioChunks.push(
                        event.data
                    );

                }

            };


        mediaRecorder.onstop =
            async () => {

                stream
                    .getTracks()
                    .forEach(
                        track =>
                            track.stop()
                    );


                const audioBlob =
                    new Blob(
                        audioChunks,
                        {
                            type:
                                mediaRecorder.mimeType
                        }
                    );


                await sendAudio(
                    audioBlob
                );

            };


        mediaRecorder.start();


        isRecording = true;


        const button =
            document.getElementById(
                "micButton"
            );


        button.classList.add(
            "recording"
        );


        button.innerHTML =
            "⏹️";


        document.getElementById(
            "status"
        ).innerText =
            "Listening... Tap again to stop";


    } catch (error) {

        console.error(error);


        alert(
            "Microphone permission is required."
        );

    }

}


/* =========================
   STOP RECORDING
========================= */

function stopRecording() {

    if (!mediaRecorder) {
        return;
    }


    mediaRecorder.stop();


    isRecording = false;


    const button =
        document.getElementById(
            "micButton"
        );


    button.classList.remove(
        "recording"
    );


    button.innerHTML =
        "🎙️";


    document.getElementById(
        "status"
    ).innerText =
        "Transcribing your voice...";

}


/* =========================
   SEND AUDIO
========================= */

async function sendAudio(audioBlob) {

    showLoading(true);


    try {

        const formData =
            new FormData();


        formData.append(
            "file",
            audioBlob,
            "campus_voice.webm"
        );


        const response =
            await fetch(
                `${API_URL}/transcribe`,
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Transcription failed"
            );

        }


        const text =
            data.text || "";


        document.getElementById(
            "queryInput"
        ).value = text;


        document.getElementById(
            "status"
        ).innerText =
            "Voice converted to text";


        if (text.trim()) {

            await askQuestion();

        }


    } catch (error) {

        console.error(error);

        displayError(
            error.message
        );


    } finally {

        showLoading(false);

    }

}


/* =========================
   SPEAK ANSWER
========================= */

function speakAnswer() {

    if (!lastAnswer) {
        return;
    }


    window.speechSynthesis.cancel();


    const speech =
        new SpeechSynthesisUtterance(
            lastAnswer
        );


    speech.rate = 0.95;

    speech.pitch = 1;


    window.speechSynthesis.speak(
        speech
    );

}


/* =========================
   CLEAR RESULT
========================= */

function clearResult() {

    document.getElementById(
        "result"
    ).style.display = "none";


    document.getElementById(
        "queryInput"
    ).value = "";


    document.getElementById(
        "answers"
    ).innerHTML = "";


    document.getElementById(
        "transcript"
    ).innerHTML = "";


    lastAnswer = "";

}


/* =========================
   ADD TO HISTORY
========================= */

function addToHistory(question) {

    question =
        question.trim();


    if (!question) {
        return;
    }


    /* Remove duplicate */

    recentQuestions =
        recentQuestions.filter(
            item =>
                item.toLowerCase()
                !== question.toLowerCase()
        );


    /* Add newest question first */

    recentQuestions.unshift(
        question
    );


    /* Keep only latest 5 */

    if (recentQuestions.length > 5) {

        recentQuestions =
            recentQuestions.slice(0, 5);

    }


    /* Save in browser */

    localStorage.setItem(
        "campusVoiceHistory",
        JSON.stringify(
            recentQuestions
        )
    );


    renderHistory();

}


/* =========================
   RENDER HISTORY
========================= */

function renderHistory() {

    const historyList =
        document.getElementById(
            "historyList"
        );


    if (!historyList) {
        return;
    }


    historyList.innerHTML = "";


    if (recentQuestions.length === 0) {

        historyList.innerHTML = `

            <div class="history-empty">

                Your recent questions
                will appear here.

            </div>

        `;

        return;

    }


    recentQuestions.forEach(
        question => {

            const button =
                document.createElement(
                    "button"
                );


            button.className =
                "history-item";


            button.innerHTML = `
                🔎
                <span>
                    ${escapeHtml(question)}
                </span>
            `;


            button.onclick = () => {

                document.getElementById(
                    "queryInput"
                ).value = question;


                askQuestion();

            };


            historyList.appendChild(
                button
            );

        }
    );

}


/* =========================
   CREATE HISTORY UI
========================= */

function createHistoryUI() {

    const mainCard =
        document.querySelector(
            ".main-card"
        );


    if (!mainCard) {
        return;
    }


    /* Prevent duplicate */

    if (
        document.getElementById(
            "historySection"
        )
    ) {
        return;
    }


    const historySection =
        document.createElement(
            "div"
        );


    historySection.id =
        "historySection";


    historySection.innerHTML = `

        <div class="history-header">

            <strong>
                🕘 Recent Questions
            </strong>

            <button
                class="clear-history"
                onclick="clearHistory()"
            >
                Clear History
            </button>

        </div>


        <div id="historyList">
        </div>

    `;


    mainCard.appendChild(
        historySection
    );


    renderHistory();

}


/* =========================
   CLEAR HISTORY
========================= */

function clearHistory() {

    recentQuestions = [];


    localStorage.removeItem(
        "campusVoiceHistory"
    );


    renderHistory();

}


/* =========================
   LOADING
========================= */

function showLoading(show) {

    const loading =
        document.getElementById(
            "loading"
        );


    loading.style.display =
        show
        ? "block"
        : "none";

}


/* =========================
   ERROR
========================= */

function displayError(message) {

    const result =
        document.getElementById(
            "result"
        );


    result.style.display =
        "block";


    document.getElementById(
        "answers"
    ).innerHTML = `

        <div class="answer-item">

            ❌ ${escapeHtml(message)}

        </div>

    `;

}


/* =========================
   HTML SECURITY
========================= */

function escapeHtml(text) {

    const div =
        document.createElement(
            "div"
        );


    div.textContent =
        String(text);


    return div.innerHTML;

}


/* =========================
   INITIALIZE
========================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        createHistoryUI();

    }
);