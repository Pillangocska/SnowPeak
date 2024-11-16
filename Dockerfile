FROM quay.io/keycloak/keycloak:latest

COPY realms/docker-realm.json /opt/keycloak/data/import/
COPY realms/local-realm.json /opt/keycloak/data/import/
ENV KC_FEATURES_ENABLED=preview
ENV KC_HEALTH_ENABLED=true
ENV KC_METRICS_ENABLED=true
ENV KC_IMPORT=/opt/keycloak/data/import/docker-realm.json,/opt/keycloak/data/import/local-realm.json

ENTRYPOINT ["/opt/keycloak/bin/kc.sh", "start-dev"]