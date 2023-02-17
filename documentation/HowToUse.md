# How to Deploy

1. Increase CrateDB virtual Memory

    ```console
    sudo sysctl -w vm.max_map_count=262144
    ```

2. Pull docker images

    ```console
    ./services create
    ```

3. Deploy containers, add database indexes, create entities, device provisioning and create subscriptions.

    ```console
    ./services start
    ```

4. Stop and remove containers

    ```console
    ./services stop
    ```