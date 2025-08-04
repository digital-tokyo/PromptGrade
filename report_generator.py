import json, datetime, uuid
from io import StringIO

def generate_report(res:dict,prompt:str)->tuple[str,str]:
    rid=uuid.uuid4().hex
    stamp=datetime.datetime.utcnow().isoformat()+"Z"
    jb={
        "report_id":rid,
        "timestamp":stamp,
        "analysis":res,
        "prompt":prompt
    }
    txt=StringIO()
    txt.write(f"PromptGrade Report {rid}\nTimestamp: {stamp}\n")
    txt.write(f"Score: {res['score']}  Category: {res['category']}\n")
    txt.write(f"Fingerprint: {res['hash']}\n\nTop Tokens:\n{res['top_tokens']}\n\n")
    txt.write(f"Constraints:\n{res['constraints']}\n\nSoft terms: {res['soft_terms']}\n")
    txt.write(f"Contradictions: {res['contradictions']}\n")
    txt.write(f"Sentiment clarity: {res['sentiment_clarity']}\n")
    txt.write(f"Readability bonus: {res['readability_bonus']}\n\n----- RAW PROMPT -----\n{prompt}")
    return json.dumps(jb,indent=2),txt.getvalue()
