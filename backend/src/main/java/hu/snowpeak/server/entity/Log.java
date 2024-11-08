package hu.snowpeak.server.entity;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.fasterxml.jackson.datatype.jsr310.deser.LocalDateTimeDeserializer;
import com.fasterxml.jackson.datatype.jsr310.ser.LocalDateTimeSerializer;
import hu.snowpeak.server.model.LogPayloadModel;
import io.hypersistence.utils.hibernate.type.json.JsonType;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.Type;

import java.time.LocalDateTime;

@Entity
@Table(name = "log")
@AttributeOverrides({
        @AttributeOverride(name = "id", column = @Column(name = "log_id")),
})
@Getter
@Setter
@RequiredArgsConstructor
public class Log extends AbstractBaseEntity {

    @ManyToOne
    @JoinColumn(name = "log_lift_id")
    private Lift lift;

    // TODO: Enum legyen majd szerintem
    @Column(name = "log_queue_name")
    private String queueName;

    @Column(name = "log_payload", columnDefinition = "json")
    @Type(JsonType.class)
    private LogPayloadModel payload;

    @Column(name = "log_time")
    @JsonDeserialize(using = LocalDateTimeDeserializer.class)
    @JsonSerialize(using = LocalDateTimeSerializer.class)
    private LocalDateTime time;
}
