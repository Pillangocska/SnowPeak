package hu.snowpeak.server.controller;

import hu.snowpeak.server.model.LogResponseModel;
import hu.snowpeak.server.service.LogService;
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
public class LogController {
    private final LogService logService;

    @GetMapping("/logs")
    @ResponseStatus(OK)
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<List<LogResponseModel>> getLogs() {
        return ResponseEntity.ok(logService.getAllLogs());
    }
}
