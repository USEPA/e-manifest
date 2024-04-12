package gov.epa.rcra.rest.auth;

import java.time.ZonedDateTime;

public record AuthResponse(String token, ZonedDateTime expiration) {
}