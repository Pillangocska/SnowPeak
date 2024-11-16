package hu.snowpeak.server.config.rabbitmq;

import org.springframework.amqp.core.DirectExchange;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Component;

@Component
public class RabbitMQProducer {

    private static final String SUGGESTION_EXCHANGE = "direct_suggestions";

    @Value("${rabbitmq.exchange.name}")
    private String exchangeName;

    @Autowired
    private RabbitTemplate rabbitTemplate;

    @Bean
    public DirectExchange suggestionExchange() {
        return new DirectExchange(SUGGESTION_EXCHANGE);
    }

    public void sendMessage(String message) {
        rabbitTemplate.convertAndSend(
                exchangeName,
                "skilift.#",
                message
        );
    }

    public void sendMessage(String message, String routingKey) {
        rabbitTemplate.convertAndSend(
                exchangeName,
                routingKey,
                message
        );
    }

    public void sendSuggestion(String suggestionMessage, String liftId) {
        rabbitTemplate.convertAndSend(
                SUGGESTION_EXCHANGE,
                liftId, // Using liftId as routing key
                suggestionMessage
        );
    }
}
