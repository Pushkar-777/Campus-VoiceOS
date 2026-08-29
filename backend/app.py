from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import assemblyai as aai
import os
import json
import tempfile
import re


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

API_KEY = os.getenv("ASSEMBLYAI_API_KEY")


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Campus VoiceOS",
    description="AI-powered campus voice assistant",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# PATHS
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_FILE = os.path.join(
    BASE_DIR,
    "frontend",
    "data",
    "campus_data.json"
)


# =========================================================
# ASSEMBLYAI
# =========================================================

if API_KEY:
    aai.settings.api_key = API_KEY


# =========================================================
# REQUEST MODEL
# =========================================================

class QueryRequest(BaseModel):
    query: str


# =========================================================
# LOAD DATA
# =========================================================

def load_data():

    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except Exception:
        return []


# =========================================================
# KEYWORDS
# =========================================================

KEYWORDS = {

    "library": [
        "library",
        "book",
        "books",
        "reading",
        "study",
        "studying",
        "library timing",
        "library timings",
        "library hours",
        "reading room"
    ],

    "canteen": [
        "canteen",
        "food",
        "eat",
        "eating",
        "lunch",
        "breakfast",
        "dinner",
        "mess",
        "restaurant",
        "snacks",
        "meal"
    ],

    "hostel": [
        "hostel",
        "room",
        "rooms",
        "accommodation",
        "stay",
        "residence",
        "dormitory",
        "dorm"
    ],

    "placement": [
        "placement",
        "placements",
        "job",
        "jobs",
        "career",
        "recruitment",
        "internship",
        "internships",
        "company",
        "companies"
    ],

    "medical": [
        "medical",
        "doctor",
        "health",
        "hospital",
        "clinic",
        "medicine",
        "healthcare"
    ],

    "sports": [
        "sports",
        "football",
        "cricket",
        "basketball",
        "volleyball",
        "game",
        "games",
        "gym",
        "playground",
        "fitness"
    ],

    "fees": [
        "fees",
        "fee",
        "payment",
        "tuition",
        "money",
        "accounts",
        "cost",
        "charges"
    ],

    "admin": [
        "admin",
        "administration",
        "office",
        "certificate",
        "certificates",
        "document",
        "documents",
        "records",
        "registration"
    ],

    "wifi": [
        "wifi",
        "wi-fi",
        "internet",
        "network",
        "connectivity",
        "connection"
    ],

    "transport": [
        "transport",
        "bus",
        "buses",
        "shuttle",
        "vehicle",
        "travel",
        "route",
        "routes"
    ],

    "labs": [
        "lab",
        "labs",
        "laboratory",
        "laboratories",
        "computer lab",
        "computer labs",
        "practical"
    ],

    "classroom": [
        "classroom",
        "classrooms",
        "class",
        "classes",
        "lecture",
        "lecture hall"
    ],

    "events": [
        "event",
        "events",
        "workshop",
        "workshops",
        "fest",
        "festival",
        "activity",
        "activities",
        "function"
    ],

    "emergency": [
        "emergency",
        "urgent",
        "danger",
        "accident"
    ],

    "security": [
        "security",
        "guard",
        "guards",
        "safety",
        "police"
    ]
}


# =========================================================
# STOP WORDS
# =========================================================

STOP_WORDS = {
    "the",
    "is",
    "are",
    "was",
    "were",
    "what",
    "where",
    "when",
    "how",
    "why",
    "can",
    "could",
    "would",
    "should",
    "tell",
    "me",
    "please",
    "about",
    "give",
    "information",
    "for",
    "to",
    "of",
    "in",
    "on",
    "at",
    "a",
    "an",
    "and",
    "or",
    "do",
    "does",
    "there",
    "this",
    "that"
}


# =========================================================
# NORMALIZE TEXT
# =========================================================

def normalize_text(text):

    text = str(text).lower()

    text = text.replace(
        "wi-fi",
        "wifi"
    )

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# DETECT CATEGORY
# =========================================================

def detect_categories(query):

    query = normalize_text(query)

    detected = []

    for category, words in KEYWORDS.items():

        for word in words:

            word = normalize_text(word)

            if word in query:

                detected.append(category)
                break

    return detected


# =========================================================
# SMART SEARCH
# =========================================================

