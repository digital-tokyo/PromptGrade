import re, regex, textstat, spacy
from collections import Counter
from hashlib import md5
from better_profanity import profanity
from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize NLP models
nlp = spacy.load("en_core_web_sm")
profanity.load_censor_words()
sia = SentimentIntensityAnalyzer()

FORNSIC_TERMS = {"evidence", "analysis", "chain of custody", "forensic", "trace", "sample", "report", "investigation"}
SOFT_TERMS = {"maybe","possibly","could","should","consider"}

def _sentiment_clarity(doc):
    pos=sum(1 for t in doc if t.pos_ in{"INTJ","ADJ","ADV"})
    neu=len(doc)-pos
    return pos/(neu+1)

def _categorize(score:int)->str:
    if score>85:return"Tactical"
    if score>60:return"Conversational"
    return"Narrative"

def _forensic_term_coverage(text):
    found = [term for term in FORNSIC_TERMS if term in text.lower()]
    return len(found), found

def grade_prompt(text:str,ptype:str="System")->dict:
    low=text.lower()
    tokens=regex.findall(r'\p{L}+',low)
    doc=nlp(text)
    freq=Counter(tokens)

    # Basic NLP scoring
    constraints={
        "you do not":low.count("you do not"),
        "you never":low.count("you never"),
        "you are not":low.count("you are not")
    }
    soft=sum(low.count(t)for t in SOFT_TERMS)
    contradictions=len(re.findall(r"\byou do not\b.*\bbut\b",low))
    constraint_score=sum(constraints.values())*2
    soft_penalty=soft*3
    contradiction_penalty=contradictions*5

    # Sentiment and readability
    sentiment_bonus=_sentiment_clarity(doc)*1.5
    readability_bonus=max(0,20-textstat.flesch_kincaid_grade(text))

    # Profanity detection (strong penalty)
    profane_words = profanity.contains_profanity(text)
    profanity_penalty = 25 if profane_words else 0

    # Sentiment analysis (negative sentiment penalty)
    sentiment = sia.polarity_scores(text)
    negative_penalty = 15 if sentiment['neg'] > 0.3 else 0

    # Forensic domain term coverage (reward)
    forensic_count, forensic_found = _forensic_term_coverage(text)
    forensic_bonus = forensic_count * 5

    # Calculate raw score
    raw = (100 + constraint_score - soft_penalty - contradiction_penalty
           + sentiment_bonus + readability_bonus - profanity_penalty - negative_penalty
           + forensic_bonus)
    score = max(0,min(100,int(raw)))

    # Compose detailed feedback
    feedback_lines = []
    if profane_words:
        feedback_lines.append("Warning: Profanity detected — lowers professionalism.")
    if negative_penalty:
        feedback_lines.append(f"Note: Negative sentiment detected ({sentiment['neg']:.2f}).")
    if forensic_count == 0:
        feedback_lines.append("No forensic-specific terms found; consider adding domain-relevant language.")
    else:
        feedback_lines.append(f"Forensic terms found: {', '.join(forensic_found)}.")
    if soft > 0:
        feedback_lines.append(f"Hedging/soft terms detected ({soft}); may reduce prompt assertiveness.")
    if contradictions > 0:
        feedback_lines.append(f"Contradictions detected ({contradictions}); clarify your intent.")
    if sum(constraints.values()) > 0:
        feedback_lines.append(f"Constraint phrases used: {constraints}.")
    feedback_lines.append(f"Readability grade bonus: {readability_bonus:.2f}.")
    feedback_lines.append(f"Sentiment clarity bonus: {sentiment_bonus:.2f}.")

    return {
        "hash": md5(text.encode()).hexdigest(),
        "lines": len([l for l in text.splitlines() if l.strip()]),
        "unique_tokens": len(freq),
        "top_tokens": freq.most_common(10),
        "constraints": constraints,
        "soft_terms": soft,
        "contradictions": contradictions,
        "sentiment_clarity": round(sentiment_bonus, 2),
        "readability_bonus": round(readability_bonus, 2),
        "profanity_penalty": profanity_penalty,
        "negative_sentiment_penalty": negative_penalty,
        "forensic_terms_found": forensic_found,
        "forensic_term_count": forensic_count,
        "score": score,
        "type": ptype,
        "category": _categorize(score),
        "feedback": "\n".join(feedback_lines)
    }
