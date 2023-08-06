import os
os.system("pip install streamlit pyngrok")
from pyngrok import ngrok


def run(script="hello.py"):
    """ run the script and connect with ngrok"""
    url = ngrok.connect(8501)
    url = url.replace('http:', 'https:')
    print(url)
    os.system(f"streamlit run {script} &")


def stop():
    ngrok.kill()
    os.system("pkill streamlit")
