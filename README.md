sentience
=========

The application of weak AI towards highly specific and defined areas has had great recent success. However the tasks of data collection, cleansing, ingestion, modelling, evaluation, generating inferences, and updating the model with new information are all largely cumbersome manual processes, and at this point somewhat of an art rather than an exact science. Furthermore a unique learning architecture, dataset, and application must crafted for each of these specific areas.

Many problems can be generalized to several core problems, for example combinatorial optimization, constraint satisfaction and search. What if instead of manually crafting a unique solution for an individual problem, if this problem solving process could be generalized and learned by the given data. In other words instead of learning weights in a pre-defined architecture, if the archicture itself could be learned, as well as the weights, and then this knowledge shared across all domains.

_Sentience_ attempts to solve the problem of problem solving by learning its own learning process. It does this by generating optimal architectures from competing candidates. Specifically a novel fully differentiable training and evaluation process named Meta Learning is proposed.

Several simultaneous mechanisms support Meta Learning: 

1. An evolutionary network-in-a-network(-in-a-network...) design to facilitate reinforcement learning through indirect coupling between all learning systems. Each sub-system is decoupled as a microservice and communicates using a messaging protocol. Apache Kafka is presently used. Each sub-system is sufficient so that it may carry out its own functionality independent of other sub-systems. However feedback and a type of entanglement between subsystems does occur as part of normal system behaviour, forming a sort of quasi-dependency with an indeterminate causality. For example, Sentience may have executive capacity greater than its present ability for normal human communication. By design the executive capacity will not be reduced due to lagging communication skills; they may only be enhanced by ideal communication, catalyzing the training of executive functionality.

2. Application of Neural Turing Machines (NTM) to provide learned representational memory to drive Meta Learning processes. This process is regularized to prefer simpler representations. NTM memory provides short term and long term access and is the only place where state information is persisted in the system. This memory differs from the weights in a machine learning model in that memory cells within a NTM may define algorithmic functionality such as copying and sorting at its most basic level. This contrasts with simply modifying the output of a classifier by updating its underlying weights.

3. A dictionary of models and hyperparameters with an ability to retrieve the most suitable architecture based on past experiences. A tunable number of candidate models are evaluated in a non-blocking fashion such that new optimal architectures may be identified. This may occur for a number of reasons including changing data, or a new model is evaluated which was not considered previously. Models currently are used from Scikit-Learn and Tensorflow. Pre-trained models, preset archicturectures, and learned architectures are all considered.

4. Endpoints which do not rely on exposure to real-world for learning; a simulation of reality is included in this codebase to facilitate on-going training through emulation. Later these endpoints may be attached to actual IO hardware interfaces for example a propulsion system, vision, touch and contact.

5. Online learning is used when possible with the intent that the dynamic effects of training highly coupled activity, behavioural, analytical, and other systems are immediately resolved.


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

`$ cd .. && rm -rf sentience`

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

