import os
import json
import requests

from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def clean_json(content):

    content = content.strip()

    if content.startswith("```json"):
        content = content.replace("```json", "")

    if content.startswith("```"):
        content = content.replace("```", "")

    if content.endswith("```"):
        content = content[:-3]

    return content.strip()


def analyze_message(message):

    prompt = f"""
Ти AI-помічник студента.

Твоє завдання:
визначити intent повідомлення.

Можливі intent:

schedule_day
teacher
room
time
subject_info
tired_day
light_day
day_summary
pair_count
after_lunch
early_day
late_day
motivation
current_pair
next_pair
end_day

Предмети:
- Архітектура програмного забезпечення
- Цифрова обробка інформації
- Методи та технології машинного навчання
- Система прийняття рішень
- Методи та технології обробки великих та надвеликих даних
- Програмно-визначені системи

ВАЖЛИВО:
повертай ТІЛЬКИ JSON.
Без пояснень.
Без markdown.
Без ```json.

Поверни JSON:

{{
    "intent": "...",
    "subject": "...",
    "day": "..."
}}

Приклади:

"розклад"
→ {{"intent":"schedule_day","subject":null,"day":null}}

"пари"
→ {{"intent":"schedule_day","subject":null,"day":"сьогодні"}}

"пари завтра"
→ {{"intent":"schedule_day","subject":null,"day":"завтра"}}

"хто веде мл"
→ {{"intent":"teacher","subject":"Методи та технології машинного навчання","day":null}}

"де буде мл"
→ {{"intent":"room","subject":"Методи та технології машинного навчання","day":null}}

"коли біг дата"
→ {{"intent":"time","subject":"Методи та технології обробки великих та надвеликих даних","day":null}}

"шо по мл завтра"
→ {{"intent":"subject_info","subject":"Методи та технології машинного навчання","day":"завтра"}}

"я завтра втомлюсь"
→ {{"intent":"tired_day","subject":null,"day":"завтра"}}

"коли легкий день"
→ {{"intent":"light_day","subject":null,"day":null}}

"підсумуй завтра"
→ {{"intent":"day_summary","subject":null,"day":"завтра"}}

"що мене чекає завтра"
→ {{"intent":"day_summary","subject":null,"day":"завтра"}}

"який завтра день"
→ {{"intent":"day_summary","subject":null,"day":"завтра"}}

"скільки завтра пар"
→ {{"intent":"pair_count","subject":null,"day":"завтра"}}

"шо в мене після обіду"
→ {{"intent":"after_lunch","subject":null,"day":"сьогодні"}}

"я завтра рано?"
→ {{"intent":"early_day","subject":null,"day":"завтра"}}

"я завтра пізно?"
→ {{"intent":"late_day","subject":null,"day":"завтра"}}

"я не хочу завтра на пари"
→ {{"intent":"motivation","subject":null,"day":"завтра"}}

"шо зараз?"
→ {{"intent":"current_pair","subject":null,"day":null}}

"яка зараз пара?"
→ {{"intent":"current_pair","subject":null,"day":null}}

"яка наступна пара?"
→ {{"intent":"next_pair","subject":null,"day":null}}

"шо далі?"
→ {{"intent":"next_pair","subject":null,"day":null}}

"коли я закінчую?"
→ {{"intent":"end_day","subject":null,"day":"сьогодні"}}

"до котрої сьогодні?"
→ {{"intent":"end_day","subject":null,"day":"сьогодні"}}

"я втомлюсь завтра?"
→ {{"intent":"tired_day","subject":null,"day":"завтра"}}

"я завтра втомлюсь?"
→ {{"intent":"tired_day","subject":null,"day":"завтра"}}

"який найлегший день?"
→ {{"intent":"light_day","subject":null,"day":null}}
Повідомлення:
"{message}"
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0
    }

    response = requests.post(
        GROQ_URL,
        headers=headers,
        json=body
    )

    data = response.json()

    print("GROQ RESPONSE:")
    print(data)

    content = data["choices"][0]["message"]["content"]

    print("RAW LLM CONTENT:")
    print(content)

    content = clean_json(content)

    print("CLEANED CONTENT:")
    print(content)

    return json.loads(content)