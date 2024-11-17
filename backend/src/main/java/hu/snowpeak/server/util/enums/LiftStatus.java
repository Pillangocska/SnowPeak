package hu.snowpeak.server.util.enums;


import lombok.Getter;

public enum LiftStatus {
    PRIVATE("PRIVATE"),
    PUBLIC("PUBLIC");

    @Getter
    private String status;

    LiftStatus(String status) {
        this.status = status;
    }
}
