package hu.snowpeak.server.mapper;

import hu.snowpeak.server.entity.Log;
import hu.snowpeak.server.model.LogResponseModel;
import lombok.extern.slf4j.Slf4j;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.ReportingPolicy;

@Mapper(componentModel = "spring", unmappedTargetPolicy = ReportingPolicy.IGNORE)
@Slf4j
public abstract class LogMapper {

    @Mapping(expression = "java(log.getLift().getId())", target = "liftId")
    public abstract LogResponseModel fromEntityToDto(Log log);
}
