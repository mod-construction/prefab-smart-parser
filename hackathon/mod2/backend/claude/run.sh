#!/bin/bash

what=$1
model=""
use_pdftotext=yes

help()
{
	echo "?"
}

openapi()
{
	k=$(cat .openapi)
	if [[ $key == "" ]] 
	then
		echo "no file ..."
		return
	fi

	export OPENAI_API_KEY=$k
	model=""
	file="buro-containers.pdf"
	extract
}

init_claude_key()
{
	local keyfile=".claude_key"
	if [[ ! -f $keyfile ]]
	then
		echo "Can't find $keyfile"
		return
	fi
	local key=$(cat $keyfile)
	export ANTHROPIC_API_KEY=$key
}

claude()
{
	model="-m claude-3.5-sonnet"
	extract
}

panels()
{
	file="insulated-panels.pdf"
	model="-m claude-3.5-sonnet"	
	init_claude_key
	extract
}

containers()
{
	file="buro-containers.pdf"
	model="-m claude-3.5-sonnet"
	init_claude_key
	extract
}

extract()
{
	if [[ $file == "" ]]
	then
		file=$(cat .file)
		if [[ $key == "" ]] 
		then
			echo "no file ..."
			return
		fi
	fi

	if [[ $use_pdftotext ]]
	then
		echo "[*] Using pdftotext from $file"
		pdftotext data/$file output.txt
	else

		echo "[*] Extracting data from $file"
		poetry run llm $model 'extract text' -a data/$file > output.txt
	fi

	cp output.txt tmp/$file-output.txt

	echo "[*] Producing Json "
	cat output.txt | poetry run llm $model -s "Extract the keypoints of this document and produce a JSON file without any further comments" > data.json
	cp data.json tmp/$file-raw.json

	echo "[*] Producing instructions "
	echo "DOCUMENT 1 : The JSON OBJECT" > instruct.txt
	cat data.json >> instruct.txt
	echo "DOCUMENT 2 : The JSON DATA MODEL" >> instruct.txt
	cat openapi.json >> instruct.txt

	echo "[*] Producing data model "
	cat instruct.txt | poetry run llm $model -s "Make a JSON file from the data contained in DOCUMENT 1 JSON OBJECT based on the DOCUMENT 2 JSON DATA MODEL. Just output a JSON file without any further comments" > result.json
	cp result.json tmp/$file.json

	echo "[*] Done"
}

exe()
{
	if [[ $what == "" ]]
	then
		help
		return
	fi

	if [[ ! -f .key ]]
	then
		echo "add api key in a .key file"
		return
	fi

	key=$(cat .key)
	export ANTHROPIC_API_KEY=$key

	case $what in
		claude) claude ;;
		openapi) openapi ;;
		insulated-panels) panels ;;
		containers) containers ;;
		*) echo "?";;
	esac



}

exe "$@"
