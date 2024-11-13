package hu.snowpeak.server.config.rabbitmq;

import org.springframework.amqp.core.*;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RabbitMQConfig {
    private static final String QUEUE_NAME = "snow-peak-queue";
    private static final String ROUTING_KEY = "routing-key";

    @Bean
    public Exchange exchange() {
        return new TopicExchange("exchange-name");
    }

    @Bean
    public Queue queue() {
        return new Queue(QUEUE_NAME, true, false, false);  // durable, not exclusive, not auto-delete
    }

    @Bean
    public Binding binding(Queue queue, Exchange exchange) {
        return BindingBuilder.bind(queue)
                .to(exchange)
                .with(ROUTING_KEY)
                .noargs();
    }
}
