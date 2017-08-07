sentience
=========

If you've seen the movie ![Her](https://en.wikipedia.org/wiki/Her_%28film%29) you may remember Samantha - the intelligent assistant. Well if you were hoping for your own personal meta learning system, you're in luck.

The goal of this project is to produce an information concierge to enhance ones life. Sentience can do things you would rather not, for example find an apartment, make a reservation, or even plan a vacation itinerary - all without explicitly defining the necessary workflow. The system is able to process abstract and indirect commands, and can even predict new potential actions to add value to your life. Sentience consumes text, speach, and video. It processes streaming and batch data, extracting events to understand and respond to task assignment, questions, and small talk. Sentience uses deep meta learning and hyper learning to generate ideal models on the fly, from a list configurable in `config/models/`. It is outfitted with the ability to problem solve problem solving itself, capable of figuring out the required learning methods and information required to train itself to complete a certain task. The next time it encounters that same task it can draw on what was previously learned and even use other experiences as a basis to improve itself. 

Sentience is built using microservices such that functionalities are independent and non-blocking. A Kafka message queue is used to facilitate communication between services in JSON format encoded as string. Python is used due to convenience for libraries such as Scikit-Learn and Tensorflow. It is also convenient for rapid prototyping.

## Installation

### Prerequisites:

a) ![Docker](https://www.docker.com/get-docker#h_installation)
b) ![Ccompose](https://docs.docker.com/compose/install/)
b) ![Git](https://git-scm.com/downloads)

### Steps:

1. Clone the repository:  

`$ git clone https://github.com/yazanobeidi/sentience.git && cd sentience`

2. Start with `build.sh` which wraps docker-compose :

`$ ./build.sh --prod`

3. Say hello via the terminal!

### Uninstall:

1. Remove Docker images
`$ docker-compose down --rmi all`

2. Delete copy of repository:

`$ cd .. && rm -rf sentience`

## Author

Yazan Obeidi

## Copyright

Yazan Obeidi, 2017

## Licence

Apache V2

