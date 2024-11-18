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

import java.io.StringReader;
import java.time.LocalDateTime;
import java.util.*;

@Component
public class RabbitMQConsumer {
    private static final String QUEUE_NAME = "snow-peak-queue";

    HashMap<UUID, ArrayList<Double>> temperatures = new HashMap<>();

    @Autowired
    private LogRepository logRepository;
    @Autowired
    private LiftRepository liftRepository;
    @Autowired
    private RabbitMQProducer rabbitMQProducer;
    @Autowired
    private ObjectMapper objectMapper;

    @RabbitListener(queues = "#{queue.name}")
    public void receiveMessage(
            String message,
            @Header(value = AmqpHeaders.RECEIVED_ROUTING_KEY, required = false) String routingKey) {
        System.out.println("Received message!!!: " + message);
        System.out.println("Received message: " + message);

        UUID liftUuid = null;

        try {
            // Parse the lift_id from routing key
            String liftId = extractLiftId(routingKey);

            if (liftId == null) {
                System.err.println("Lift ID could not be extracted from the routing key!");
                return;
            }

            // Fetch the Lift entity
            liftUuid = UUID.fromString(liftId);
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

        try{
            ArrayList<Double> tmpList = new ArrayList<>();

            ObjectMapper objectMapper = new ObjectMapper();

            // Convert JSON string to a Map
            Map<String, Object> map = objectMapper.readValue(message, Map.class);

            if(map.get("type").equals("temperature") && liftUuid != null) {
                double newTemperature = Double.parseDouble(map.get("value").toString());
                int index = 0;
                index = map.get("location").equals("base") ? 0 : 1;
                if(temperatures.containsKey(liftUuid)) {

                    if(isMoreThanPercentDifferent(temperatures.get(liftUuid).get(index), newTemperature, 5)){

                        System.out.println("WARN!! Invalid temperature value!");

                        //send warning message to the lift for invalid temperature value
                        Map<String, Object> suggestion = new HashMap<>();
                        suggestion.put("messageKind", "suggestion");
                        suggestion.put("user", "abc123");
                        suggestion.put("severity", "WARNING");
                        suggestion.put("timestamp", LocalDateTime.now().toString());
                        suggestion.put("message", String.format(
                                "Invalid temperature value detected: %f. Previous value: %f",
                                newTemperature,
                                temperatures.get(liftUuid).get(index)
                        ));

                        // Convert suggestion to JSON string
                        String suggestionString = objectMapper.writeValueAsString(suggestion);

                        System.out.println(suggestionString);

                        // Send the suggestion message using the lift's UUID as routing key
                        rabbitMQProducer.sendSuggestion(suggestionString, liftUuid.toString());
                    }
                    else {
                        tmpList.clear();
                        tmpList = temperatures.get(liftUuid);
                        temperatures.get(liftUuid).clear();
                        for(int i = 0; i < tmpList.size(); i++) {
                            if(i != index) {
                                temperatures.get(liftUuid).add(tmpList.get(i));
                            }
                            else {
                                temperatures.get(liftUuid).add(newTemperature);
                            }
                        }
                    }
                }
                else {
                    tmpList.add(index, newTemperature);
                    temperatures.put(liftUuid, tmpList);
                }
            }
        } catch (Exception e) {
            System.err.println("Error processing message data: " + e.getMessage());
        }
    }

    private String extractLiftId(String routingKey) {
        if (routingKey == null || !routingKey.startsWith("skilift.")) {
            return null;
        }
        String[] parts = routingKey.split("\\.");
        return parts.length > 1 ? parts[1] : null;
    }

    private static boolean isMoreThanPercentDifferent(double baseValue, double compareValue, double precent) {
        baseValue = Math.abs(baseValue);
        compareValue = Math.abs(compareValue);

        double threshold = baseValue * (precent / 100);

        return baseValue + threshold < compareValue || baseValue - threshold > compareValue;
    }
}
