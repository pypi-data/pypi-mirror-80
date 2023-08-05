#!/bin/sh


set -ex
{
python3 -m duckietown_challenges_server.aido_change_versions $DT_ENV_DEVELOPER/aido $DT_ENV_DEVELOPER/src

cd $DT_ENV_DEVELOPER/src/duckietown-challenges-runner && make build push

cd $DT_ENV_DEVELOPER/src/aido-protocols     && make build-base-images push-base-images
cd $DT_ENV_DEVELOPER/src/gym-duckietown     && make build-docker-python3 push-docker-python3
cd $DT_ENV_DEVELOPER/aido/challenge-aido_LF/duckiebot && make build  push

cd $DT_ENV_DEVELOPER/aido/challenge-aido_LF-template-pytorch  && make build push
cd $DT_ENV_DEVELOPER/aido/challenge-aido_LF-template-ros  && make build push

# cd $DT_ENV_DEVELOPER/src/duckietown-challenges-server && make bump-upload
# cd $DT_ENV_DEVELOPER/src/duckietown-challenges-server && make build-no-cache push
# cd $DT_ENV_DEVELOPER/src/duckietown-challenges-server && docker-compose down -v
# cd $DT_ENV_DEVELOPER/src/duckietown-challenges-server && docker-compose build --no-cache
# cd $DT_ENV_DEVELOPER/src/duckietown-challenges-server && docker-compose up -d


cd $DT_ENV_DEVELOPER/aido/challenge-aido_LF && make define-challenge-LF
cd $DT_ENV_DEVELOPER/aido/challenge-multistep && make define-challenge
cd $DT_ENV_DEVELOPER/aido/challenge-prediction && make define-challenge


cd $DT_ENV_DEVELOPER/aido/aido-robotarium-evaluation-form && make define-challenge

#
# # challenge_aido_LF
# #???? duckiebot bridge
# pip list | grep zuper
# docker run -it --rm duckietown/aido3-base-python3:daffy pip3 list | grep zuper

python3 -m duckietown_challenges_server.aido_check_containers
}
