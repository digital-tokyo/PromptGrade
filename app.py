import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import streamlit as st, matplotlib.pyplot as plt
from prompt_grader import grade_prompt
from report_generator import generate_report

st.set_page_config(page_title="PromptGrade",layout="centered",page_icon="🅿︎")

with open("style.css")as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

st.title("PromptGrade")

txt=st.text_area("Paste your prompt here",height=280)
ptype=st.selectbox("Prompt type",["System","Assistant","User"])

if st.button("Grade"):
    if txt.strip():
        res=grade_prompt(txt,ptype)
        st.subheader(f"Score: {res['score']}")
        st.caption(f"Fingerprint: {res['hash']} • Category: {res['category']}")
        c1,c2=st.columns(2)
        with c1: st.json(res["constraints"])
        with c2: st.json({"Soft_terms":res["soft_terms"],"Contradictions":res["contradictions"]})
        fig,ax=plt.subplots(figsize=(4,2.6))
        ax.bar(["Constraints","Soft","Contradictions"],
               [sum(res["constraints"].values()),res["soft_terms"],res["contradictions"]],
               color=["#0a84ff","#ffffff","#666666"])
        ax.set_facecolor("#000000")
        ax.tick_params(colors="#ffffff")
        for s in ax.spines.values(): s.set_color("#ffffff")
        st.pyplot(fig,use_container_width=True)
        j,t=generate_report(res,txt)
        st.download_button("Download JSON",j,file_name="report.json")
        st.download_button("Download TXT",t,file_name="report.txt")
    else:
        st.error("Prompt cannot be empty.")
