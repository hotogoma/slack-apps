AWS_PROFILE = default
FUNCTION = slack-koyomi

.PHONY: default publish clean

default:

packages:
	docker run \
		--rm \
		--platform linux/x86_64 \
		-v ${PWD}:/work \
		-w /work \
		python:3.12 \
			pip install -r requirements.txt -t ./packages

function.zip: main.py packages
	zip -r $@ $^

publish: function.zip
	aws --profile ${AWS_PROFILE} lambda update-function-code \
		--function-name ${FUNCTION} \
		--zip-file fileb://$<

clean:
	rm -rf packages function.zip