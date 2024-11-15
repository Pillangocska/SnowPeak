package hu.snowpeak.server.config.rabbitmq;

import com.fasterxml.jackson.databind.ObjectMapper;
import hu.snowpeak.server.entity.Lift;
import hu.snowpeak.server.entity.Log;
import hu.snowpeak.server.repository.LogRepository;
import hu.snowpeak.server.repository.LiftRepository;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.amqp.support.AmqpHeaders;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.util.UUID;

@Component
public class RabbitMQConsumer {
    private static final String QUEUE_NAME = "snow-peak-queue";

    @Autowired
    private LogRepository logRepository;
    @Autowired
    private LiftRepository liftRepository;

    @RabbitListener(queues = "#{queue.name}")  
    public void receiveMessage(
            String message,
            @Header(value = AmqpHeaders.RECEIVED_ROUTING_KEY, required = false) String routingKey) {
        System.out.println("Received message!!!: " + message);
        System.out.println("Received message: " + message);

        try {
            // Parse the lift_id from routing key
            String liftId = extractLiftId(routingKey);

            if (liftId == null) {
                System.err.println("Lift ID could not be extracted from the routing key!");
                return;
            }

            // Fetch the Lift entity
            UUID liftUuid = UUID.fromString(liftId);
            Lift lift = liftRepository.findById(liftUuid)
                    .orElseThrow(() -> new IllegalArgumentException("Lift not found for ID: " + liftId));

            // Convert the payload to a string if not already
            ObjectMapper objectMapper = new ObjectMapper();
            String payload = objectMapper.writeValueAsString(objectMapper.readTree(message));


            // Create and save the Log entity
            Log log = new Log();
            log.setId(UUID.randomUUID());
            log.setPayload(payload);
            log.setTime(LocalDateTime.now());
            log.setLift(lift);// Ensure liftId is a valid UUID

            logRepository.save(log);

            System.out.println("Log saved successfully!");
        } catch (Exception e) {
            System.err.println("Error processing the message: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private String extractLiftId(String routingKey) {
        if (routingKey == null || !routingKey.startsWith("skilift.")) {
            return null;
        }
        // Assume routing key format is "skilift.<lift_id>.logs..."
        String[] parts = routingKey.split("\\.");
        return parts.length > 1 ? parts[1] : null;
    }
}
