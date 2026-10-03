from pathlib import Path


KNOWLEDGE_FILE = Path("knowledge/city_knowledge.txt")


def load_knowledge():

    return KNOWLEDGE_FILE.read_text(
        encoding="utf-8"
    )


def retrieve_knowledge(query):

    knowledge = load_knowledge()

    query_words = set(
        query.lower().split()
    )

    sections = knowledge.split("\n\n")

    matches = []

    for section in sections:

        section_words = set(
            section.lower().split()
        )

        score = len(
            query_words.intersection(section_words)
        )

        if score > 0:
            matches.append(
                (score, section)
            )

    matches.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    return "\n\n".join(
        section
        for score, section in matches[:3]
    )