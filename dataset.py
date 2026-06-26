"""
Shared data for the Mood Machine lab.  (TF reference version)
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy", "great", "good", "love", "excited",
    "awesome", "fun", "chill", "relaxed", "amazing",
    "proud", "hopeful",
]

NEGATIVE_WORDS = [
    "sad", "bad", "terrible", "awful", "angry",
    "upset", "tired", "stressed", "hate", "boring",
    "exhausted", "annoyed",
]

# ---------------------------------------------------------------------
# Labeled dataset
# ---------------------------------------------------------------------

SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    # --- added: realistic / tricky examples ---
    "lowkey stressed but kind of proud of myself",   # mixed
    "I absolutely love getting stuck in traffic",    # sarcasm -> really negative
    "this movie was so bad it was good lol",          # mixed / ironic
    "ok 🙂",                                           # emoji, flat-to-uneasy
    "not bad at all honestly",                        # double negation -> positive
    "wow great another meeting that could've been an email",  # sarcasm -> negative
    "this slaps no cap 🔥",                            # slang -> positive
    "I'm exhausted 😭 but we did it",                  # mixed
    "meh it was okay i guess",                        # neutral / lukewarm
]

TRUE_LABELS = [
    "positive",  # I love this class so much
    "negative",  # Today was a terrible day
    "mixed",     # Feeling tired but kind of hopeful
    "neutral",   # This is fine
    "positive",  # So excited for the weekend
    "negative",  # I am not happy about this
    "mixed",     # lowkey stressed but kind of proud of myself
    "negative",  # sarcasm: love getting stuck in traffic
    "mixed",     # so bad it was good
    "neutral",   # ok 🙂   (genuinely arguable -> good discussion edge case)
    "positive",  # not bad at all
    "negative",  # sarcastic "wow great"
    "positive",  # this slaps no cap
    "mixed",     # exhausted but we did it
    "neutral",   # meh it was okay
]

assert len(SAMPLE_POSTS) == len(TRUE_LABELS), "Lengths must match!"
