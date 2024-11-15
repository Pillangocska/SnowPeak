package hu.snowpeak.server.controller;

import hu.snowpeak.server.model.LiftResponseModel;
import hu.snowpeak.server.model.PrivateLiftResponseModel;
import hu.snowpeak.server.service.LiftService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
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
        return ResponseEntity.ok(liftService.getAllLifts());
    }

    @GetMapping("/private-lifts")
    @ResponseStatus(OK)
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<List<PrivateLiftResponseModel>> getPrivateLifts() {
        return ResponseEntity.ok(liftService.getPrivateLifts());
    }
}
