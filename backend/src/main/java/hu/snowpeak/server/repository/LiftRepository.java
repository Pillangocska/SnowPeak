package hu.snowpeak.server.repository;

import hu.snowpeak.server.entity.Lift;
import hu.snowpeak.server.util.enums.LiftStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface LiftRepository extends JpaRepository<Lift, UUID> {
    List<Lift> findAllByMasterOperatorIdAndStatus(UUID masterId, LiftStatus status);

    List<Lift> findAllByStatus(LiftStatus status);
}
