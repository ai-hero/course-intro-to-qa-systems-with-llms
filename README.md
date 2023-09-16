# Intro to Q&A Systems with Large Language Models

# Setting Up Dependencies

```
source setup.sh
```

And when done,
```
deactivate
```

# Setting up environment variables
Create a `.env` file in this repo. Add yur keys and secrets to download your data there:
```
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
MLOPS_DATA_URL=
```

# Hello Milo
```
streamlit run introduction/hello_milo.py
```

# Course Proof-of-concept Prototype

The proof of concept prototype for the course is in the folder `poc/`:
1. First run the notebook [here](poc/explore.ipynb) to understand the code.
2. Then, run the PoC
    a. First download the data with `python poc/download_chats.py`.
    b. Then, build the index with the data pre-processing pipeline in `python poc/build_index.py`
    c. Run Milo assistant with `streamlit run poc/milo.py`
