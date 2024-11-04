package hu.snowpeak.server.model;

import lombok.Data;

import java.util.UUID;

@Data
public class LiftResponseModel {
    private UUID id;
    private UUID extId;
    private Float startLatitude;
    private Float startLongitude;
    private Float startElevation;
    private Float endLatitude;
    private Float endLongitude;
    private Float endElevation;
    private Integer seatCapacity;
    private Integer numberOfSeats;
}
