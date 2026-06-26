# Model Card: Mood Machine

This model card covers **both** versions of the Mood Machine classifier:
a rule based model (`mood_analyzer.py`) and an ML model (`ml_experiments.py`).
I built and compared both.

## 1. Model Overview

**Model type:**
I compared both the rule based model and the scikit-learn ML model on the
same dataset.

**Intended purpose:**
Classify short, English, social-media-style posts as one of
positive / negative / neutral / mixed. This is a learning toy, not a
production or moderation system.

**How it works (brief):**
The rule based model tokenizes text, adds/subtracts points from word lists,
emojis, and slang (with negation flipping the next word), and maps the result
to a label. The ML model turns each post into a bag-of-words count vector and
fits a logistic regression on the labels.

## 2. Data

**Dataset description:**
`SAMPLE_POSTS` has 15 posts: the 6 starters plus 9 I added. The new ones
deliberately cover slang, emojis, sarcasm, double negation, and lukewarm tone.

**Labeling process:**
I labeled each post by my own read of its dominant tone. Several were genuinely
hard: "ok 🙂" I called neutral, though 🙂 often reads as uneasy or passive-
aggressive; "this movie was so bad it was good" I called mixed, but it could be
positive. Those are exactly the rows worth disagreeing about.

**Important characteristics of your dataset:**
- Contains slang ("slaps", "no cap", "meh") and emojis (🙂 🔥 😭)
- Includes sarcasm ("I absolutely love getting stuck in traffic")
- Several posts express mixed feelings
- Many posts are short and ambiguous

**Possible issues with the dataset:**
Only 15 examples and one annotator, so labels reflect my own bias. Classes are
not balanced, and it's all casual US-English internet speech — no other
dialects, languages, or formal writing.

## 3. How the Rule Based Model Works (if used)

**Your scoring rules:**
- Positive/negative word lists each contribute points; "love", "hate",
  "terrible", "amazing", etc. are weighted 2 instead of 1.
- Emojis and slang have their own score maps (🔥 +2, 😭 -2, "meh" -1).
- Negation: a word like "not"/"never" flips the sign of the next sentiment word
  ("not bad" → positive).
- I track positive and negative mass separately, so if both fire I can return
  "mixed" instead of a single scalar that can't tell mixed from neutral.

**Strengths of this approach:**
Predictable and fully explainable — every decision traces to specific tokens.
Handles clear cases, simple negation, and obvious slang/emoji well.

**Weaknesses of this approach:**
Sarcasm (a single positive keyword dominates), ambiguous emoji, and any word
not in the lists. It can't read context, only tokens.

## 4. How the ML Model Works (if used)

**Features used:**
Bag of words via `CountVectorizer` (raw token counts).

**Training data:**
Trained on `SAMPLE_POSTS` and `TRUE_LABELS` from `dataset.py`.

**Training behavior:**
Training accuracy was 1.00 and stayed near-perfect as I added examples —
because with ~62 features over 15 rows it simply memorizes. Changing even one
label visibly shifts its predictions, since each row is a big fraction of the data.

**Strengths and weaknesses:**
Strength: learns associations automatically, no hand-written rules. Weakness:
severe overfitting on this tiny set, no negation (bag of words sees "great" in
"not great"), and `CountVectorizer` silently drops emojis and 1-character
tokens, so emoji signal is lost entirely.

## 5. Evaluation

**How you evaluated the model:**
Both were scored on the labeled posts in `dataset.py`. Rule based: **10/15
(0.67)**. ML: **15/15 (1.00)** training accuracy — but that number is
misleading because it's measured on the data the model memorized.

**Examples of correct predictions:**
- "I love this class so much" → positive (clear keyword, no negation).
- "lowkey stressed but kind of proud of myself" → mixed (both pos and neg fire).
- "not bad at all honestly" → positive (negation flips "bad").

**Examples of incorrect predictions:**
- Rule based: "I absolutely love getting stuck in traffic" → positive, true
  negative. "love" dominates; rules can't see sarcasm.
- Rule based: "I'm exhausted 😭 but we did it" → negative, true mixed. The
  positive half ("we did it") has no listed keyword.
- ML on unseen text: "happy happy happy" → negative, and "not great" →
  positive. The two models fail in different places: rules break on
  sarcasm/ambiguity; ML breaks on anything outside its memorized vocabulary.

## 6. Limitations

- The dataset is tiny (15 posts), so neither model generalizes.
- Neither detects sarcasm reliably.
- Rule based depends entirely on which words I listed and weighted.
- ML training accuracy (1.00) measures memorization, not real performance —
  there is no held-out test set.

## 7. Ethical Considerations

- A post expressing real distress could be misread as neutral or positive
  ("I'm fine 🙂"), which is dangerous if mood detection ever gates support.
- Built only on one annotator's read of US-English slang, it will misinterpret
  other dialects and language communities more often.
- Analyzing personal messages at all raises privacy concerns; mood inferred
  from text is a guess, not a fact about how someone feels.

## 8. Ideas for Improvement

- Add much more labeled data and a real held-out test set instead of training
  accuracy.
- Use TF-IDF instead of raw counts, and preprocessing that preserves emojis.
- Expand negation and slang handling in the rule based scorer.
- Try a small pretrained language model that captures context and sarcasm.
