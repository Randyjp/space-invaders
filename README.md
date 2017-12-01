# Space Invaders

Recreation of the classic Space Invaders game, made following the instruction contained in the book Python Crash Course. 
This was a toy project with the intention of brushing up some of my Python3 skills and by no means contains all the 
features included in the  original game. 

## Getting Started

At its current state, the project runs only on linux machines, this is a result of the way docker
interacts with the video drivers of the the host computer. For the most part, you only need to
download the project files and run the commands contained in the installing section. 

### Prerequisites

You need to install the Docker daemon and Docker compose in order to run the game. For instructions
on how to install them, follow the links below:

* [Docker](https://docs.docker.com/engine/installation/)
* [Docker Compose](https://docs.docker.com/compose/install/)

### Installing

There's two steps to have the game up and running. From the root of the project: 

* Build the Docker image from the Docker file: 

```
docker build -t yourname/spaceinvaders .
```

* Run compose: 

```
docker-compose build
```

* Fire up your docker container: 

```
docker-compose up
```


## Built With

* [Docker](https://www.docker.com/) - Container manager
* [Pygame](https://www.pygame.org/) - Gaming Library for Python

## Authors

* **Randy Perez**

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

