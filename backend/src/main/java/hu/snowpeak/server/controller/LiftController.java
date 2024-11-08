package hu.snowpeak.server.controller;

import hu.snowpeak.server.model.LiftResponseModel;
import hu.snowpeak.server.service.LiftService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
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

    @GetMapping("/lifts")
    @ResponseStatus(OK)
//    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<List<LiftResponseModel>> getLifts() {
        return ResponseEntity.ok(liftService.getAllLifts());
    }
}