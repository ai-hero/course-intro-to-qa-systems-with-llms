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

# Optional Labs
# Hello Milo
A simple MLOps Q&A bot using OpenAI directly. Note: DOES NOT USE RETRIVAL-AUGMENTED GENERATION.
```
streamlit run introduction/hello_milo.py
```

# Q&A on Video
A Q&A that answers questions based on a video transcript. Note: DOES NOT USE RETRIVAL-AUGMENTED GENERATION.

This is one example of RAG, where the entire transcript is the retrieved context. Since transcripts are large,
we need a LLM with a large window - for this we use Anthropic's Claude.

Make sure you have your `ANTHROPIC_API_KEY` set in your `.env` file.

```
streamlit run video/video_milo.py
```
e.g. Use `https://www.youtube.com/watch?v=0e5q4zCBtBs` and questions about the panel discussion.

# Q&A from blog articles
Another example of RaG from blog data where we answer questions based on data on blugs that are publicly available.

a. First download the data with `python blog/download_blogs.py`.
b. Then, build the index with the data pre-processing pipeline in `python blog/build_index.py`
c. Run Milo assistant with `streamlit run blog/blog_milo.py`

You can also change the blog in `download_blogs.py`:
```
PAGES = [
    "https://mlops.community/building-the-future-with-llmops-the-main-challenges/",
]
```

NOTE: the html page contains a lot of data. This is where data cleanup comes in.
Feel free to clean up the data manually or with a script to see improved performance.
