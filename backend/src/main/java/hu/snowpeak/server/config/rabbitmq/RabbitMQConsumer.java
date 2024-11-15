package hu.snowpeak.server.config.rabbitmq;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

@Component
public class RabbitMQConsumer {
    private static final String QUEUE_NAME = "snow-peak-queue";

    @RabbitListener(queues = "#{queue.name}")  // Reference the anonymous queue by its bean name
    public void receiveMessage(String message) {
        System.out.println("Received message!!!: " + message);
        try {
            ObjectMapper mapper = new ObjectMapper();
            Object json = mapper.readValue(message, Object.class);
            System.out.println(mapper.writerWithDefaultPrettyPrinter().writeValueAsString(json));
            System.out.println();
        } catch (JsonProcessingException e) {
            System.out.println("Received message: " + message);
        }
    }
}
