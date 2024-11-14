package hu.snowpeak.server.repository;

import hu.snowpeak.server.entity.Lift;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface LiftRepository extends JpaRepository<Lift, UUID> {
    List<Lift> findAllByWorkersContaining(UUID workerId);

    List<Lift> findAllByMasterOperatorId(UUID masterId);
}
