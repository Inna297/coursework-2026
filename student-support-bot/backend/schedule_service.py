import datetime

schedule = {
    "понеділок": [
        {
            "subject": "ДВВС",
            "time": "13:30-14:50"
        },

        {
            "subject": "Архітектура ПЗ",
            "type": "Лаб",
            "teacher": "Прокопів Роман Володимирович",
            "room": "10/Б",
            "time": "15:05-16:25"
        },

        {
            "subject": "Архітектура ПЗ",
            "type": "Лекція",
            "teacher": "Прокопів Роман Володимирович",
            "room": "2/Б",
            "time": "16:40-18:00"
        },
    ],

    "вівторок": [
        {
            "subject": "Цифрова обробка інформації",
            "type": "Лекція",
            "teacher": "Фургала Юрій Михайлович",
            "room": "2/Б",
            "time": "11:50-13:10"
        },

        {
            "subject": "Методи та технології машинного навчання",
            "type": "Лекція",
            "teacher": "Ляшкевич Василь Яремович",
            "room": "2/Б",
            "time": "13:30-14:50"
        },
    ],

    "середа": [
        {
            "subject": "Цифрова обробка інформації",
            "type": "Лаб",
            "teacher": "Фесюк Андрій Вікторович",
            "room": "7/Т",
            "time": "8:30-9:50"
        },

        {
            "subject": "Система прийняття рішень",
            "type": "Лекція",
            "teacher": "Дуфанець Марта Василівна",
            "room": "130/Т",
            "time": "10:10-11:30"
        },

        {
            "subject": "Методи та технології обробки великих та надвеликих даних",
            "type": "Лекція",
            "teacher": "Мисюк Ірина Володимирівна",
            "room": "2/Б",
            "time": "11:50-13:10"
        },

        {
            "subject": "Система прийняття рішень",
            "type": "Лаб",
            "teacher": "Дуфанець Марта Василівна",
            "room": "7/Т",
            "time": "13:30-14:50"
        },
    ],

    "четвер": [
        {
            "subject": "ДВВС",
            "time": "11:50-13:10"
        },

        {
            "subject": "ДВВС",
            "time": "13:30-14:50"
        },

        {
            "subject": "Методи та технології обробки великих та надвеликих даних",
            "type": "Лаб",
            "teacher": "Мисюк Ірина Володимирівна",
            "room": "10/Б",
            "time": "15:05-16:25"
        },
    ],

    "пʼятниця": [
        {
            "subject": "Програмно-визначені системи",
            "type": "Лекція",
            "teacher": "Васюта Василь Михайлович",
            "room": "130/Т",
            "time": "8:30-9:50"
        },

        {
            "subject": "Програмно-визначені системи",
            "type": "Лаб",
            "teacher": "Васюта Василь Михайлович",
            "room": "3/Т",
            "time": "10:10-11:30"
        },

        {
            "subject": "Методи та технології машинного навчання",
            "type": "Лаб",
            "teacher": "Ляшкевич Василь Яремович",
            "room": "9/Б",
            "time": "11:50-13:10"
        },
    ]
}

aliases = {
    "апз": "Архітектура ПЗ",
    "архітектура": "Архітектура ПЗ",
    "арх пз": "Архітектура ПЗ",

    "цоі": "Цифрова обробка інформації",

    "спр": "Система прийняття рішень",
    "прийняття рішень": "Система прийняття рішень",

    "біг дата": "Методи та технології обробки великих та надвеликих даних",
    "big data": "Методи та технології обробки великих та надвеликих даних",

    "пвс": "Програмно-визначені системи",

    "мн": "Методи та технології машинного навчання",
    "мл": "Методи та технології машинного навчання",
    "машинне навчання": "Методи та технології машинного навчання",
}

days = [
    "понеділок",
    "вівторок",
    "середа",
    "четвер",
    "пʼятниця"
]


def get_today():
    return days[datetime.datetime.today().weekday()]


def format_schedule(day):

    if day not in schedule:
        return "Пар немає."

    text = f"Розклад на {day}\n\n"

    for i, lesson in enumerate(schedule[day], 1):

        text += f"{i}. {lesson['subject']}"

        if "type" in lesson:
            text += f" ({lesson['type']})"

        text += "\n"

        if "teacher" in lesson:
            text += f"{lesson['teacher']}\n"

        if "room" in lesson:
            text += f"Аудиторія: {lesson['room']}\n"

        text += f"{lesson['time']}\n\n"

    return text


def detect_subject(user_message):

    msg = user_message.lower()

    for alias, real_name in aliases.items():

        if alias in msg:
            return real_name

    return None


