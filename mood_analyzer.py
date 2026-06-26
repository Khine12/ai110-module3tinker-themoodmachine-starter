# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

Flow:
  preprocess(text) -> tokens
  score_text(text) -> single numeric score (positive minus negative)
  predict_label(text) -> "positive" / "negative" / "neutral" / "mixed"
"""

import re
import string
from typing import List, Optional, Tuple

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS


# --- Signals that aren't plain dictionary words --------------------------
EMOJI_SCORES = {
    "🙂": +1, "😂": +2, "❤️": +2, "🥳": +2, "🔥": +2, "👍": +1,
    "😭": -2, "😡": -2, "👎": -2, "🙁": -1,
    "💀": +1,   # slang "I'm dead" = hilarious (deliberately ambiguous)
    "🥲": -1,   # bittersweet, leaning negative
    ":)": +1, ":-)": +1, ":(": -1, ":-(": -1,
}
SLANG_SCORES = {
    "lol": +1, "lmao": +1, "slaps": +2, "fire": +2, "goated": +2,
    "meh": -1, "ugh": -1, "sucks": -2,
}
# Words stronger than the default +/-1.
WEIGHTS = {
    "love": 2, "amazing": 2, "awesome": 2, "proud": 2,
    "hate": 2, "terrible": 2, "awful": 2, "exhausted": 2,
}
NEGATORS = {"not", "no", "never", "dont", "don't", "aint", "ain't",
            "cant", "can't", "isnt", "isn't", "wasnt", "wasn't"}


class MoodAnalyzer:
    """A very simple, rule based mood classifier."""

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------
    def preprocess(self, text: str) -> List[str]:
        """
        Lowercase, pull emojis/emoticons out as their own tokens, strip
        punctuation off words, and collapse elongated chars ("soooo" -> "soo").
        """
        text = text.strip().lower()
        tokens: List[str] = []
        for raw in text.split():
            if raw in EMOJI_SCORES:          # whole token is an emoticon like ":)"
                tokens.append(raw)
                continue
            for ch in raw:                   # peel unicode emoji off a word
                if ch in EMOJI_SCORES:
                    tokens.append(ch)
            word = raw.strip(string.punctuation)
            word = re.sub(r"(.)\1{2,}", r"\1\1", word)
            if word:
                tokens.append(word)
        return tokens

    # ---------------------------------------------------------------------
    # Per-token value + (positive, negative) mass
    # ---------------------------------------------------------------------
    def _token_value(self, token: str) -> int:
        if token in EMOJI_SCORES:
            return EMOJI_SCORES[token]
        if token in SLANG_SCORES:
            return SLANG_SCORES[token]
        if token in self.positive_words:
            return WEIGHTS.get(token, 1)
        if token in self.negative_words:
            return -WEIGHTS.get(token, 1)
        return 0

    def _score_components(self, text: str) -> Tuple[int, int]:
        """Return (positive_mass, negative_mass), each >= 0, with negation handled."""
        tokens = self.preprocess(text)
        pos, neg = 0, 0
        negate = False
        for tok in tokens:
            if tok in NEGATORS:
                negate = True
                continue
            val = self._token_value(tok)
            if negate:
                val = -val              # flip ONLY the immediately next token
                negate = False          # then reset (avoids "no cap" bleeding into 🔥)
            if val > 0:
                pos += val
            elif val < 0:
                neg += -val
        return pos, neg

    # ---------------------------------------------------------------------
    # Scoring  (enhancement: negation + weighting + emoji/slang signals)
    # ---------------------------------------------------------------------
    def score_text(self, text: str) -> int:
        """Single numeric mood score: positive mass minus negative mass."""
        pos, neg = self._score_components(text)
        return pos - neg

    # ---------------------------------------------------------------------
    # Label
    # ---------------------------------------------------------------------
    def predict_label(self, text: str) -> str:
        """
        Map the score to a label. A single scalar can't tell 'neutral' from
        'mixed', so we also check whether BOTH sides fired.
        """
        score = self.score_text(text)               # the stub's numeric score
        pos, neg = self._score_components(text)      # to distinguish mixed
        if pos >= 1 and neg >= 1:
            return "mixed"
        if score > 0:
            return "positive"
        if score < 0:
            return "negative"
        return "neutral"

    # ---------------------------------------------------------------------
    def explain(self, text: str) -> str:
        pos, neg = self._score_components(text)
        return f"Score = {pos - neg} (pos_mass={pos}, neg_mass={neg}) -> {self.predict_label(text)}"
