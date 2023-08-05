
minimal: LF-submit-minimal LF-submit-minimal2


define-challenge:
	cd $(DT_ENV_DEVELOPER)/src/aido-base-python3  &&  make build push
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-scenario_maker &&  make build push
	cd $(DT_ENV_DEVELOPER)/src/gym-duckietown  &&  make build push
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-simulator-gym  &&  make build push
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF &&  make define-challenge


baselines:
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-baseline-IL-logs-tensorflow &&  make submit-bea
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-baseline-IL-sim-tensorflow &&  make submit-bea
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-baseline-RL-sim-pytorch &&  make submit-bea
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-baseline-duckietown &&  make submit-bea
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-minimal-agent &&  make submit-bea
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-template-pytorch &&  make submit-bea
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-template-random &&  make submit-bea
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-template-ros &&  make submit-bea
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-template-tensorflow &&  make submit-bea

	# cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-minimal-agent-full &&  make submit-bea
	# cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-duckiebot-bridge


	# XXX cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-baseline-IL-logs-tensorflow/imitation_agent  && make submit-bea
#	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-baseline-IL-sim-tensorflow/submission  &&  make submit-bea
#	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-baseline-RL-sim-pytorch  && make submit-bea
#	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-baseline-duckietown/submission  &&make submit-bea
#	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-template-pytorch  && make submit-bea
#	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-template-random  && make submit-bea
#	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-template-ros && make submit-bea
#	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-template-tensorflow  && make submit-bea


alldefine: define-LF define-multistep define-prediction define-robotarium

define-LF:
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF && make define-challenge

define-multistep:
	cd $(DT_ENV_DEVELOPER)/aido/challenge-multistep && make define-challenge

define-prediction:
	cd $(DT_ENV_DEVELOPER)/aido/challenge-prediction && make define-challenge

define-robotarium:
	cd $(DT_ENV_DEVELOPER)/aido/aido-robotarium-evaluation-form && make define-challenge

update-versions:
	python3 -m duckietown_challenges_server.aido_change_versions $(DT_ENV_DEVELOPER)/aido $(DT_ENV_DEVELOPER)/src

check-versions:
	python3 -m duckietown_challenges_server.aido_check_containers

build: build-runner build-protocols build-gym build-duckiebot build-server build-pytorch

build-runner:
	cd $(DT_ENV_DEVELOPER)/src/duckietown-challenges-runner && make build push

build-protocols:
	cd $(DT_ENV_DEVELOPER)/src/aido-protocols     && make build-base-images push-base-images

build-gym:
	cd $(DT_ENV_DEVELOPER)/src/gym-duckietown     && make build-docker-python3 push-docker-python3

build-duckiebot:
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF/duckiebot && make build  push

build-server:
	cd $(DT_ENV_DEVELOPER)/src/duckietown-challenges-server && make build push

build-pytorch:
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-template-pytorch  && make build push


build-pytorch:
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-template-pytorch  && make build push


bump:
	bumpversion --verbose patch
	git push --tags
	git push --all

upload:
	rm -f dist/*
	rm -rf src/*.egg-info
	python setup.py sdist
	twine upload --verbose dist/*

bump-upload:
	$(MAKE) bump
	$(MAKE) upload
