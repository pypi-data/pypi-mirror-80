#!/bin/zsh
#source ~/.zshrc # NO  ! this resets the PIP_INDEX-URL
hash -d ZE=/Volumes/work/zupermind/env
hash -d dt-env=${DT_ENV_DEVELOPER}
hash -d src=~dt-env/src
hash -d aido=~dt-env/aido

# https://stefan.sofa-rockers.org/2017/11/09/getting-started-with-devpi/
# devpi-server --serverdir=/tmp/devpi --init
# devpi-server --serverdir=/tmp/devpi --passwd root  # pwd="paperone"
# devpi-server --serverdir=/tmp/devpi --restrict-modify=root --host 0.0.0.0 --start
#  devpi use https://staging.duckietown.org
# devpi login root # pwd="paperone"
# devpi index -c root/devel bases=root/pypi volatile=True
# keyring set ${PIP_INDEX_URL} root
# cloudflared --hostname staging2.duckietown.org http://localhost:8443

# variables
# export PIP_TRUSTED_HOST=staging.duckietown.org
#
#export TWINE_REPOSITORY_URL=https://staging.duckietown.org/root/devel/
#export PIP_INDEX_URL=https://staging.duckietown.org/root/devel/
#export TWINE_USERNAME=root
#export AIDO_REGISTRY=staging-registry.duckietown.org:9443
alias real-world="env -u TWINE_USERNAME -u AIDO_REGISTRY -u TWINE_REPOSITORY_URL -u PIP_INDEX_URL"

alias doifchange="python -m duckietown_challenges_server.doifchange"

#cd ~src/duckietown-challenges-server && docker-compose -f docker-compose.registry.yml up -d

# if it has a version tag
# update requirements
# commit
# retag with same
# push

# Reset the DB
#   docker-compose down -v
#   docker-compose up mysql

# cd ~src/duckietown-shell             && make bump-upload
# cd ~src/duckietown-shell-commands    && make bump-upload
set -x
set -euo pipefail

#doifchange ~ZE/zuper-commons echo 1
#doifchange ~ZE/zuper-typing echo 1
#doifchange ~src/duckietown-challenges echo 1
#doifchange ~src/duckietown-tokens echo 1
#doifchange ~src/duckietown-challenges-runner echo 1
#doifchange ~ZE/zuper-ipce  echo 1
#doifchange ~ZE/zuper-nodes echo 1
#doifchange ~ZE/zuper-nodes-python2 echo 1
#doifchange ~ZE/zuper-auth echo 1
#doifchange ~src/aido-protocols echo 1
#doifchange ~src/duckietown-serialization echo 1
#doifchange ~src/duckietown-world  echo 1
#doifchange ~src/gym-duckietown echo 1
#doifchange ~src/duckietown-challenges-server echo 1

doifchange ~ZE/zuper-commons make bump-upload
doifchange ~ZE/zuper-typing make bump-upload
#
doifchange ~src/duckietown-challenges make bump-upload
doifchange ~src/duckietown-tokens make bump-upload

doifchange ~src/duckietown-challenges-runner make bump-upload build push

doifchange ~ZE/zuper-ipce make bump-upload
doifchange ~ZE/zuper-nodes make bump-upload
doifchange ~ZE/zuper-nodes-python2 make bump-upload

doifchange ~ZE/zuper-auth make bump-upload
doifchange ~src/aido-protocols make bump-upload
doifchange ~src/aido-utils make bump-upload
doifchange ~src/aido-analyze make bump-upload
doifchange ~src/aido-agents make bump-upload
doifchange ~src/duckietown-serialization make bump-upload
doifchange ~src/duckietown-world make bump-upload # ests-clean tests

doifchange ~src/gym-duckietown make bump-upload

# cd ~src/duckietown-challenges-server && docker-compose up -d registry

cd ~src/gym-duckietown && make build-docker-python3 push-docker-python3

cd ~src/aido-base-python3 && make build push

cd ~aido/challenge-aido_LF-duckiebot-bridge && make build push

doifchange ~src/duckietown-challenges-server make bump-upload
# need the build so that the deps will adjust
cd ~src/duckietown-challenges-server && make build #push

#cd ~src/duckietown-challenges-server && docker-compose -f docker-compose.ac.yml down -v || true
#cd ~src/duckietown-challenges-server && docker-compose -f docker-compose.ac.yml up -d --build
##echo ""
#echo "Waiting 60 seconds for the server to come up"
#sleep 30
#echo ""
cd ~aido/challenge-aido_LF-minimal-agent-full && make build push
cd ~aido/challenge-aido_LF-scenario_maker && make build push
cd ~aido/challenge-aido_LF-simulator-gym && make build push # need push
#cd ~aido/challenge-aido_LF && make define-challenge
cd ~aido/challenge-aido_LF && make define-challenge-LFV2
cd ~aido/challenge-aido_LF-minimal-agent && make submit-bea
cd ~aido/challenge-aido_LF-minimal-agent-full && make submit-bea

cd ~aido/challenge-aido_LF-minimal-agent-python2 && make submit-bea
cd ~aido/challenge-aido_LF-baseline-duckietown/3_submit && make submit-bea
cd ~aido/challenge-aido_LF-baseline-IL-sim-tensorflow/submission && make submit-bea
cd ~aido/challenge-aido_LF-baseline-RL-sim-pytorch &&  make submit-bea

cd ~aido/challenge-multistep && make define-challenge
#cd ~aido/challenge-multistep/submission && make submit-bea

cd ~aido/challenge-prediction && make define-challenge
#cd ~aido/challenge-prediction/predictor_mean && make submit-bea


#cd ~aido/aido-robotarium-evaluation-form && make define-challenge-no-cache

# cd ~aido/challenge-aido_LF-baseline-IL-logs-tensorflow/imitation_agent && make submit-bea

#cd ~aido/challenge-aido_LF-template-pytorch && dts challenges submit --no-cache
#cd ~aido/challenge-aido_LF-template-random && dts challenges submit --no-cache
#cd ~aido/challenge-aido_LF-template-ros && dts challenges submit --no-cache
#cd ~aido/challenge-aido_LF-template-tensorflow && dts challenges submit --no-cache
