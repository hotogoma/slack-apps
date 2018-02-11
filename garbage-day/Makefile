AWS_PROFILE = default
FUNCTION = slack-garbage-day

.PHONY: default publish clean

default:

function.zip: main.py
	zip $@ $^

publish: function.zip
	aws --profile ${AWS_PROFILE} lambda update-function-code \
		--function-name ${FUNCTION} \
		--zip-file fileb://$<

clean: function.zip
	rm -f $^
