import docker




def __initiate():
    """
        This initialize all the database that is required for hosting mqtt_web
    """
    client = docker.from_env()
    #Run RabbitMQ file monitor message handler
    # docker run -d --hostname my-rabbit --name some-rabbit -p 8080:15672 rabbitmq:3-management
    container2 = client.containers.run("rabbitmq:3-management", name='monitor-mq-test', ports= {'15672/tcp': 8080, '5672/tcp': 5672}, detach=True, )


if __name__ == "__main__":
    __initiate()