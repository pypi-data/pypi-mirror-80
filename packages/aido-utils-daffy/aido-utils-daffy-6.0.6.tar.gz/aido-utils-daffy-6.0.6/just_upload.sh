#!/bin/zsh
hash -d ZE=/Volumes/work/zupermind/env
hash -d dt-env=${DT_ENV_DEVELOPER}
hash -d src=~dt-env/src

cd ~ZE/zuper-commons && make upload
cd ~ZE/zuper-typing && make upload
cd ~src/duckietown-challenges && make upload
cd ~src/duckietown-tokens && make upload
cd ~src/duckietown-challenges-runner && make upload build push
cd ~ZE/zuper-ipce && make upload
cd ~ZE/zuper-nodes && make upload
cd ~ZE/zuper-nodes-python2 && make upload
cd ~ZE/zuper-auth && make upload
cd ~src/aido-protocols && make upload
cd ~src/aido-analyze && make upload
cd ~src/aido-agents && make upload
cd ~src/duckietown-serialization && make upload
cd ~src/duckietown-world && make upload # ests-clean tests
cd ~src/gym-duckietown && make upload
cd ~src/duckietown-challenges-server && make upload
