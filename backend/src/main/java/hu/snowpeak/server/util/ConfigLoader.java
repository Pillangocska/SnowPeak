package hu.snowpeak.server.util;

import hu.snowpeak.server.service.ConfigFileService;
import hu.snowpeak.server.service.LiftService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
@Slf4j
@RequiredArgsConstructor
public class ConfigLoader implements CommandLineRunner {

    private final ConfigFileService configFileService;
    private final LiftService liftService;

    @Value("${config.directory.path}")
    private String configDirectoryPath;

    @Override
    public void run(String... args) throws Exception {
        log.info("Starting to load configurations from directory: {}", configDirectoryPath);
        liftService.markAllAsPrivate();
        configFileService.processConfigDirectory(configDirectoryPath);
        log.info("Completed loading configurations");
    }
}