def find_next_subject(subject):

    today_index = datetime.datetime.today().weekday()

    for offset in range(5):

        idx = (today_index + offset) % 5
        day = days[idx]

        for lesson in schedule[day]:

            if lesson["subject"] == subject:

                return (
                    f"Найближча пара:\n\n"
                    f"{subject}\n"
                    f"{day}\n"
                    f"{lesson['time']}\n"
                    f"Аудиторія: {lesson.get('room', 'невідомо')}\n"
                    f"Викладач: {lesson.get('teacher', 'невідомо')}"
                )

    return "Не знайшов інформацію."
def get_current_pair():
  
    now = datetime.datetime.now()

    current_time = now.strftime("%H:%M")

    today = get_today()

    if today not in schedule:
        return "Сьогодні пар немає."

    for lesson in schedule[today]:

        start, end = lesson["time"].split("-")

        if start <= current_time <= end:

            return (
                f"Зараз триває:\n\n"
                f"{lesson['subject']}\n"
                f"{lesson['time']}\n"
                f"Аудиторія: {lesson.get('room', 'невідомо')}"
            )

    return "Зараз пари немає."


def get_next_pair():

    now = datetime.datetime.now()

    current_time = now.strftime("%H:%M")

    today = get_today()

    if today not in schedule:
        return "Сьогодні пар немає."

    for lesson in schedule[today]:

        start, end = lesson["time"].split("-")

        if current_time < start:

            return (
                f"Наступна пара:\n\n"
                f"{lesson['subject']}\n"
                f"{lesson['time']}\n"
                f"Аудиторія: {lesson.get('room', 'невідомо')}"
            )

    return "Сьогодні пар більше немає."


def get_end_of_day():

    today = get_today()

    if today not in schedule:
        return "Сьогодні пар немає."

    last_lesson = schedule[today][-1]

    end_time = last_lesson["time"].split("-")[1]

    return f"Сьогодні пари до {end_time}."

months = {
    "січня": 1,
    "лютого": 2,
    "березня": 3,
    "квітня": 4,
    "травня": 5,
    "червня": 6,
    "липня": 7,
    "серпня": 8,
    "вересня": 9,
    "жовтня": 10,
    "листопада": 11,
    "грудня": 12,
}


def detect_day_from_message(message):

    msg = message.lower()

    # ---------- DAY WORDS ----------
    for day in days:

        if day in msg:
            return day

    # ---------- DD.MM ----------
    import re

    match = re.search(r"(\d{1,2})[./](\d{1,2})", msg)

    if match:

        day_num = int(match.group(1))
        month_num = int(match.group(2))

        try:

            date_obj = datetime.datetime(
                datetime.datetime.now().year,
                month_num,
                day_num
            )

            weekday = days[date_obj.weekday()]

            return weekday

        except:
            return None

    # ---------- 18 травня ----------
    words = msg.split()

    for i in range(len(words) - 1):

        if words[i].isdigit():

            day_num = int(words[i])

            month_word = words[i + 1]

            if month_word in months:

                try:

                    date_obj = datetime.datetime(
                        datetime.datetime.now().year,
                        months[month_word],
                        day_num
                    )

                    weekday = days[date_obj.weekday()]

                    return weekday

                except:
                    return None

    return None
def find_subject_lesson(subject):
  
    now = datetime.datetime.now()

    current_time = now.strftime("%H:%M")

    today_index = now.weekday()

    for offset in range(5):

        idx = (today_index + offset) % 5

        day = days[idx]

        if day not in schedule:
            continue

        lessons = schedule[day]

        for lesson in lessons:

            lesson_subject = lesson["subject"].lower()

            # ГОЛОВНИЙ ФІКС
            if subject.lower() in lesson_subject:

                # ---------- TODAY ----------
                if offset == 0:

                    start, end = lesson["time"].split("-")

                    # якщо пара триває
                    if start <= current_time <= end:
                        return lesson, day

                    # якщо ще буде сьогодні
                    if current_time < start:
                        return lesson, day

                else:
                    return lesson, day

    return None, None

def get_teacher(subject):
  
    lesson, day = find_subject_lesson(subject)

    if not lesson:
        return "Викладача ще не знайдено."

    return (
        f"{lesson['subject']}:\n"
        f"{lesson.get('teacher', 'невідомо')}"
    )


def get_room(subject):
  
    lesson, day = find_subject_lesson(subject)

    if not lesson:
        return "Аудиторія ще невідома."

    return lesson.get("room", "невідомо")


def get_time(subject):
  
    lesson, day = find_subject_lesson(subject)

    if not lesson:
        return "Час пари ще невідомий."

    return (
        f"{day}\n"
        f"{lesson['time']}"
    )


def get_after_subject(subject):
  
    lesson, day = find_subject_lesson(subject)

    if not lesson:
        return f"{subject} не знайдено."

    lessons = schedule[day]

    for i in range(len(lessons) - 1):

        current_subject = lessons[i]["subject"]

        if current_subject == lesson["subject"]:

            next_lesson = lessons[i + 1]

            return (
                f"Після {subject}:\n\n"
                f"{next_lesson['subject']}\n"
                f"{next_lesson['time']}\n"
                f"Аудиторія: {next_lesson.get('room', 'невідомо')}"
            )

    return (
        f"Після {subject} більше пар немає 😌"
    )

