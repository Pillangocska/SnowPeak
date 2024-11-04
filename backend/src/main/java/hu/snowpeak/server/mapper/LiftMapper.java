package hu.snowpeak.server.mapper;

import hu.snowpeak.server.entity.Lift;
import hu.snowpeak.server.model.LiftResponseModel;
import lombok.extern.slf4j.Slf4j;
import org.mapstruct.Mapper;
import org.mapstruct.ReportingPolicy;

@Mapper(componentModel = "spring", unmappedTargetPolicy = ReportingPolicy.IGNORE)
@Slf4j
public abstract class LiftMapper {

    public abstract LiftResponseModel fromEntityToDto(Lift product);
}
