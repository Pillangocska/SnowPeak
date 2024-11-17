FROM quay.io/keycloak/keycloak:latest

# Copy realm files
COPY realms/docker-realm.json /opt/keycloak/data/import/
COPY realms/local-realm.json /opt/keycloak/data/import/

# Set environment variables
ENV KC_FEATURES_ENABLED=preview
ENV KC_HEALTH_ENABLED=true
ENV KC_METRICS_ENABLED=true

# Build the optimized version for production
RUN /opt/keycloak/bin/kc.sh build

# Use array syntax for better argument handling
ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
CMD ["start-dev", "--import-realm"]
