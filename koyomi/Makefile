AWS_PROFILE = default
FUNCTION = slack-koyomi

.PHONY: default publish clean

default:

packages:
	docker run --rm -v ${PWD}:/work -w /work python:3.6 \
		pip install -r requirements.txt -t ./packages

function.zip: main.py packages
	zip -r $@ $^

publish: function.zip
	aws --profile ${AWS_PROFILE} lambda update-function-code \
		--function-name ${FUNCTION} \
		--zip-file fileb://$<

clean: function.zip
	rm -f $^
