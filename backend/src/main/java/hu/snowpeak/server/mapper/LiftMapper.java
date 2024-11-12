package hu.snowpeak.server.mapper;

import hu.snowpeak.server.entity.Lift;
import hu.snowpeak.server.model.LiftConfigModel;
import hu.snowpeak.server.model.LiftResponseModel;
import lombok.extern.slf4j.Slf4j;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.ReportingPolicy;

@Mapper(componentModel = "spring", unmappedTargetPolicy = ReportingPolicy.IGNORE)
@Slf4j
public abstract class LiftMapper {

    public abstract LiftResponseModel fromEntityToDto(Lift lift);

    @Mapping(target = "id", source = "liftId")
    @Mapping(target = "startLatitude", source = "startLat")
    @Mapping(target = "startLongitude", source = "startLon")
    @Mapping(target = "startElevation", source = "startElevation")
    @Mapping(target = "endLatitude", source = "endLat")
    @Mapping(target = "endLongitude", source = "endLon")
    @Mapping(target = "endElevation", source = "endElevation")
    @Mapping(target = "seatCapacity", source = "carrierCapacity")
    @Mapping(target = "numberOfSeats", source = "carrierSpacing")
    @Mapping(target = "masterOperatorId", source = "masterOperator")
    @Mapping(target = "workers", source = "workerOperators")
    public abstract Lift fromConfigToEntity(LiftConfigModel liftConfig);
}
