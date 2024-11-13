package hu.snowpeak.server.service;

import hu.snowpeak.server.entity.Lift;
import hu.snowpeak.server.mapper.LiftMapper;
import hu.snowpeak.server.model.LiftResponseModel;
import hu.snowpeak.server.model.PrivateLiftResponseModel;
import hu.snowpeak.server.repository.LiftRepository;
import hu.snowpeak.server.util.AuthContextHelper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Stream;

@Service
@Slf4j
@RequiredArgsConstructor
public class LiftService {
    private final LiftRepository liftRepository;

    private final LiftMapper liftMapper;

    public List<LiftResponseModel> getAllLifts() {
        return liftRepository.findAll().stream().map(liftMapper::fromEntityToDto).toList();
    }

    public List<PrivateLiftResponseModel> getPrivateLifts() {
        List<Lift> workerLifts = liftRepository.findAllByWorkersContaining(AuthContextHelper.getUserId());
        List<Lift> masterLifts = liftRepository.findAllByMasterOperatorId(AuthContextHelper.getUserId());

        return Stream.concat(workerLifts.stream(), masterLifts.stream()).map(liftMapper::fromEntityToPrivateDto).toList();
    }
}
