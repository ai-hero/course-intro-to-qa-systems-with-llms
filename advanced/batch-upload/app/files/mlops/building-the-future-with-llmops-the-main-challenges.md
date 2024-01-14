Skip to content

[ MLOps Community ](/)

Menu

  * [Join](/join/)
  * [Learn](https://learn.mlops.community)
  * [Tools](/learn/)expand
    * [Feature Store](https://mlops.community/learn/feature-store/)
    * [Machine Learning Monitoring](https://mlops.community/learn/monitoring/)
    * [Metadata Storage and Management](https://mlops.community/learn/metadata-storage-and-management/)
  * [Blog](/blog/)
  * Eventsexpand
    * [In-person](/meetups/)
    * [Virtual](https://home.mlops.community/home/events)
  * [Newsletter](https://go.mlops.community/newsletter)
  * [Docs](https://mlops.notion.site/MLOps-Community-Orientation-e696c23ab1c74b97bfaa3d348a8eb499)

August 28, 2023

# Building the Future with LLMOps: The Main Challenges

![](https://mlops.community/wp-content/uploads/2023/08/pexels-google-
deepmind-17485608-scaled.jpg)

![](https://mlops.community/wp-
content/uploads/2023/08/8945f1f5-b0ed-4940-97cb-1ae33c617c2d.jpg)

[Andrew McMahon](https://mlops.community/author/andrew/)

Head of MLOps at NatWest Group (Parental Leave) | Author “Machine Learning
Engineering with Python”| Co-host AI Right Podcast | British Data Award Winner
2022 | Data Scientist of the Year 2019

[electricweegie.com/](https://electricweegie.com/)

[](https://www.linkedin.com/in/andrew-p-mcmahon/ "Linkedin")

  

_The following is an extract from[Andrew
McMahon](https://www.linkedin.com/in/andymcmahon629/)’s book, Machine Learning
Engineering with  
Python, Second Edition. Available on Amazon at <https://packt.link/w3JKL>._

![](https://mlops.community/wp-content/uploads/2023/08/image-4.png)

Given the rise in interest in LLMs recently, there has been no shortage of
people expressing the desire to integrate these models into all sorts of
software systems. For us as ML engineers, this should immediately trigger us
to ask the question, “What will that mean operationally?” As discussed
throughout this book, the marrying together of operations and development of
ML systems is termed MLOps. Working with LLMs is likely to lead to its own
interesting challenges, however, and so a new term, LLMOps, has arisen to give
this subfield of MLOps some good marketing. Is this really any different? I
don’t think it is that different but should be viewed as a sub-field of MLOps
with its own additional challenges. Some of the main challenges that I see in
this area are:

  * **Larger infrastructure** , even for fine-tuning: As discussed previously, these models are far too large for typical organizations or teams to consider training their own, so instead teams will have to leverage third-party models, be they open-source or proprietary, and fine-tune them. Fine-tuning models of this scale will still be very expensive and so there will be a higher premium on building very efficient data ingestion, preparation, and training pipelines.
  * **Model management is different** : When you train your own models, effective ML engineering requires us to define good practices for versioning our models and storing metadata that provide the lineage of the experiments and training runs we have gone through to produce these models. In a world where models are more often hosted externally, this is slightly harder to do, as we do not have access to the training data, to the core model artefacts, and probably not even to the detailed model architecture. Versioning metadata will then likely default to the publicly available metadata for the model, think along the lines of gpt-4-v1.3 and similar-sounding names. That is not a lot of information to go on, and so you will likely have to think of ways to enrich this metadata, perhaps with your own example runs and test results in order to understand how that model behaved in certain scenarios. This then also links to the next point.
  * **Rollbacks become more challenging** : If your model is hosted externally by a third party, you do not control the roadmap of that service. This means that if there is an issue with version 5 of a model and you want to roll back to version 4, that option might not be available to you. This is a different kind of “drift” from the model performance drift we’ve discussed at length in this book but it is going to become  
increasingly important. This will mean that you should have your own model,
perhaps with nowhere near the same level of functionality or scale, ready as a
last resort default to switch to in case of issues.

  * **Model performance is more of a challenge** : As mentioned in the previous point, with foundation models being served as externally hosted services, you are no longer in as much control as you were. This means that if you do detect any issues with the model you are consuming, be they drift or some other bugs, you are very limited in what you can do and you will need to consider that default rollback we just discussed.

  * **Applying your own guardrails will be key** : LLMs hallucinate, they get things wrong, they can regurgitate training data, and they might even inadvertently offend the person interacting with them. All of this means that as these models are adopted by more organizations, there will be a growing need to develop methods for applying bespoke guardrails to systems utilizing them. As an example, if an LLM was being  
used to power a next-generation chatbot, you could envisage that between the
LLM service and the chat interface, you could have a system layer that checked
for abrupt sentiment changes and important keywords or data that should be
obfuscated. This layer could utilize simpler ML models and a variety of other
techniques. At its most sophisticated, it could try and ensure that the
chatbot did not lead to a violation of ethical or other norms established by
the organization. If your organization has made the climate crisis an area of
focus, you may want to screen the conversation in real-time for information
that goes against critical scientific findings in this area as an example.

Since the era of foundation models has only just begun, it is likely that more
and more complex challenges will arise to keep us busy as ML engineers for a
long time to come. To me, this is one of the most exciting challenges we face
as a community, how we harness one of the most sophisticated and cutting-edge
capabilities ever developed by the ML community in a way that still allows the
software to run safely, efficiently, and robustly for users day in and day
out. Are you ready to take on that challenge?  
Let’s dive into some of these topics in a bit more detail, first with a
discussion of LLM validation.

## Validating LLMs

The validation of generative AI models is inherently different from and
seemingly more complex than the same for other ML models. The main reasons for
this are that when you are generating content, you are often creating very
complex data in your results that has never existed! If an LLM returns a
paragraph of generated text when asked to help summarize and analyze some
document, how do you determine if the answer is “good”? If you ask an LLM to
reformat some data into a table, how can you build a suitable metric that
captures if it has done this correctly? In a generative context, what does
“model performance”  
and “drift” really mean and how do I calculate them? Other questions may be
more use case dependent, for example, if you are building an information
retrieval or Retrieval-Augmented Generation (see Retrieval-Augmented
Generation for Knowledge-Intensive NLP Tasks,
<https://arxiv.org/pdf/2005.11401.pdf>) solution, how do you evaluate the
truthfulness of the text generated by the LLM?  
  
There are also important considerations around how we screen the LLM-generated
outputs for any potential biased or toxic outputs that may cause harm or
reputational damage to the organization running the model. The world of LLM
validation is complex!  
  
What can we do? Thankfully, this has not all happened in a vacuum and there
have been several benchmarking tools and datasets released that can help us on
our journey. Things are so young that there are not many worked examples of
these tools yet, but we will discuss the key points so that you are aware of
the landscape and can keep on top of how things are evolving. Let’s list some
of the higher-profile evaluation frameworks and datasets for LLMs:

● **OpenAI Evals** : This is a framework whereby OpenAI allows for the
crowdsourced development of tests against proposed text completions generated
by LLMs. The core concept at the heart of evals is the “Completion Function
Protocol,” which is a mechanism for standardizing the testing of the strings
returned when interacting with an LLM. The framework is available on GitHub at
<https://github.com/openai/evals>.  
● **Holistic Evaluation of Language Models (HELM)** : This project, from
Stanford University, styles itself as a “living benchmark” for LLM
performance. It gives you a wide variety of datasets, models, and metrics and
shows the performance across these different combinations. It is a very
powerful resource that you can use to base your own test scenarios on, or
indeed just to use the information directly to understand the risks and
potential benefits of using any specific LLM for your use case. The HELM
benchmarks are available at <https://crfm.stanford.edu/helm/latest/>.  
● **Guardrails AI** : This is a Python package that allows you to do
validation on LLM outputs in the same style as Pydantic, which is a very
powerful idea! You can also use it to build control flows with the LLM for
when issues arise like a response to a prompt not meeting your set criteria;
in this case, you can use Guardrails AI to re-prompt the LLM in the hope of
getting a different response. To use Guardrails AI, you specify a Reliable AI
Markup Language (RAIL) file that defines the prompt format and expected
behaviour in an XML-like file. Guardrails AI is available on GitHub at
<https://shreyar.github.io/guardrails/>.

There are several more of these frameworks being created all the time, but
getting familiar with the core concepts and datasets out there will become
increasingly important as more organizations want to take LLM-based systems
from fun proofs-of-concept to production solutions. In the penultimate section
of this chapter, we will briefly discuss some specific challenges I see around
the management of “prompts” when building LLM applications.

## PromptOps

When working with generative AI that takes text inputs, the data we input is
often referred to as “prompts” to capture the conversational origin of working
with these models and the concept that an input demands a response, the same
way a prompt from a person would. For simplicity, we will call any input data
that we feed to an LLM a prompt, whether this is in a user interface or via an
API call and irrespective of the nature of the content we provide to the LLM.  
  
Prompts are often quite different beasts from the data we typically feed into
an ML model. They can be effectively freeform, have a variety of lengths, and,
in most cases, express the intent for how we want the model to act. In other
ML modeling problems, we can certainly feed in unstructured textual data, but
this intent piece is missing. This all leads to some important considerations
for us as ML engineers working with these models.  
  
First, the shaping of prompts is important. The term prompt engineering has
become popular in the data community recently and refers to the fact that
there is often a lot of thought that goes into designing the content and
format of these prompts. This is something we need to bear in mind when
designing our ML systems with these models. We should be asking questions like
“Can I standardize the prompt formats for my application or use case?”, “Can I
provide appropriate additional formatting or content on top of what a user or
input system provides to get a better outcome?”, and similar questions. I will
stick with calling  
this prompt engineering.  
  
Secondly, prompts are not your typical ML input, and tracking and managing
them is a new, interesting challenge. This challenge is compounded by the fact
that the same prompt may give very different outputs for different models, or
even with different versions of the same model. We should think carefully
about tracking the lineage of our prompts and the outputs they generate. I
term this challenge as prompt management.  
  
Finally, we have a challenge that is not necessarily unique to prompts but
definitely becomes a more pertinent one if we allow users of a system to feed
in their own prompts, for example in chat interfaces. In this case, we need to
apply some sort of screening and obfuscation rules to data coming in and
coming out of the model to ensure that the model is not “jailbroken” in some
way to evade any guardrails. We would also want to guard against adversarial
attacks that may be designed to extract training data from these systems,
thereby gaining personally identifiable or other critical information that we
do not wish to be shared.  
  
As you begin to explore this brave new world of LLMOps with the rest of the
world, it will be important to keep these prompt-related challenges in mind.

## Take on the challenge!

Hopefully, the preceding paragraphs have convinced you that there are some
unique areas to explore when it comes to LLMOps and that this area is ripe for
innovation. These points barely scratch the surface of this rich new world but
I personally think they highlight that we do not have the answers yet. Are you
ready to help build the future?

## Author

  * ![Andrew McMahon](https://mlops.community/wp-content/uploads/2023/08/8945f1f5-b0ed-4940-97cb-1ae33c617c2d.jpg)

[Andrew McMahon](https://mlops.community/author/andrew/ "Andrew McMahon")

Head of MLOps at NatWest Group (Parental Leave) | Author “Machine Learning
Engineering with Python”| Co-host AI Right Podcast | British Data Award Winner
2022 | Data Scientist of the Year 2019

[ View all posts ](https://mlops.community/author/andrew/ "View all posts") [
](mailto:andrewpmcmahon629@gmail.com) [ ](https://electricweegie.com/)

###  
  
Related posts:

[ ![](https://mlops.community/wp-content/uploads/2022/02/model-
serve-150x150.png)Serve hundreds to thousands of ML models — Architectures
from Industry](https://mlops.community/serve-hundreds-to-thousands-of-ml-
models-architectures-from-industry/ "Serve hundreds to thousands of ML models
— Architectures from Industry") [ ![](https://mlops.community/wp-
content/uploads/2023/08/pexels-soly-moses-12334692-150x150.jpg)Explainable AI:
Visualizing Attention in Transformers](https://mlops.community/explainable-ai-
visualizing-attention-in-transformers/ "Explainable AI: Visualizing Attention
in Transformers") [ ![Monitoring](https://mlops.community/wp-
content/uploads/2022/11/pexels-pixabay-274895-150x150.jpg)Monitoring
Regression Models Without Ground-Truth](https://mlops.community/monitoring-
regression-models-without-ground-truth/ "Monitoring  Regression Models Without
Ground-Truth") [ ![](https://mlops.community/wp-
content/uploads/2023/04/pexels-karolina-grabowska-6769739-150x150.jpg)“It
worked when I prompted it” or the challenges of building an LLM
Product](https://mlops.community/it-worked-when-i-prompted-it-or-the-
challenges-of-building-an-llm-product/ "“It worked when I prompted it” or the
challenges of building an LLM Product") [ ![](https://mlops.community/wp-
content/uploads/2023/05/pexels-pixabay-237454-150x150.jpg)Fine Tuning vs.
Prompt Engineering Large Language Models](https://mlops.community/fine-tuning-
vs-prompt-engineering-llms/ "Fine Tuning vs. Prompt Engineering Large Language
Models")

Tags: [LLMOps](https://mlops.community/tag/llmops/),
[LLMs](https://mlops.community/tag/llms/),
[MLops](https://mlops.community/tag/mlops/)  

![MLOps Community](https://mlops.community/wp-
content/themes/mlops/assets/logos/logo-mlops-white.svg)

©2024 MLOps Community. All rights reserved unless states. Images provided by
[Unsplash.com](https://unsplash.com) and [pexels.com](https://pexels.com).
Made with ♥, tea and biscuits.

  * [Join](/join/)
  * [Learn](https://learn.mlops.community)
  * [Tools](/learn/)
  * [Blog](/blog/)
  * Events
  * [Newsletter](https://go.mlops.community/newsletter)
  * [Docs](https://mlops.notion.site/MLOps-Community-Orientation-e696c23ab1c74b97bfaa3d348a8eb499)

  * [Home](https://mlops.community/)
  * [Learn](https://mlops.community/learn/)
  * [Schedule](https://home.mlops.community/)
  * [Blog](https://mlops.community/blog/)

  * [Slack](https://go.mlops.community/slack)
  * [Youtube](https://go.mlops.community/youtube)
  * [Medium](https://go.mlops.community/medium)
  * [Twitter](https://go.mlops.community/twitter)
  * [Linkedin](https://go.mlops.community/linkedin)

©2024 MLOps Community. All rights reserved unless states. Images provided by
[Unsplash.com](https://unsplash.com) and [pexels.com](https://pexels.com).
Made with ♥, tea and biscuits.
