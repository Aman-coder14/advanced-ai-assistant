import wikipedia


def search_wikipedia(query):

    try:

        result = wikipedia.summary(
            query,
            sentences=5,
            auto_suggest=True
        )

        return result

    except Exception:

        return None