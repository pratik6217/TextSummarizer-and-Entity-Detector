import streamlit as st
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import re
from spacy import displacy
from bs4 import BeautifulSoup 
import requests
nltk.download('punkt')
nltk.download('stopwords')
import heapq

HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25 rem; padding: 1rem;>{}</div>"""
nlp = spacy.load('en_core_web_sm')
options = ['Home', 'Summarizer', 'URL Summarizer', 'Named Entity Recognition', 'NER for URL']
choice  = st.sidebar.selectbox("Options:", options)

# @st.cache(allow_output_mutation = True, ignore_hash = True)
def summarizer(input_text):
    doc = nlp(input_text)
    tokens=[token.text for token in doc]
    word_frequencies={}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
    sentence_tokens= [sent for sent in doc.sents]

    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
    select_length = int(len(sentence_tokens))
    summary = nlargest(7, sentence_scores,key=sentence_scores.get)
    final_summary = [word.text for word in summary]
    summary = ''.join(final_summary)
    return summary
    
@st.cache(allow_output_mutation = True)
def analyze_text(input_text):
    nlp = spacy.load('en_core_web_sm')
    return nlp(input_text)

@st.cache(allow_output_mutation = True)
def get_text(url):
    page = requests.get(url).content
    soup = BeautifulSoup(page)
    fetched_text = " ".join(map(lambda p: p.text, soup.find_all('p')))
    return fetched_text

@st.cache(allow_output_mutation = True)
def summary(input_text):
    # Removing Square Brackets and Extra Spaces
    # input_text = re.sub(r'[[0-9]*]', ' ', input_text)
    # input_text = re.sub(r's+', ' ', input_text)

    # Removing special characters and digits
    # formatted_article_text = re.sub('[^a-zA-Z]', ' ', input_text )
    formatted_article_text = re.sub(r's+', ' ', input_text)

    sentence_list = nltk.sent_tokenize(input_text)
    stopwords = nltk.corpus.stopwords.words('english')
    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    maximum_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequency)

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary
    

if choice == 'Home':
    st.title("Welcome to Summarizer and Entity Recogniser.")
    st.write(" ")
    st.write("Natural language processing (NLP) refers to the branch of computer science—and more specifically, the branch of artificial intelligence or AI—concerned with giving computers the ability to understand text and spoken words in much the same way human beings can.")
    st.write("NLP combines computational linguistics—rule-based modeling of human language—with statistical, machine learning, and deep learning models. Together, these technologies enable computers to process human language in the form of text or voice data and to ‘understand’ its full meaning, complete with the speaker or writer’s intent and sentiment.")
    st.write("NLP drives computer programs that translate text from one language to another, respond to spoken commands, and summarize large volumes of text rapidly—even in real time. There’s a good chance you’ve interacted with NLP in the form of voice-operated GPS systems, digital assistants, speech-to-text dictation software, customer service chatbots, and other consumer conveniences. But NLP also plays a growing role in enterprise solutions that help streamline business operations, increase employee productivity, and simplify mission-critical business processes.")
    st.header("Summarizarion:")
    st.image("./1.png")
    st.write("Text Summarization involves condensing a piece of text into a shorter version, reducing the size of the original text while preserving key information and the meaning of the content. Since manual text synthesis is a long and generally laborious task, task automation is gaining in popularity and therefore a strong motivation for academic research.")
    st.header("Named Entity Recognition:")
    st.image("./2.png")
    st.write("Named entity recognition (NER) is an NLP based technique to identify mentions of rigid designators from text belonging to particular semantic types such as a person, location, organisation etc.")
    st.write("he term Named Entity was first proposed at the Message Understanding Conference (MUC-6) to identify names of organisations, people and geographic locations in the text, currency, time, and percentage expressions. Since then, there has been increasing interest in NER and Information Extraction (IE) techniques on text-based data for various scientific events.Today, NER is widely used across various fields and sectors to automate the information extraction process.")
    st.write("")
    
elif choice == "Summarizer":
    st.header("Summarizer")
    st.write(" ")
    st.write("Text Summarization involves condensing a piece of text into a shorter version, reducing the size of the original text while preserving key information and the meaning of the content. Since manual text synthesis is a long and generally laborious task, task automation is gaining in popularity and therefore a strong motivation for academic research.")
    # st.write("Generally, Text Summarization is classified into two main types: Extraction Approach and Abstraction Approach.")
    st.write("")
    inp = st.text_area("Summary", placeholder = "Please enter your paragraph here.....", height = 200)
    if st.button("Summarize"):
        if inp == "":
            st.error("Input box cannot be empty !")
        else:
            st.subheader("Original Text:")
            st.text_area("Original Text:", inp, height = 300)
            st.write(" ")
            s = summarizer(inp)
            st.text_area("Summarized Text:", s, height = 300)

elif choice == "URL Summarizer":
    inp = st.text_input("Summary", placeholder = "Please enter your paragraph here.....")
    # per = st.slider("Percentage", 0.1, 0.5)
    if st.button("Summarize"):
        if inp == "":
            st.error("Input box cannot be empty !")
        else:
            text = get_text(inp)
            st.text_area("Original Text:", text, height = 350)
            st.write(" ")
            s = summary(text)
            st.text_area("Summarized Text:", s, height = 300)

elif choice == "Named Entity Recognition":
    st.title("Named Entity Recognition with Spacy.")
    st.write("")
    inp = st.text_area("Type Text Here:", placeholder = "Type here...", height = 200)
    if st.button('detect'):
        if inp == "":
            st.error("Input Box cannot be empty !")
        else:
            doc = analyze_text(inp)
            html = displacy.render(doc, style = 'ent')
            html = html.replace("\n\n", "\n")
            st.markdown(html, unsafe_allow_html = True)

elif choice == "NER for URL":
    st.title("NER for URL")
    st.write(" ")
    st.write("")
    inp = st.text_input("Type URL Here:", placeholder = "Type here...")
    if st.button('detect'):
        if inp == "":
            st.error("Please enter a url !")
        else:
            text = get_text(inp)
            ner = nlp(text)
            se = [words.label_ for words in ner.ents]
            e = ""
            for words in set(se):
                e = e + (words + "  -->  " + spacy.explain(words)) + "\n"
            st.text_area("Explanation of Entities", e, height = 150)
            doc = analyze_text(text)
            html = displacy.render(doc, style = 'ent')
            html = html.replace("\n\n", "\n")
            st.write("")
            st.subheader("Entities Detected:")
            st.markdown(html, unsafe_allow_html = True)