FROM maven:3.8.1-eclipse-temurin-17-alpine AS build
WORKDIR /build

COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn clean
RUN mvn package -DskipTests

FROM eclipse-temurin:17-jre-alpine
WORKDIR /opt/app

RUN addgroup -S spring && adduser -S spring -G spring && \
    chown -R spring:spring /opt/app
USER spring:spring
COPY --from=build /build/target/*.jar app.jar

ENV JAVA_OPTS="-Xms512m -Xmx512m"

EXPOSE ${SPRING_BOOT_PORT}
EXPOSE ${AMQP_PORT}

ENTRYPOINT ["sh", "-c", "java ${JAVA_OPTS} -jar app.jar"]