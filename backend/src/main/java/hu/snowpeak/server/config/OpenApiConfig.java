package hu.snowpeak.server.config;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.enums.SecuritySchemeIn;
import io.swagger.v3.oas.annotations.enums.SecuritySchemeType;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.security.SecurityScheme;
import org.springframework.context.annotation.Configuration;

@Configuration
@SecurityScheme(name = "bearerAuth", type = SecuritySchemeType.HTTP, in = SecuritySchemeIn.HEADER, bearerFormat = "JWT", scheme = "bearer")
@OpenAPIDefinition(
        info = @Info(
                title = "SnowPeak API",
                version = "${api.version}",
                description = "${api.description}"
        ),
        security = {@SecurityRequirement(name = "bearerAuth")}
)
public class OpenApiConfig {
}