def search_campus(query):

    data = load_data()

    query = normalize_text(query)

    if not query:
        return []

    detected_categories = detect_categories(query)

    query_words = [
        word
        for word in query.split()
        if word not in STOP_WORDS
        and len(word) > 2
    ]

    results = []

    for item in data:

        category = normalize_text(
            item.get("category", "")
        )

        item_text = normalize_text(
            json.dumps(
                item,
                ensure_ascii=False
            )
        )

        score = 0

        # Category match
        for detected in detected_categories:

            if detected == category:
                score += 20

        # Keyword match
        for keyword in KEYWORDS.get(category, []):

            keyword = normalize_text(keyword)

            if keyword in query:
                score += 6

        # Word match
        for word in query_words:

            if word in item_text:
                score += 3

        # Timing questions
        if (
            "timing" in query
            or "timings" in query
            or "hours" in query
        ):

            if (
                "timing" in item_text
                or "hours" in item_text
                or "open" in item_text
            ):
                score += 5

        # Location questions
        if (
            "where" in query
            or "location" in query
            or "located" in query
        ):

            if (
                item.get("location")
                or "location" in item_text
            ):
                score += 5

        if score > 0:
            results.append(
                (score, item)
            )

    results.sort(
        key=lambda x: x[0],
        reverse=True
    )

    final_results = []
    seen = set()

    for score, item in results:

        identifier = (
            item.get("category", ""),
            item.get("question", ""),
            item.get("answer", "")
        )

        if identifier not in seen:

            seen.add(identifier)
            final_results.append(item)

        if len(final_results) >= 5:
            break

    return final_results


# =========================================================
# NATURAL RESPONSE
# =========================================================

def create_natural_response(
    query,
    results
):

    if not results:

        return (
            "Sorry, I couldn't find relevant "
            "campus information. Try asking about "
            "the library, canteen, hostel, placements, "
            "fees, Wi-Fi, transport, labs or sports."
        )

    best = results[0]

    answer = best.get(
        "answer",
        "Information is available."
    )

    location = best.get("location")

    response = answer

    if location:
        response += f" Location: {location}."

    return response


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "name": "Campus VoiceOS",
        "version": "1.0.0",
        "status": "running",
        "message": "AI-powered campus voice assistant"
    }


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health():

    data = load_data()

    return {
        "status": "healthy",
        "assemblyai": bool(API_KEY),
        "data_loaded": len(data) > 0,
        "information_count": len(data)
    }


# =========================================================
# CATEGORIES
# =========================================================

@app.get("/categories")
def categories():

    data = load_data()

    categories_list = sorted(
        list(
            set(
                item.get(
                    "category",
                    "other"
                )
                for item in data
            )
        )
    )

    return {
        "count": len(categories_list),
        "categories": categories_list
    }


# =========================================================
# STATS
# =========================================================

@app.get("/stats")
def stats():

    data = load_data()

    category_count = {}

    for item in data:

        category = item.get(
            "category",
            "other"
        )

        category_count[category] = (
            category_count.get(
                category,
                0
            ) + 1
        )

    return {
        "total_information": len(data),
        "categories": category_count
    }


# =========================================================
# TEXT QUERY
# =========================================================

@app.post("/query")
def query_campus(
    request: QueryRequest
):

    query = request.query.strip()

    if not query:

        return {
            "query": "",
            "count": 0,
            "category": None,
            "answer": "Please ask a campus-related question.",
            "results": []
        }

    results = search_campus(query)

    detected_categories = detect_categories(query)

    natural_answer = create_natural_response(
        query,
        results
    )

    return {
        "query": query,
        "count": len(results),
        "category": (
            detected_categories[0]
            if detected_categories
            else None
        ),
        "answer": natural_answer,
        "results": results
    }


# =========================================================
# AUDIO TRANSCRIPTION
# =========================================================

@app.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...)
):

    if not API_KEY:

        raise HTTPException(
            status_code=500,
            detail=(
                "AssemblyAI API key is missing. "
                "Add ASSEMBLYAI_API_KEY to the .env file."
            )
        )

    if not file:

        raise HTTPException(
            status_code=400,
            detail="Audio file is required."
        )

    temp_path = None

    try:

        # Read audio
        content = await file.read()

        if not content:

            raise HTTPException(
                status_code=400,
                detail="The uploaded audio file is empty."
            )

        # File name
        filename = file.filename or "audio.webm"

        # Extension
        file_extension = os.path.splitext(
            filename
        )[1]

        if not file_extension:
            file_extension = ".webm"

        # Temporary file
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=file_extension
        ) as temp_file:

            temp_file.write(content)

            temp_path = temp_file.name

        # AssemblyAI
        transcriber = aai.Transcriber()

        transcript = transcriber.transcribe(
            temp_path
        )

        # Check transcription error
        if (
            transcript.status
            == aai.TranscriptStatus.error
        ):

            raise HTTPException(
                status_code=500,
                detail=str(
                    transcript.error
                )
            )

        # Extract text
        text = transcript.text or ""

        if not text.strip():

            return {
                "status": "success",
                "text": "",
                "message": "No speech detected."
            }

        return {
            "status": "success",
            "text": text.strip()
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {str(e)}"
        )

    finally:

        if (
            temp_path
            and os.path.exists(temp_path)
        ):

            try:
                os.remove(temp_path)
            except Exception:
                pass