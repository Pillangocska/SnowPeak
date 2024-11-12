package hu.snowpeak.server.util;

import lombok.extern.slf4j.Slf4j;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Properties;

@Slf4j
public class EnvFileParser {
    public static Properties parseEnvFile(Path filePath) throws IOException {
        Properties properties = new Properties();
        List<String> lines = Files.readAllLines(filePath);

        for (String line : lines) {
            if (line.trim().isEmpty() || line.trim().startsWith("#")) {
                continue;
            }

            int commentIndex = line.indexOf('#');
            if (commentIndex > 0) {
                line = line.substring(0, commentIndex).trim();
            }

            int equalIndex = line.indexOf('=');
            if (equalIndex > 0) {
                String key = line.substring(0, equalIndex).trim();
                String value = line.substring(equalIndex + 1).trim();

                if (value.startsWith("\"") && value.endsWith("\"")) {
                    value = value.substring(1, value.length() - 1);
                }
                if (value.startsWith("'") && value.endsWith("'")) {
                    value = value.substring(1, value.length() - 1);
                }

                properties.setProperty(key, value);
            }
        }
        return properties;
    }
}
