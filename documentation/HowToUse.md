# How to Deploy

1. Access to `provision` folder once the respository has been cloned:

    ```console
    cd ~/FiwareDockerDevMode/provision/
    ```

2. Create and copy the certificates using `ssl.sh` script from services names like api. E.g.:

    > Details of the script have been documented in [Security Layer](./AddSecurityLayer.md)

    ```console
    ./ssl.sh api
    ```

3. Increase CrateDB virtual Memory

    ```console
    sudo sysctl -w vm.max_map_count=262144
    ```

4. Update the `PROTOCOL` environmental variable from `AMQP` to `MQTT`:

    ```console
    cd ./Publisher-Agent
    nano docker-compose.yml
    PROTOCOL=MQTT
    ```

5. Pull docker images

    ```console
    ./services create
    ```

6. Deploy containers, add database indexes, create entities, device provisioning and create subscriptions.

    ```console
    ./services start
    ```

7. Stop and remove containers

    ```console
    ./services stop
    ```
