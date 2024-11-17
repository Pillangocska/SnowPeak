FROM maven:3.9.6-eclipse-temurin-21 AS build
WORKDIR /build

COPY pom.xml .
COPY config ./config
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn clean
RUN mvn package -DskipTests

FROM eclipse-temurin:21-jre-alpine
WORKDIR /opt/app

RUN addgroup -S spring && adduser -S spring -G spring && \
    chown -R spring:spring /opt/app
USER spring:spring
COPY --from=build /build/target/*.jar app.jar
COPY --from=build /build/config ./config

EXPOSE ${SPRING_BOOT_PORT}

ENTRYPOINT ["sh", "-c", "java -jar app.jar"]
