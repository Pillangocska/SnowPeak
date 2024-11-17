package hu.snowpeak.server.service;

import hu.snowpeak.server.entity.Lift;
import hu.snowpeak.server.mapper.LiftMapper;
import hu.snowpeak.server.model.LiftResponseModel;
import hu.snowpeak.server.model.PrivateLiftResponseModel;
import hu.snowpeak.server.repository.LiftRepository;
import hu.snowpeak.server.util.enums.LiftStatus;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Service
@Slf4j
@RequiredArgsConstructor
public class LiftService {
    private final LiftRepository liftRepository;

    private final LiftMapper liftMapper;

    public List<LiftResponseModel> getAllPublicLifts() {
        return liftRepository.findAllByStatus(LiftStatus.PUBLIC).stream().map(liftMapper::fromEntityToDto).toList();
    }

    public List<PrivateLiftResponseModel> getPrivateLiftsByOperatorId(String operatorId) {
        List<Lift> masterLifts = liftRepository.findAllByMasterOperatorIdAndStatus(UUID.fromString(operatorId), LiftStatus.PUBLIC);

        return masterLifts.stream().map(liftMapper::fromEntityToPrivateDto).toList();
    }

    public void markAllAsPrivate() {
        List<Lift> lifts = liftRepository.findAll();

        lifts.forEach(lift -> lift.setStatus(LiftStatus.PRIVATE));

        liftRepository.saveAll(lifts);
    }
}
