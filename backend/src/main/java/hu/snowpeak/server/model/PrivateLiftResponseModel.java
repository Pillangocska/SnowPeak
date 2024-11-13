package hu.snowpeak.server.model;

import lombok.Data;

import java.util.UUID;

@Data
public class PrivateLiftResponseModel {
    private UUID id;
    private Float startLatitude;
    private Float startLongitude;
    private Float startElevation;
    private Float endLatitude;
    private Float endLongitude;
    private Float endElevation;
    private Integer seatCapacity;
    private Integer numberOfSeats;
}
