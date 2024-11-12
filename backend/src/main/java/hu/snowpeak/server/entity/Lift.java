package hu.snowpeak.server.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.experimental.SuperBuilder;

import java.util.Set;
import java.util.UUID;

@Entity
@Table(name = "lift")
@AttributeOverrides({
        @AttributeOverride(name = "id", column = @Column(name = "lift_id")),
})
@Getter
@Setter
@RequiredArgsConstructor
@SuperBuilder(toBuilder = true)
public class Lift extends AbstractBaseEntity {

    @Column(name = "lift_start_latitude")
    private Float startLatitude;

    @Column(name = "lift_start_longitude")
    private Float startLongitude;

    @Column(name = "lift_start_elevation")
    private Float startElevation;

    @Column(name = "lift_end_latitude")
    private Float endLatitude;

    @Column(name = "lift_end_longitude")
    private Float endLongitude;

    @Column(name = "lift_end_elevation")
    private Float endElevation;

    @Column(name = "lift_seat_capacity")
    private Integer seatCapacity;

    @Column(name = "lift_num_seats")
    private Integer numberOfSeats;

    @Column(name = "lift_master_operator_id")
    private UUID masterOperatorId;

    @ElementCollection
    @CollectionTable(name = "worker",
            joinColumns = {@JoinColumn(name = "worker_lift_id", referencedColumnName = "lift_id", nullable = false)})
    @Column(name = "worker_id")
    private Set<UUID> workers;
}
