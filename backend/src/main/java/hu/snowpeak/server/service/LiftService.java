package hu.snowpeak.server.service;

import hu.snowpeak.server.mapper.LiftMapper;
import hu.snowpeak.server.model.LiftResponseModel;
import hu.snowpeak.server.repository.LiftRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@Slf4j
@RequiredArgsConstructor
public class LiftService {
    private final LiftRepository liftRepository;

    private final LiftMapper liftMapper;

    public List<LiftResponseModel> getAllLifts() {
        return liftRepository.findAll().stream().map(liftMapper::fromEntityToDto).toList();
    }
}
