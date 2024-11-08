package hu.snowpeak.server.model;

import lombok.Data;

import java.time.LocalDateTime;
import java.util.UUID;

@Data
public class LogResponseModel {
    private UUID id;
    private UUID liftId;
    private String queueName;
    private String payload;
    private LocalDateTime time;
}
