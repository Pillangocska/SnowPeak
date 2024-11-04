package hu.snowpeak.server.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import lombok.experimental.SuperBuilder;

import java.util.Optional;
import java.util.UUID;

@Getter
@Setter
@ToString
@RequiredArgsConstructor
@MappedSuperclass
@SuperBuilder(toBuilder = true)
public class AbstractBaseEntity {
    @Id
    @Column(name = "id")
    private UUID id;

    @PrePersist
    @PreUpdate
    private void beforeSave() {
        setId(Optional.ofNullable(id).orElse(UUID.randomUUID()));
    }
}
