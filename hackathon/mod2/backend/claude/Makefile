install:
	poetry install

claude:
	./run.sh claude

openapi:
	./run.sh openapi

insulated-panels:
	./run.sh insulated-panels

containers:
	./run.sh containers

test:
	poetry run llm -m claude-3.5-sonnet "what is LLM ?"
extract-pdf:
	poetry run llm -m claude-3.5-sonnet 'extract text' -a data/2.pdf > output.txt
output-json:
	cat output.txt | poetry run llm -m claude-3.5-sonnet -s "Extract the keypoints of this document and produce a JSON file without any further comments" > data.json

create-instructions:
	echo "DOCUMENT 1 : The JSON OBJECT" > instruct.txt
	cat data.json >> instruct.txt
	echo "DOCUMENT 2 : The JSON DATA MODEL" >> instruct.txt
	cat openapi.json >> instruct.txt

generate-model-data:
	cat instruct.txt | poetry run llm -m claude-3.5-sonnet -s "Make a JSON file from the data contained in DOCUMENT 1 JSON OBJECT based on the DOCUMENT 2 JSON DATA MODEL. Just output a JSON file without any further comments" > result.json


