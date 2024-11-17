package hu.snowpeak.server.model;

import hu.snowpeak.server.util.enums.LiftStatus;
import lombok.Data;

import java.util.Set;
import java.util.UUID;

@Data
public class LiftConfigModel {
    private String liftId;

    private Double startLat;
    private Double startLon;
    private Double startElevation;
    private Double endLat;
    private Double endLon;
    private Double endElevation;

    private Integer arrivalRate;
    private Double lineSpeed;
    private Integer carrierCapacity;
    private Integer carrierSpacing;
    private Integer carriersLoading;

    private LiftStatus status;

    private UUID masterOperator;
    private Set<UUID> workerOperators;
}