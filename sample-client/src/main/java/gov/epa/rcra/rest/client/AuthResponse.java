package gov.epa.rcra.rest.client;

import java.time.ZonedDateTime;

public record AuthResponse(String token, ZonedDateTime expiration) {
}