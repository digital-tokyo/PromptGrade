# PromptGrade™

Elite Streamlit app that scores and visualizes AI prompts using deterministic NLP logic and Sony-inspired visual design.

---

## 🔧 Features
- Constraint + soft language detection
- Contradiction scanning
- Sentiment & readability scoring
- Visual bar chart
- JSON + TXT report downloads
- Ultra-premium UI (Sony-style)

---

## 🚀 Local Setup

```bash
git clone https://github.com/digital-tokyo/promptgrade.git
cd promptgrade
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run app.py
