#!/bin/sh


set -ex
{

# cd $DT_ENV_DEVELOPER/src/duckietown-challenges-server && make bump-upload
# cd $DT_ENV_DEVELOPER/src/duckietown-challenges-server && make build-no-cache push
# cd $DT_ENV_DEVELOPER/src/duckietown-challenges-server && docker-compose down -v
# cd $DT_ENV_DEVELOPER/src/duckietown-challenges-server && docker-compose build --no-cache
# cd $DT_ENV_DEVELOPER/src/duckietown-challenges-server && docker-compose up -d


#cd $DT_ENV_DEVELOPER/aido/challenge-aido_LF && make define-challenge-LF
#cd $DT_ENV_DEVELOPER/aido/challenge-multistep && make define-challenge
#cd $DT_ENV_DEVELOPER/aido/challenge-prediction && make define-challenge
#cd $DT_ENV_DEVELOPER/aido/aido-robotarium-evaluation-form && make define-challenge



cd $DT_ENV_DEVELOPER/aido/challenge-aido_LF-template-pytorch  && dts challenges submit
cd $DT_ENV_DEVELOPER/aido/challenge-aido_LF-template-random  && dts challenges submit
cd $DT_ENV_DEVELOPER/aido/challenge-aido_LF-template-ros && dts challenges submit
cd $DT_ENV_DEVELOPER/aido/challenge-aido_LF-template-tensorflow  && dts challenges submit

#cd $DT_ENV_DEVELOPER/aido/challenge-aido_LF-baseline-IL-logs-tensorflow/imitation_agent  && dts challenges submit
cd $DT_ENV_DEVELOPER/aido/challenge-aido_LF-baseline-IL-sim-tensorflow/submission  && dts challenges submit
cd $DT_ENV_DEVELOPER/aido/challenge-aido_LF-baseline-RL-sim-pytorch  && dts challenges submit
cd $DT_ENV_DEVELOPER/aido/challenge-aido_LF-baseline-duckietown/submission  && dts challenges submit


}
