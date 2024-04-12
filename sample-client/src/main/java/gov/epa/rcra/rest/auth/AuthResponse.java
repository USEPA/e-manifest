package gov.epa.rcra.rest.auth;

import java.time.ZonedDateTime;

record AuthResponse(String token, ZonedDateTime expiration) {
}