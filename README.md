sentience
=========

So far nobody has linked together the available building blocks for artificial general intelligence (AGI). These tools include Differentiable Neural Computers, Neural Programmer-Interpreters, and Deep Q-Networks. Together, a single entity that is capable of ingesting multiple types of data, audio and visual recognition, general problem solving, learning to learn, algorithm generation, creativity, and interdisciplinary knowledge integration, may be created, resulting in something sort of like in the movie Her.

_Sentience_ is deployed using Docker as a microservices for each distinct aspect of the AGI:

1. Executor  

Executive functions and cognitive control. Appropriate behaviour selection and operation for goal achievement.  

2. Interactor  

Communications and interactions with others.

3. Strategizer  

Data aggregration, analysis, pattern recognition, forecasting, feeding to goal planning, definition of options, preferences, strategies, goals, contexts, and auxillary knowledge store.  

## Installation

### Prerequisites:

a) [Docker](https://www.docker.com/get-docker#h_installation)  

b) [Compose](https://docs.docker.com/compose/install/)  

b) [Git](https://git-scm.com/downloads)  


### Steps:

1. Clone the repository:  

`$ git clone https://github.com/yazanobeidi/sentience.git && cd sentience`

2. Start with `build.sh` which wraps docker-compose :

`$ ./build.sh --prod`

3. Say hello via the terminal!

### Uninstall:

1. Remove Docker images: 

`$ docker-compose down --rmi all`

2. Delete copy of repository:

`$ cd .. && rm -r sentience`

## Disclaimer

This project does not attempt to make the claim that strong AI is actually possible or not. What this project does is try to emulate intelligent behaviour using present state-of-the-art tools in the field. 

## Notes

`python3.6 -m pip` must be used to access pip for Python3.6, as python3.6-pip is not presently packaged with python3.6 in Ubuntu:trusty.

## Author

Yazan Obeidi

## Copyright

Yazan Obeidi, 2017

## Licence

Apache V2

