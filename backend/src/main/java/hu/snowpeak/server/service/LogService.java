package hu.snowpeak.server.service;

import hu.snowpeak.server.mapper.LogMapper;
import hu.snowpeak.server.model.LogResponseModel;
import hu.snowpeak.server.repository.LogRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@Slf4j
@RequiredArgsConstructor
public class LogService {

    private final LogRepository logRepository;

    private final LogMapper logMapper;

    public List<LogResponseModel> getAllLogs() {
        return logRepository.findAll().stream().map(logMapper::fromEntityToDto).toList();
    }
}
