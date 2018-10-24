![CrowdAI-Logo](https://github.com/crowdAI/crowdai/raw/master/app/assets/images/misc/crowdai-logo-smile.svg?sanitize=true)
# marlo-multi-agent-starter-kit

[![gitter-badge](https://badges.gitter.im/Microsoft/malmo.png)](https://gitter.im/Microsoft/malmo)   

![FindTheGoal](https://media.giphy.com/media/1gWkQbDsHOfo4kZXZv/giphy.gif)

Instructions to participate in the second round of the [MarLo challenge](https://www.crowdai.org/challenges/marlo-2018). 

The task is to submit code which controls an *arbitrary* number of agents which can maximise the cumulative reward for all the agents in a series of N-agent environments in [MarLo](https://marlo.readthedocs.io).

Participants will have to submit their code, with packaging specifications, and the evaluator will automatically build a docker image and execute their agent against different instantiations of multiple N-agent environments across three tasks.

### Setup
* **docker** : By following the instructions [here](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
* **nvidia-docker** : By following the instructions [here](https://github.com/nvidia/nvidia-docker/wiki/Installation-(version-2.0))
* **repo2docker**
```sh
pip install crowdai-repo2docker
```
* **Anaconda** (By following instructions [here](https://www.anaconda.com/download)) 
* **malmo and marlo**
```sh 
conda create python=3.6 --name marlo
conda config --add channels conda-forge
conda activate marlo # or `source activate marlo` depending on your conda version
conda install -c crowdai malmo
pip install -U marlo

# Test installation by :
python -c "import marlo"
python -c "from marlo import MalmoPython"
```
* **Your code specific dependencies**
```sh
# If say you want to install PyTorch
conda install pytorch torchvision -c pytorch
```

### Clone repository 
```
git clone git@github.com:crowdAI/marlo-multi-agent-starter-kit.git
cd marlo-multi-agent-starter-kit
```

### Build Docker Image locally 
```
cd marlo-multi-agent-starter-kit

# The following are the contents of the ./build.sh file
# Hence you can alternatively call ./build.sh for the same effect.

export IMAGE_NAME="marlo_random_agents"

crowdai-repo2docker --no-run \
  --user-id 1001 \
  --user-name crowdai \
  --image-name ${IMAGE_NAME} \
  --debug .
```
This should take some time, but it will build a docker image out of the this repository

### Test Submission Locally
Assuming you have docker and the rest of the dependencies installed..
```
cd marlo-multi-agent-starter-kit
# The following are the contents of the ./test_submission_locally.sh file
# Hence you can alternatively call ./test_submission_locally.sh for the same effect.

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
```

## Important Concepts

### Repository Structure
* `crowdai.json`
  Each repository should have a `crowdai.json` with the following content : 
```json
{
  "challenge_id" : "crowdai-marLo-2018",
  "grader_id" : "crowdai-marLo-2018-multi",
  "authors" : ["your-crowdai-username"],
  "description" : "sample description about your awesome marlo agent",
  "license" : "MIT",
  "gpu":false
}
```
This is used to map your submission to the said challenge, so please remember to use the correct `challenge_id` and `grader_id` as specified above.

Please specify if your code will require GPU or not for the evaluation of your model. If you specify `true` for the GPU, then `N` number of GPUs will be made available if your code is expected to control `N` agents.

### Packaging of your software environment
You can specify your software environment by using all the [available configuration options of repo2docker](https://repo2docker.readthedocs.io/en/latest/config_files.html). (But please remember to use [crowdai-repo2docker](https://pypi.org/project/crowdai-repo2docker/) to have GPU support)   

The recommended way is to use Anaconda configuration files using **environment.yml** files.

```sh 
# The included environment.yml is generated by the command below, and you do not need to run it again 
# if you did not add any custom dependencies

conda env export --no-build > environment.yml

# Note the `--no-build` flag, which is important if you want your anaconda env to be replicable across all 
```

### Debugging the packaged software environment

If you have issues with your submission because of your software environment and dependencies, you can debug them, by first building the docker image, and then getting a shell inside the image by : 
```
docker run --net=host -it $IMAGE_NAME /bin/bash 
```
and then exploring to find the cause of the issue.

### Code Entrypoint
The evaluator will use `/home/crowdai/run.sh` as the entrypoint, so please remember to have a `run.sh` at the root, which can instantitate any necessary environment variables, and also start executing your actual code. This repository includes a sample `run.sh` file.
If you are using a Dockerfile to specify your software environment, please remember to create a `crowdai` user, and place the entrypoint code at `run.sh`.

## Submission 
To make a submission, you will have to create a private repository on [https://gitlab.crowdai.org](https://gitlab.crowdai.org).

You will have to add your SSH Keys to your GitLab account by following the instructions [here](https://docs.gitlab.com/ee/gitlab-basics/create-your-ssh-keys.html).
If you do not have SSH Keys, you will first need to [generate one](https://docs.gitlab.com/ee/ssh/README.html#generating-a-new-ssh-key-pair).

Then you can create a submission by making a *tag push* to your repository on [https://gitlab.crowdai.org](https://gitlab.crowdai.org). **Any tag push to your private repository is considered as a submission**   
Then you can add the correct git remote, and finally submit by doing : 

```
cd marlo-multi-agent-starter-kit
# Add crowdAI git remote endpoint
git remote add crowdai git@gitlab.crowdai.org:<YOUR_CROWDAI_USER_NAME>/marlo-multi-agent-starter-kit.git
git push crowdai master

# Create a tag for your submission and push
git tag -am "v0.1" v0.1
git push crowdai master
git push crowdai v0.1

# Note : If the contents of your repository (latest commit hash) does not change, 
# then pushing a new tag will not trigger a new evaluation.
```
You now should be able to see the details of your submission at : 
[gitlab.crowdai.org/<YOUR_CROWDAI_USER_NAME>/marlo-multi-agent-starter-kit/issues](gitlab.crowdai.org/<YOUR_CROWDAI_USER_NAME>/marlo-single-agent-starter-kit/issues)

**NOTE**: Remember to update your username in the link above :wink:

In the link above, you should start seeing something like this take shape (each of the steps can take a bit of time, so please be patient too :wink: ) : 
![](https://i.imgur.com/vucYbwy.png)

and if everything works out correctly, then you should be able to see the final scores like this : 
![](https://i.imgur.com/QkoGOwv.png)

**Best of Luck** :tada: :tada:

# Author
Sharada Mohanty <https://twitter.com/MeMohanty>
