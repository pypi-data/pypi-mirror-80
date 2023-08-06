all:

.PHONY: ci build define-challenges templates baselines

aido: ci build define-challenges templates baselines


bases: lib-duckietown-challenges lib-duckietown-challenges-runner lib-duckietown-tokens lib-aido-protocols
	$(MAKE) -C $(DT_ENV_DEVELOPER)/src/aido-base-python3 build push


ci: bases
	$(MAKE) -C $(DT_ENV_DEVELOPER)/aido/aido-submission-ci-test build push

templates:  \
	template-pytorch \
	template-random \
	template-ros \
	template-tensorflow

template-pytorch: bases
	$(MAKE) -C $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-template-pytorch build push submit-bea

template-random: bases
	$(MAKE) -C $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-template-random build push  submit-bea

template-ros: bases
	$(MAKE) -C $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-template-ros build push submit-bea

template-tensorflow: bases
	$(MAKE) -C $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-template-tensorflow build push  submit-bea

baselines: \
	baseline-tensorflow-IL-logs \
	baseline-tensorflow-IL-sim \
	baseline-pytorch \
	baseline-duckietown \
	baseline-minimal-agent \
	baseline-minimal-agent-full \
	baseline-JBR


baseline-tensorflow-IL-logs: bases template-tensorflow
	$(MAKE) -C $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-baseline-IL-logs-tensorflow submit-bea

baseline-tensorflow-IL-sim: bases template-tensorflow
	$(MAKE) -C $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-baseline-IL-sim-tensorflow  submit-bea

baseline-pytorch: bases template-pytorch
	$(MAKE) -C $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-baseline-RL-sim-pytorch  submit-bea

baseline-JBR: bases
	$(MAKE) -C $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-baseline-JBR  submit-bea

baseline-duckietown: bases
	$(MAKE) -C $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-baseline-duckietown  submit-bea

baseline-minimal-agent: bases lib-aido-analyze lib-aido-agents
	$(MAKE) -C $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-minimal-agent  submit-bea

baseline-minimal-agent-full: bases  lib-aido-analyze lib-aido-agents
	$(MAKE) -C $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-minimal-agent  submit-bea

other:
	$(MAKE) -C $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-minimal-agent-full submit-bea


define-challenges: define-LF define-multistep define-prediction define-robotarium

define-LF: build-scenario-maker  build-simulator-gym  build-experiment_manager
	$(MAKE) -C $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF define-challenge-parallel

build-scenario-maker: bases lib-duckietown-world
	$(MAKE) -C $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-scenario_maker build push

build-gym-duckietown: bases
	$(MAKE) -C $(DT_ENV_DEVELOPER)/src/gym-duckietown build push

build-simulator-gym: build-gym-duckietown lib-duckietown-gym
	$(MAKE) -C $(DT_ENV_DEVELOPER)/aido/challenge-aido_LF-simulator-gym build push

define-multistep:
	$(MAKE) -C $(DT_ENV_DEVELOPER)/aido/challenge-multistep define-challenge

define-prediction:
	$(MAKE) -C $(DT_ENV_DEVELOPER)/aido/challenge-prediction define-challenge

define-robotarium:
	$(MAKE) -C $(DT_ENV_DEVELOPER)/aido/aido-robotarium-evaluation-form define-challenge


build: \
	build-runner \
	build-gym-duckietown \
	build-scenario-maker \
	build-simulator-gym \
	build-mooc-fifos-connector\
	build-aido-submission-ci-test\
	build-experiment_manager

	# build-server


build-experiment_manager: bases
	$(MAKE) -C $(DT_ENV_DEVELOPER)/src/challenge-aido_LF-experiment_manager  build push


build-aido-submission-ci-test: bases
	$(MAKE) -C $(DT_ENV_DEVELOPER)/src/build-aido-submission-ci-test  build push

build-mooc-fifos-connector: bases
	$(MAKE) -C $(DT_ENV_DEVELOPER)/src/mooc-fifos-connector  build push

build-runner: bases lib-duckietown-challenges lib-duckietown-challenges-runner lib-duckietown-tokens
	$(MAKE) -C $(DT_ENV_DEVELOPER)/src/duckietown-challenges-runner build push
#
#build-server:
#	$(MAKE) -C $(DT_ENV_DEVELOPER)/src/duckietown-challenges-server build push

libs: \
	lib-aido-utils \
	lib-aido-agents \
	lib-aido-analyze \
	lib-aido-protocols \
	lib-duckietown-gym \
	lib-duckietown-world \
	lib-duckietown-challenges \
	lib-duckietown-challenges-runner \
	lib-duckietown-tokens

lib-aido-utils:
	$(MAKE) -C $(DT_ENV_DEVELOPER)/src/aido-utils  upload

lib-aido-agents:
	$(MAKE) -C $(DT_ENV_DEVELOPER)/src/aido-agents upload

lib-aido-analyze:
	$(MAKE) -C $(DT_ENV_DEVELOPER)/src/aido-analyze upload

lib-aido-protocols:
	$(MAKE) -C $(DT_ENV_DEVELOPER)/src/aido-protocols upload

lib-duckietown-gym:
	$(MAKE) -C $(DT_ENV_DEVELOPER)/src/gym-duckietown upload

lib-duckietown-world:
	$(MAKE) -C $(DT_ENV_DEVELOPER)/src/duckietown-world upload

lib-duckietown-challenges:
	$(MAKE) -C $(DT_ENV_DEVELOPER)/src/duckietown-challenges upload

lib-duckietown-challenges-runner:
	$(MAKE) -C $(DT_ENV_DEVELOPER)/src/duckietown-challenges-runner upload

lib-duckietown-tokens:
	$(MAKE) -C $(DT_ENV_DEVELOPER)/src/duckietown-tokens upload

build-challenges-runner: lib-duckietown-challenges
	$(MAKE) -C $(DT_ENV_DEVELOPER)/src/gym-duckietown build push

mooc: mooc-fifos-connector

mooc-fifos-connector: base
	$(MAKE) -C $(DT_ENV_DEVELOPER)/src/mooc-fifos-connector build push

update-baselines-circleci:
	./update-circleci-baselines.sh
