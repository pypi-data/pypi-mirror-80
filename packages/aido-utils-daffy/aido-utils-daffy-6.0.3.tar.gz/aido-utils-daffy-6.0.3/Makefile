
minimal: LF-submit-minimal LF-submit-minimal2

LF-submit-minimal:
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF/minimal_agent && dts challenges submit

LF-submit-minimal2:
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF/minimal_agent_python2 && dts challenges submit

multistep-submit:
	cd $(DT_ENV_DEVELOPER)/aido/challenge-multistep/submission && dts challenges submit

prediction-submit:
	cd $(DT_ENV_DEVELOPER)/aido/challenge-prediction/predictor_mean && dts challenges submit

baselines:
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-baseline-IL-logs-tensorflow/imitation_agent  && dts challenges submit
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-baseline-IL-sim-tensorflow/submission  && dts challenges submit
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-baseline-RL-sim-pytorch  && dts challenges submit
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-baseline-duckietown/submission  && dts challenges submit
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-template-pytorch  && dts challenges submit
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-template-random  && dts challenges submit
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-template-ros && dts challenges submit
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-template-tensorflow  && dts challenges submit

alldefine: define-LF define-multistep define-prediction define-robotarium

define-LF:
	cd $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF && make define-challenge-LF

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
