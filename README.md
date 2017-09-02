sentience
=========

The appilication of weak AI towards highly specific and defined areas has had great recent success. However the tasks of data collection, cleansing, ingestion, modelling, evaluation, generating inferences, and updating the model with new information are all largely cumbersome manual processes, and at this point somewhat of an art rather than an exact science. Furthermore a unique learning architecture, dataset, and application must crafted for each of these specific areas.

Many problems can be generalized to several core problems, for example combinatorial optimization and search. What if instead of manually crafting a unique solution for an individual problem, if this problem solving process could be generalized and learned by the given data. In other words instead of learning weights in a pre-defined architecture, if the archicture itself could be learned, as well as the weights, and then this knowledge shared across all domains.

_Sentience_ attempts to solve the problem of problem solving by learning its own learning process. It does this by generating optimal architectures from competing candidates. Specifically a novel fully differntiable training and evaluation process named Meta Learning is proposed.

Several simultaneous mechanisms support Meta Learning: 

1. A dictionary of models and hyperparameters with an ability to retrieve the most suitible architecture based on past experiences. A modifiable number of candidate models are evaluated in a non-blocking fashion such that new optimal architectures may be identified. This may occur for a number of reasons including changing data, or a new model is evaluated which was not considered previously. Models currently are used from Scikit-Learn and Tensorflow. Pre-trained models, preset archicturectures, and learned architectures are all considered.

2. Application of Neural Turing Machines to provide learned representational memory to drive Meta Learning processes. As usual this process is regularized to prefer simpler representations.

3. Endpoints which do not rely on exposure to real-world for learning; a simulation of reality is included in this codebase to facilitate on-going training through emulation. Later these endpoints may be attached to actual IO interfaces for example a propulsion system, vision, touch and contact.

4. Online learning is used when possible with the intent that the dynamic effects of training highly coupled activity, behavioural, analytical, and other systems are immediately realized and resolved.

5. A evolutionary network-in-a-network(-in-a-network...) indirect coupling between all learning systems.

6. Novel goal creation

## Installation

### Prerequisites:

a) [Docker](https://www.docker.com/get-docker#h_installation)
b) [Ccompose](https://docs.docker.com/compose/install/)
b) [Git](https://git-scm.com/downloads)

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

## Notes

`python3.6 -m pip` must be used to access pip for Python3.6, as python3.6-pip is not presently packaged with python3.6 in Ubuntu:trusty.

## Author

Yazan Obeidi

## Copyright

Yazan Obeidi, 2017

## Licence

Apache V2

