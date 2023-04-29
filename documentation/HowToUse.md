# How to Deploy

1. Increase CrateDB virtual Memory

    ```console
    sudo sysctl -w vm.max_map_count=262144
    ```

2. Update the submodules:

    ```console
    git submodule update --init --recursive
    ```

3. Update the `PROTOCOL` environmental variable from `AMQP` to `MQTT`:

    ```console
    cd ./Publisher-Agent
    nano docker-compose.yml
    PROTOCOL=MQTT
    ```

4. Pull docker images

    ```console
    ./services create
    ```

5. Deploy containers, add database indexes, create entities, device provisioning and create subscriptions.

    ```console
    ./services start
    ```

6. Stop and remove containers

    ```console
    ./services stop
    ```