package hu.snowpeak.server.entity;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.fasterxml.jackson.datatype.jsr310.deser.LocalDateTimeDeserializer;
import com.fasterxml.jackson.datatype.jsr310.ser.LocalDateTimeSerializer;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;

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

    @Column(name = "log_payload")
    private String payload;

    @Column(name = "log_time")
    @JsonDeserialize(using = LocalDateTimeDeserializer.class)
    @JsonSerialize(using = LocalDateTimeSerializer.class)
    private LocalDateTime time;
}
