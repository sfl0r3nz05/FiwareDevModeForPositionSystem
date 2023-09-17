# CSV Data Sender

Basic project to send data from a CSV file over a socket.

>**Note:** At this moment the project is ad-hoc to send positioning data loaded in CSV, but in the To Do is to give guidelines to send any kind of data.

## Project status

- The project is under development: 🛠 by [sfl0r3nz05](sfigueroa@ceit.es)

## Architecture

- The CSV Data Sender must be ready for use in any environment. E.g.:

  - Fiware-based environment:

      ![Architecture3](https://user-images.githubusercontent.com/6643905/219717111-a68e0f2b-423e-489a-893f-a04f3c2ee195.png)


  - RabbitMQ-based environment:

      <img width="400" alt="SDG" src="https://user-images.githubusercontent.com/6643905/234698920-2a24ac28-a1f5-453c-a0ed-10d709c48b9b.PNG">

## Requirements

- The requirements are to have docker installed and a network called `syntheticnet` created on it, to install docker you can follow [this](https://docs.docker.com/engine/install/) guide, and to create a docker network run the following command:

  ```bash
  docker network create syntheticnet
  ```

- In case of using the agent to connect to an already existing network, it will be enough to modify the docker-compose file. E.g.:

  ```console
  networks:
    default:
        external:
           name: syntheticnet
  ```

## How to Generate new data

## How to use

1. Set the environment variables of the `docker-compose.yml` file:

  > **Note**: SLEEP_TIME defines the sending time between one packet and another.

    ```console
    SOCK_LISTENER_HOST=publisher
    SOCK_LISTENER_PORT=8053
    SLEEP_TIME=0.9
    ```

2. To launch the program using docker simply place your terminal in the project folder and run the following command:

    ```console
    docker-compose up
    ```

   ### Demonstration

   - [Demonstration video of sending data from the SDG to an AMQP publisher agent](https://youtu.be/OavGNGMnQZ4)
   - [Demostration Video of sending data from the SDG to a MQTT publisher agent](https://youtu.be/k_vCP0BRygY)
   - [Demonstration of sending data to the next information flow: SDG -> Publisher Agent MQTT -> Fiware](https://youtu.be/lwRACg6GNws)

## To Do

- Add trivy vulnerability scanner to github workflow
- Improve project documentation
- Manage any kind of data
