# Claude backend

Testing Claude API with [llm-claude-3](https://github.com/simonw/llm-claude-3) Python package

## Install

* Install Poetry

`pip install poetry`

* Install dependencies

`make install`

* Add your API key in a `.claude_key` file

## Run 

Run a test with [Buro conainters PDF](https://www.conzept.com/files/inhalte/container/buerocontainer/inhalt/technische-beschreibung/buerocontainer-technische-beschreibung.pdf)
  

`make containers`

## Prompting

See [Makefile](Makefile) for details

* Extract data from Pdf

`make extract-pdf `

* Generate a Json file from the data

`make output-json`

* Instruct the LLM with both data and model json file

`make create-instructions`

* Generate model object

`make generate-model-data`


## First results

* [1.json](results/1.json) from [this file](https://drive.google.com/file/d/1STAh85Z6r1DoObr9W8Re1pNnCZRXH4Dt/view?usp=drive_link)
* [2.json](results/2.json) from [this file](https://drive.google.com/file/d/1Ssb9eAlNsvaw10N0sNMx-dQDXW5MahEz/view?usp=sharing)
* [3.json](results/3.json) from [this file](https://drive.google.com/drive/folders/19LgBolM8rnz2p3_qOhbqIcsMwOG_md96)


* [buro-container-raw-data.json](results/buro-container-raw-data.json) from [this file](https://www.conzept.com/files/inhalte/container/buerocontainer/inhalt/technische-beschreibung/buerocontainer-technische-beschreibung.pdf)
* [buro-container.json](results/buro-container.json) from [this file](https://www.conzept.com/files/inhalte/container/buerocontainer/inhalt/technische-beschreibung/buerocontainer-technische-beschreibung.pdf)




