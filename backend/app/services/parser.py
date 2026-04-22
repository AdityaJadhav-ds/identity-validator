import re


def extract_aadhaar(text: str):
    try:
        clean_text = text.replace("\n", " ")
        matches = re.findall(r"\d{4}\s?\d{4}\s?\d{4}", clean_text)
        return matches[0].replace(" ", "") if matches else None
    except:
        return None


def extract_pan(text: str):
    try:
        if not text:
            return None

        # KEEP ORIGINAL TEXT (NO REPLACEMENT)
        text = text.upper()

        # Remove only spaces/newlines
        clean_text = text.replace(" ", "").replace("\n", "")

        # STRICT PAN PATTERN
        candidates = re.findall(r"[A-Z]{5}\d{4}[A-Z]", clean_text)

        if candidates:
            return candidates[0]  # return first valid match

        return None

    except Exception:
        return None


def extract_name(text: str):
    try:
        lines = text.split("\n")
        candidates = []

        for line in lines:
            line = line.strip()

            if len(line) < 5:
                continue

            if any(keyword in line.lower() for keyword in [
                "government", "india", "male", "female", "dob", "income"
            ]):
                continue

            if not all(c.isalpha() or c.isspace() for c in line):
                continue

            words = line.split()

            if 2 <= len(words) <= 4:
                candidates.append(line)

        return max(candidates, key=len) if candidates else None

    except:
        return None