import re, regex, textstat, spacy
from collections import Counter
from hashlib import md5

nlp = spacy.load("en_core_web_sm")
SOFT_TERMS = {"maybe","possibly","could","should","consider"}

def _sentiment_clarity(doc):
    pos=sum(1 for t in doc if t.pos_ in{"INTJ","ADJ","ADV"})
    neu=len(doc)-pos
    return pos/(neu+1)

def _categorize(score:int)->str:
    if score>85:return"Tactical"
    if score>60:return"Conversational"
    return"Narrative"

def grade_prompt(text:str,ptype:str="System")->dict:
    low=text.lower()
    tokens=regex.findall(r'\p{L}+',low)
    doc=nlp(text)
    freq=Counter(tokens)
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
    sentiment_bonus=_sentiment_clarity(doc)*1.5
    readability_bonus=max(0,20-textstat.flesch_kincaid_grade(text))
    raw=100+constraint_score-soft_penalty-contradiction_penalty+sentiment_bonus+readability_bonus
    score=max(0,min(100,int(raw)))
    return{
        "hash":md5(text.encode()).hexdigest(),
        "lines":len([l for l in text.splitlines()if l.strip()]),
        "unique_tokens":len(freq),
        "top_tokens":freq.most_common(10),
        "constraints":constraints,
        "soft_terms":soft,
        "contradictions":contradictions,
        "sentiment_clarity":round(sentiment_bonus,2),
        "readability_bonus":round(readability_bonus,2),
        "score":score,
        "type":ptype,
        "category":_categorize(score)
    }
