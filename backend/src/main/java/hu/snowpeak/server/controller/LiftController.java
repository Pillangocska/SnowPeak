package hu.snowpeak.server.controller;

import hu.snowpeak.server.model.LiftResponseModel;
import hu.snowpeak.server.model.PrivateLiftResponseModel;
import hu.snowpeak.server.service.LiftService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

import static org.springframework.http.HttpStatus.OK;

@RestController
@Slf4j
@RequiredArgsConstructor
public class LiftController {
    private final LiftService liftService;

    @GetMapping("/public-lifts")
    @ResponseStatus(OK)
    public ResponseEntity<List<LiftResponseModel>> getPublicLifts() {
        return ResponseEntity.ok(liftService.getAllPublicLifts());
    }

    @GetMapping("/private-lifts/{operatorId}")
    @ResponseStatus(OK)
    public ResponseEntity<List<PrivateLiftResponseModel>> getPrivateLiftsByOperatorId(@PathVariable String operatorId) {
        return ResponseEntity.ok(liftService.getPrivateLiftsByOperatorId(operatorId));
    }
}
