=====
Usage
=====

To use b_rabbit in a project::

    from b_rabbit.b_rabbit import BRabbit


    #first, you need to create a BRabbit instance to provide rabbitMQ connection:

    # create a parent instance which provide a global rabbitMQ connection
    rabbit = BRabbit(host='localhost', port=5672)

    # Now it is very easy to use the messaging pattern with rabbitmq
    # here is a demonstration of using the publish-subscribe


    # first create a publisher instance from the parent
    publisher = rabbit.EventPublisher(b_rabbit=rabbit,
                                        publisher_name='whatever_you_name_it')

    # now you can just publish your message:
    publisher.publish(routing_key='testing.test',
                      payload='Hello from publisher')


    # similarly subscribing is very easy to implement:
    # first a subscriber instance from the parent class
    subscriber = rabbit.EventSubscriber(
                                    b_rabbit=rabbit,
                                    routing_key='testing.test',
                                    publisher_name='name_it',
                                    event_listener=callback)

     # the callback is a function you need to define in order to do something with the received message
     def callback(msg):
        # do something with the received msg from the publisher
        print(f"msg received: {msg}")


     # after that subscribing is straightforward:
     subscriber.subscribe_on_thread()

    # take a look in the examples to see a working publish-subscribe and RPC
