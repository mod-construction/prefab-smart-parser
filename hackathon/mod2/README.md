# PDFtoDLM: Multi-File PDF to JSON Extraction Tool

[AEC Hackathon Munich](https://www.tum-venture-labs.de/events/aec-hackathon-munich-edition/) : [MOD Smart Prefab challenge](https://github.com/mod-construction/prefab-smart-parser), Team **MOD-2**.

Our goal is to extract structured data from unstructured PDFs containing information about prefabricated elements. The main challenge is to produce reliable results in JSON format, which can be used for further applications.

![](doc/img/agents.jpg)

The strategy we chose involves using two models acting as agents, based on [OpenAI](backend/openai) and [Claude](backend/claude) respectively, to improve each other's quality. One model generates the initial JSON based on the prompt request, while the other checks it and corrects any mistakes in the previous output.


There are some typical approaches for this challenge. Prompt engineering refers to designing effective prompts to instruct the LLM to complete the task. RAG applies semantic embedding to retrieve the relevant chunks of documents and the LLM then uses this retrieved content to generate answers that are more informed and accurate. Fine tuning aims to customize an LLM on a specific dataset to adjust its behavior or optimize it for specific tasks. In this project, we did not do fine tuning, instead, we tried a strategy called Verbal Reinforcement Learning, that is using feedback from human evaluators to iteratively improve how the LLM responds.

PDFtoDLM is composed of two [backends](./backend/README.md) for LLMs, a [frontend](frontend) user interface, and some additional [tools](./tools/README.md).

## **Features**
- Upload multiple PDF files via the web interface.
- Immediate visualization of each uploaded PDF.
- Asynchronous generation of structured JSON data from each PDF.
- Interactive JSON schema editor with live syntax highlighting.
- Options to save edited JSON and download it locally.

## **Tech Stack**

**OpenAI**

- **Frontend**: React.js
- **Backend**: Node.js with Express
- **PDF Parsing**: pdf-parse, pdf-lib
- **AI Integration**: OpenAI API

**Claude**

- Bash, [llm-claude-3](https://github.com/simonw/llm-claude-3)

## **Installation**

**OpenAI backend**

- **Node.js** (v14 or higher)
- **npm** or **yarn**
- OpenAI API Key (requires a valid API key from [OpenAI](https://platform.openai.com/))

**Claude backend**

- **Python**
- Claude API Key
- [Installation](backend/claude/README.md)


## Team

* [Jianpeng Cao](https://www.linkedin.com/in/jianpeng-cao-758511126/) (Kemp)
* [Milovann Yanatchkov](https://www.linkedin.com/in/milovann-yanatchkov/)
* [Olga Poletkina](https://www.linkedin.com/in/olga-poletkina-a6037098/)
* [Kaamil Ahmed Kaleem](https://www.linkedin.com/in/kaamil-ahmed-b20141141/)
* [Miguel Angel Montoya Gonzalez](https://www.linkedin.com/in/angel-montoya/)
* [Carmen Rubio Garcia](https://www.linkedin.com/in/carmen-rubio-garcia/)
* [Selin Yeltekin](https://www.linkedin.com/in/selinyeltekin/)
* [Yasmin Ragab](https://www.linkedin.com/in/yasmin-ragab-a3a9a910b/)
* [Yuxin Qiu](https://www.linkedin.com/in/yuxin-qiu-56a272211/)