def get_subject_by_day(subject, day):
  
    if day not in schedule:
        return "Пар немає."

    found = []

    for lesson in schedule[day]:

        if subject.lower() in lesson["subject"].lower():

            text = (
                f"{lesson['subject']}"
            )

            if "type" in lesson:
                text += f" ({lesson['type']})"

            text += "\n"

            if "teacher" in lesson:
                text += f"{lesson['teacher']}\n"

            if "room" in lesson:
                text += f"Аудиторія: {lesson['room']}\n"

            text += f"{lesson['time']}"

            found.append(text)

    if not found:
        return f"{subject} у {day} немає."

    result = f"{subject} — {day}\n\n"

    result += "\n\n".join(found)

    return result

def get_day_name(day_keyword):
  
    if day_keyword == "сьогодні":
        return get_today()

    if day_keyword == "завтра":

        idx = days.index(get_today())

        return days[(idx + 1) % 5]

    return day_keyword


def get_pair_count(day_keyword):

    day = get_day_name(day_keyword)

    if day not in schedule:
        return "Пар немає."

    count = len(schedule[day])

    return f"У {day} {count} пари."


def get_after_lunch(day_keyword="сьогодні"):

    day = get_day_name(day_keyword)

    if day not in schedule:
        return "Пар немає."

    text = f"Після обіду у {day}:\n\n"

    found = False

    for lesson in schedule[day]:

        start = lesson["time"].split("-")[0]

        hour = int(start.split(":")[0])

        if hour >= 13:

            found = True

            text += (
                f"{lesson['subject']}\n"
                f"{lesson['time']}\n"
            )

            if "room" in lesson:
                text += f"Аудиторія: {lesson['room']}\n"

            text += "\n"

    if not found:
        return f"Після обіду у {day} пар немає."

    return text


def get_early_day(day_keyword):

    day = get_day_name(day_keyword)

    if day not in schedule:
        return "Пар немає."

    first_pair = schedule[day][0]

    start = first_pair["time"].split("-")[0]

    if start <= "09:00":

        return (
            f"Так 😭\n"
            f"Перша пара у {day} о {start}"
        )

    return (
        f"Ні 😎\n"
        f"Перша пара у {day} о {start}"
    )


def get_easy_day():

    min_pairs = 999
    best_day = None

    for day in days:

        count = len(schedule[day])

        if count < min_pairs:

            min_pairs = count
            best_day = day

    return (
        f"Найлегший день — {best_day}.\n"
        f"У тебе {min_pairs} пари."
    )


def get_tired_day(day_keyword):

    day = get_day_name(day_keyword)

    if day not in schedule:
        return "Пар немає."

    count = len(schedule[day])

    if count >= 4:
        return f"Так 😵 У {day} аж {count} пари."

    if count == 3:
        return f"Ну... середньо 😅 У {day} 3 пари."

    return f"Ні 😎 У {day} лише {count} пари."

def get_day_summary(day):
  
    if day not in schedule:
        return "Пар немає."

    lessons = schedule[day]

    count = len(lessons)

    first_pair = lessons[0]["time"].split("-")[0]
    last_pair = lessons[-1]["time"].split("-")[1]

    labs = 0

    subjects = []

    for lesson in lessons:

        subjects.append(lesson["subject"])

        if lesson.get("type") == "Лаб":
            labs += 1

    # ---------- DIFFICULTY ----------
    difficulty = "легкий"

    if count >= 4 or labs >= 2:
        difficulty = "важкий"

    elif count == 3:
        difficulty = "середній"

    subjects_text = ", ".join(subjects)

    return (
        f"{day.capitalize()}:\n\n"
        f"• Пар: {count}\n"
        f"• Початок: {first_pair}\n"
        f"• Кінець: {last_pair}\n"
        f"• Лабораторних: {labs}\n"
        f"• Предмети: {subjects_text}\n\n"
        f"День оцінюється як {difficulty}."
    )

def resolve_day(day_value):
  
    if not day_value:
        return get_today()

    if day_value == "сьогодні":
        return get_today()

    if day_value == "завтра":

        idx = days.index(get_today())

        return days[(idx + 1) % 5]

    # ---------- DD.MM ----------
    import re

    match = re.search(r"(\d{1,2})[./](\d{1,2})", day_value)

    if match:

        day_num = int(match.group(1))
        month_num = int(match.group(2))

        try:

            date_obj = datetime.datetime(
                datetime.datetime.now().year,
                month_num,
                day_num
            )

            return days[date_obj.weekday()]

        except:
            return get_today()

    return day_value

def get_week_schedule():
  
    text = "Розклад на тиждень:\n\n"

    for day in days:

        text += format_schedule(day)
        text += "\n-------------------\n\n"

    return text