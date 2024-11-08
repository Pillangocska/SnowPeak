package hu.snowpeak.server.mapper;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import hu.snowpeak.server.entity.Log;
import hu.snowpeak.server.model.LogResponseModel;
import lombok.extern.slf4j.Slf4j;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.ReportingPolicy;

@Mapper(componentModel = "spring", unmappedTargetPolicy = ReportingPolicy.IGNORE)
@Slf4j
public abstract class LogMapper {

    @Mapping(expression = "java(entityToJsonString(log))", target = "payload")
    @Mapping(expression = "java(log.getLift().getId())", target = "liftId")
    public abstract LogResponseModel fromEntityToDto(Log log);

    public String entityToJsonString(Log log) {
        ObjectMapper mapper = new ObjectMapper();

        try {
            return mapper.writeValueAsString(log);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }
}
