package hu.snowpeak.server.service;

import hu.snowpeak.server.entity.Lift;
import hu.snowpeak.server.exception.ConfigurationException;
import hu.snowpeak.server.mapper.LiftMapper;
import hu.snowpeak.server.model.LiftConfigModel;
import hu.snowpeak.server.repository.LiftRepository;
import hu.snowpeak.server.util.EnvFileParser;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;
import java.util.stream.Stream;

@Service
@Slf4j
@RequiredArgsConstructor
public class ConfigFileService {

    private final LiftRepository liftRepository;
    private final LiftMapper liftMapper;


    public void processConfigFile(Path filePath) throws IOException {
        Properties properties;

        if (filePath.toString().endsWith(".env")) {
            properties = EnvFileParser.parseEnvFile(filePath);
        } else {
            properties = new Properties();
            try (InputStream input = Files.newInputStream(filePath)) {
                properties.load(input);
            }
        }

        try {
            LiftConfigModel config = new LiftConfigModel();
            config.setLiftId(getRequiredProperty(properties, "LIFT_ID"));

            // Geographic Coordinates
            config.setStartLat(parseDouble(properties, "START_LAT"));
            config.setStartLon(parseDouble(properties, "START_LON"));
            config.setStartElevation(parseDouble(properties, "START_ELEVATION"));
            config.setEndLat(parseDouble(properties, "END_LAT"));
            config.setEndLon(parseDouble(properties, "END_LON"));
            config.setEndElevation(parseDouble(properties, "END_ELEVATION"));

            // Operational Parameters
            config.setArrivalRate(parseInt(properties, "ARRIVAL_RATE"));
            config.setLineSpeed(parseDouble(properties, "LINE_SPEED"));
            config.setCarrierCapacity(parseInt(properties, "CARRIER_CAPACITY"));
            config.setCarrierSpacing(parseInt(properties, "CARRIER_SPACING"));
            config.setCarriersLoading(parseInt(properties, "CARRIERS_LOADING"));

            // Operator Configuration
            config.setMasterOperator(UUID.fromString(getRequiredProperty(properties, "MASTER_OPERATOR")));
            String workerOperators = getRequiredProperty(properties, "WORKER_OPERATORS");
            List<UUID> workerOperatorsList = Arrays.stream(workerOperators.split(",")).map(UUID::fromString).toList();

            config.setWorkerOperators(new HashSet<>(workerOperatorsList));

            Lift liftToSave = liftMapper.fromConfigToEntity(config);

            liftRepository.save(liftToSave);
            log.info("Successfully processed and saved configuration for lift: {}", config.getLiftId());
        } catch (Exception e) {
            log.error("Error processing config file: {}", filePath, e);
            throw new ConfigurationException("Failed to process config file: " + filePath, e);
        }
    }

    private String getRequiredProperty(Properties properties, String key) {
        String value = properties.getProperty(key);
        if (value == null || value.trim().isEmpty()) {
            throw new ConfigurationException("Required property not found: " + key);
        }
        return value.trim();
    }

    private Double parseDouble(Properties properties, String key) {
        String value = getRequiredProperty(properties, key);
        try {
            return Double.parseDouble(value);
        } catch (NumberFormatException e) {
            throw new ConfigurationException("Invalid double value for " + key + ": " + value);
        }
    }

    private Integer parseInt(Properties properties, String key) {
        String value = getRequiredProperty(properties, key);
        try {
            return Integer.parseInt(value);
        } catch (NumberFormatException e) {
            throw new ConfigurationException("Invalid integer value for " + key + ": " + value);
        }
    }

    public void processConfigDirectory(String directoryPath) throws IOException {
        try (Stream<Path> paths = Files.walk(Paths.get(directoryPath))) {
            //liftRepository.deleteAll();

            paths.filter(Files::isRegularFile)
                    .filter(path -> path.toString().endsWith(".env"))
                    .forEach(path -> {
                        try {
                            processConfigFile(path);
                        } catch (IOException e) {
                            log.error("Error processing file: {}", path, e);
                        }
                    });
        }
    }
}
