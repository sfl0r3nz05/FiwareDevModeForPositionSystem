# Publisher Agent

The publisher agent is responsible for organizing the positioning data (raw data) received from a Synthetic Data Generator (see CSV-Data-Sender
project) for a given identifier (e.g., tag) and sending it to the edge via AMQP or MQTT messaging technologies.

>**Note:** At this moment the project is ad-hoc to send positioning data loaded in CSV, but in the To Do is to give guidelines to send any kind of data.

## Project status

- The project is under development: 🛠 by [sfl0r3nz05](sfigueroa@ceit.es)

## Architecture

- The publisher agent must be ready for use in any environment. E.g.:

  - Fiware-based environment:

      ![Architecture1](https://user-images.githubusercontent.com/6643905/219717124-d5d2db80-e31b-42a9-854b-261e1c25ac43.png)


  - RabbitMQ-based environment:

      <img width="450" alt="ConsumerAgent" src="https://user-images.githubusercontent.com/6643905/234698918-11b62db0-a0b2-41b1-94be-99009d1e61d9.PNG">

## Requirements

1. [Install docker]((https://docs.docker.com/engine/install/)).
2. Enable same docker network as the publisher. E.g. a network called `syntheticnet`:

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

3. Other option could be use `host` as `network_mode`. Sample of result:

    ```console
    services:
      publisher-agent:
        ...
         - MQTT_QUEUE_PORT=1883
          - TOPIC=/5jggokgpepnvsb2uv4s40d59ov/tag001/attrs
        ports:
          - 8053:8053
        network_mode: "host"
    ```

## How to Receive data from SDG

## How to use

1. Set the environment variables of the `docker-compose.yml` file depending on the messaging technology:

    > *Note: SLLEP_TIME environmental variable defines the sending time between one packet and another*

    ```bash
    SLEEP_TIME=10
    ```

    > *Note: PROTOCOL environmental variable allows to define the messaging technology type*

    ```bash
    PROTOCOL=AMQP
    ```

    > *Note: TOPIC environmental variable defines the name of the topic to be used*

    ```bash
    TOPIC=/5jggokgpepnvsb2uv4s40d59ov/tag001/attrs
    ```

    ```bash
    AMQP_QUEUE_HOST=rmq0
    ```

    ```bash
    AMQP_QUEUE_PORT=5672
    ```

    ```bash
    MQTT_QUEUE_HOST=mosquitto
    ```

    ```bash
    MQTT_QUEUE_PORT=1883
    ```

3. To launch the program using docker simply place your terminal in the project folder and run the following command:

    ```bash
    docker-compose up -d
    ```

## Test the publisher agent for amqp

For test purpose adding the next service to `docker-compose.yml` file.

```bash
rmq0:
  hostname: rmq0
  image:  'rabbitmq:3.6.7-management'
  ports:
    - 5672:5672
    - 15672:15672
  cap_add:
    - ALL
```

   ### Demonstration

   - [Demonstration video of sending data from the SDG to an AMQP publisher agent](https://youtu.be/OavGNGMnQZ4)

## Test the publisher agent for mqtt

For test purpose adding the next service to `docker-compose.yml` file.

```bash
mosquitto:
  image: eclipse-mosquitto:1.6.14
  hostname: mosquitto
  expose:
    - "1883"
    - "9001"
  ports:
    - "1883:1883"
    - "9001:9001"
  volumes:
    - ./mosquitto/mosquitto.conf:/mosquitto/config/mosquitto.conf
```

   ### Demonstration

   - [Demostration Video of sending data from the SDG to a MQTT publisher agent](https://youtu.be/k_vCP0BRygY)
   - [Demonstration of sending data to the next information flow: SDG -> Publisher Agent MQTT -> Fiware](https://youtu.be/lwRACg6GNws)

## To Do

- Add trivy vulnerability scanner to github workflow
- Improve project documentation
- Manage any kind of data
- Support other the messaging technologies like Kafka or HTTP
- Implement a solution to handle several topics simultaneously
