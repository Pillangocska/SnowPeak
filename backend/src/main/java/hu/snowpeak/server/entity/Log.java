package hu.snowpeak.server.entity;

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
    private LocalDateTime time;
}
