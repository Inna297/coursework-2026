from backend.llm_service import analyze_message

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.schedule_service import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

last_context = {
    "intent": None,
    "subject": None
}

modules = {
    "Цифрова обробка інформації":
    "Модуль 1 — 31 березня\nМодуль 2 — 26 травня",

    "Методи та технології машинного навчання":
    "Модуль 1 — 31 березня\nМодуль 2 — 26 травня",

    "Система прийняття рішень":
    "Модуль 1 — 15 квітня\nМодуль 2 — 27 травня",

    "Методи та технології обробки великих та надвеликих даних":
    "Модуль 1 — 18 березня\nМодуль 2 — 22 квітня",

    "Програмно-визначені системи":
    "Колоквіум — 3 квітня",
}

exams = {
    "Цифрова обробка інформації":
    "Залік — 26 травня",

    "Методи та технології обробки великих та надвеликих даних":
    "Залік — 27 травня",

    "Програмно-визначені системи":
    "Залік — 29 травня",

    "ДВВС":
    "Залік — 25-28 травня",

    "Архітектура програмного забезпечення":
    "Екзамен — дата ще невідома",

    "Система прийняття рішень":
    "Екзамен — дата ще невідома",

    "Методи та технології машинного навчання":
    "Екзамен — дата ще невідома",
}


@app.get("/")
def root():
    return {"message": "FEP-33 Assistant працює"}


@app.get("/chat")
def chat(message: str = Query(...)):

    msg = message.lower().strip()

    try:

        llm_data = analyze_message(message)

        intent = llm_data.get("intent")
        llm_subject = llm_data.get("subject")
        llm_day = llm_data.get("day")

    except Exception as e:

        print("MAIN LLM ERROR:", e)

        intent = None
        llm_subject = None
        llm_day = None

    # ---------- DAY ----------
    target_day = get_today()

    # завтра
    if llm_day == "завтра":

        idx = days.index(get_today())
        target_day = days[(idx + 1) % 5]

    # сьогодні
    elif llm_day == "сьогодні":

        target_day = get_today()

    # конкретний день
    elif llm_day in days:

        target_day = llm_day

    # дата типу 27.05
    elif llm_day:

        detected = detect_day_from_message(llm_day)

        if detected:
            target_day = detected

    # ---------- CURRENT PAIR ----------
    if intent == "current_pair":

        return {
            "reply": get_current_pair()
        }

    # ---------- NEXT PAIR ----------
    if intent == "next_pair":

        return {
            "reply": get_next_pair()
        }

    # ---------- END DAY ----------
    if intent == "end_day":

        return {
            "reply": get_end_of_day()
        }

    # ---------- EARLY DAY ----------
    if intent == "early_day":

        lessons = schedule[target_day]

        first_time = lessons[0]["time"].split("-")[0]

        hour = int(first_time.split(":")[0])

        if hour <= 9:

            return {
                "reply":
                f"Так 😭\n\n"
                f"Перша пара о {first_time}"
            }

        return {
            "reply":
            f"Ні 😌\n\n"
            f"Початок лише о {first_time}"
        }

    # ---------- LATE DAY ----------
    if intent == "late_day":

        lessons = schedule[target_day]

        last_time = lessons[-1]["time"].split("-")[1]

        return {
            "reply":
            f"Закінчуєш о {last_time}"
        }

    # ---------- MOTIVATION ----------
    if intent == "motivation":

        lessons = schedule[target_day]

        count = len(lessons)

        if count <= 2:

            return {
                "reply":
                "Та там не так страшно 😌\n\n"
                f"У тебе лише {count} пар."
            }

        return {
            "reply":
            "Трошки важкувато 😭\n\n"
            "Але ти вже стільки всього витягнула,\n"
            "то і цей день переживеш 💪"
        }

    # ---------- DAY SUMMARY ----------
    if intent == "day_summary":

        return {
            "reply": get_day_summary(target_day)
        }

    # ---------- TIRED ----------
    if intent == "tired_day":

        return {
            "reply": get_tired_day(target_day)
        }

    # ---------- LIGHT DAY ----------
    if intent == "light_day":

        return {
            "reply": get_easy_day()
        }

    # ---------- PAIR COUNT ----------
    if intent == "pair_count":

        return {
            "reply": get_pair_count(target_day)
        }

    # ---------- AFTER LUNCH ----------
    if intent == "after_lunch":

        return {
            "reply": get_after_lunch(target_day)
        }
    
    # ---------- MODULES ----------
    if "модул" in msg:

        text = "Модулі:\n\n"

        for subject_name, info in modules.items():
            text += f"{subject_name}\n{info}\n\n"

        return {"reply": text}

    # ---------- EXAMS ----------
    if "екзам" in msg or "залік" in msg:

        text = "Екзамени / заліки:\n\n"

        for subject_name, info in exams.items():
            text += f"{subject_name}\n{info}\n\n"

        return {"reply": text}

    # ---------- SCHEDULE DAY ----------
    if intent == "schedule_day":

        # ---------- WEEK ----------
        if llm_day == "тиждень":

            return {
                "reply": get_week_schedule()
            }

        # ---------- NORMAL ----------
        return {
            "reply": format_schedule(target_day)
        }

    # ---------- SUBJECT ----------
    subject = detect_subject(msg)

    if subject:

        last_context["subject"] = subject

    elif last_context["subject"]:

        subject = last_context["subject"]

    # ---------- SUBJECT + DAY ----------
    if subject and llm_day:

        return {
            "reply": get_subject_by_day(subject, target_day)
        }

    # ---------- SUBJECT QUERIES ----------
    if subject:

        if (
            "хто" in msg
            or intent == "teacher"
        ):

            return {
                "reply": get_teacher(subject)
            }

        if (
            "де" in msg
            or "аудитор" in msg
            or intent == "room"
        ):

            return {
                "reply": get_room(subject)
            }

        if (
            "коли" in msg
            or "час" in msg
            or intent == "time"
        ):

            return {
                "reply": get_time(subject)
            }

        return {
            "reply": find_next_subject(subject)
        }



    # ---------- FALLBACK ----------
    return {
        "reply":
        "Я не до кінця зрозумів запит 😅"
    }