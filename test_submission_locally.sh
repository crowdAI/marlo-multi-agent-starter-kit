#!/bin/bash 

########################################################################
# This script tests the submission locally by mimicking (to some extent)
# what happens on the evaluation serber
########################################################################

export IMAGE_NAME="marlo_random_agents"

# Build Image from the repository
./build.sh

# Ensure you have a Minecraft Clients running on port 10000 and 10001
# by doing : 
#    $MALMO_MINECRAFT_ROOT/launchClient.sh -port 10000
# and 
#    $MALMO_MINECRAFT_ROOT/launchClient.sh -port 10001

docker run --net=host -it $IMAGE_NAME /home/crowdai/run.sh

# Now if everything works out well, then you should see the agents inside
# the docker container interacting with the minecraft clients on your host.
