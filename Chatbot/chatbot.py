import json
import re
from pathlib import Path
from datetime import datetime


# Project directory and FAQ dataset
ROOT_DIR = Path(__file__).resolve().parent
FAQ_FILE = ROOT_DIR / "sample_faq.json"


def load_dataset():
    """Load greetings and FAQs from the JSON dataset."""
    try:
        with open(FAQ_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("The dataset must contain a JSON object.")

        if not isinstance(data.get("greetings"), list):
            raise ValueError("The greetings section must be a list.")

        if not isinstance(data.get("faqs"), list):
            raise ValueError("The FAQs section must be a list.")

        for faq in data["faqs"]:
            if not isinstance(faq, dict):
                raise ValueError("Each FAQ must be a JSON object.")

            if not isinstance(faq.get("question"), str):
                raise ValueError("Each FAQ must have a question.")

            if not isinstance(faq.get("answer"), str):
                raise ValueError("Each FAQ must have an answer.")

        return data

    except FileNotFoundError:
        print(f"Error: FAQ dataset not found at {FAQ_FILE}")
        return None

    except (json.JSONDecodeError, ValueError) as error:
        print(f"Error loading FAQ dataset: {error}")
        return None


def normalize_text(text):
    """Normalize input for matching."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def tokenize(text):
    """Extract words using regular expressions."""
    return set(re.findall(r"\b[a-z0-9]+\b", normalize_text(text)))


def calculate_match(user_input, question):
    """Calculate keyword overlap between input and FAQ question."""
    user_words = tokenize(user_input)
    question_words = tokenize(question)

    if not user_words or not question_words:
        return 0

    # Ignore common words that do not contribute much to matching.
    stop_words = {
        "a", "an", "the", "is", "are", "am", "do", "does",
        "i", "we", "you", "your", "my", "our", "to", "of",
        "for", "in", "on", "how", "what", "when", "can",
        "me", "please", "and", "will", "be"
    }

    user_keywords = user_words - stop_words
    question_keywords = question_words - stop_words

    if not user_keywords or not question_keywords:
        return 0

    common = user_keywords.intersection(question_keywords)

    # Score based on how much of the FAQ question is matched.
    return len(common) / len(question_keywords)


def get_response(user_input, data):
    """Identify user intent and return an appropriate response."""

    text = normalize_text(user_input)

    # Exit commands
    if re.fullmatch(r"(bye|goodbye|exit|quit)", text):
        return "EXIT"

    # Greeting detection
    greeting_patterns = [
        r"\bhi\b",
        r"\bhello\b",
        r"\bhey\b",
        r"\bgood morning\b",
        r"\bgood afternoon\b",
        r"\bgood evening\b"
    ]

    if any(re.search(pattern, text) for pattern in greeting_patterns):
        return (
            "Hello! Welcome to the Datheon support assistant.\n"
            "You can ask about business hours, project submission, "
            "or certificates."
        )

    # Business hours intent
    if re.search(
        r"\b(hours?|timings?|open|closed|working days|"
        r"business hours|office hours)\b",
        text
    ):
        return data["faqs"][0]["answer"]

    # Project submission intent
    if re.search(
        r"\b(project|submission|submit|github|repository|"
        r"student workspace|internship project)\b",
        text
    ):
        for faq in data["faqs"]:
            question = normalize_text(faq["question"])

            if "submit" in question or "project" in question:
                return faq["answer"]

    # Certificate intent
    if re.search(
        r"\b(certificate|certificates|certification|"
        r"issued|issuance|receive certificate)\b",
        text
    ):
        for faq in data["faqs"]:
            question = normalize_text(faq["question"])

            if "certificate" in question:
                return faq["answer"]

    # General FAQ matching
    scored_faqs = []

    for faq in data["faqs"]:
        score = calculate_match(user_input, faq["question"])
        scored_faqs.append((score, faq["answer"]))

    scored_faqs.sort(key=lambda item: item[0], reverse=True)

    if scored_faqs and scored_faqs[0][0] >= 0.4:
        return scored_faqs[0][1]

    # Fallback response
    return (
        "I'm sorry, I couldn't find an answer to that question.\n"
        "Try asking about business hours, internship project submission, "
        "or certificate issuance."
    )


def main():
    """Run the interactive chatbot."""
    print("=" * 55)
    print("       DATHEON CUSTOMER SUPPORT CHATBOT")
    print("=" * 55)

    data = load_dataset()

    if data is None:
        print("Chatbot cannot start without a valid FAQ dataset.")
        return

    print("Bot: Hello! How can I help you today?")
    print("Bot: Type 'bye', 'exit', or 'quit' to end the conversation.")

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if not user_input:
                print("Bot: Please enter a question.")
                continue

            response = get_response(user_input, data)

            if response == "EXIT":
                print("Bot: Thank you for contacting Datheon support. Goodbye!")
                break

            print(f"Bot: {response}")

        except (KeyboardInterrupt, EOFError):
            print("\nBot: Conversation ended. Goodbye!")
            break


if __name__ == "__main__":
    main()