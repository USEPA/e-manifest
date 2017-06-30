package gov.epa.rcra.web.rest.api.client.auth;

import java.util.Date;

public class AuthResponse {

	protected String token;
	protected Date expiration;

	public String getToken() {
		return token;
	}

	public void setToken(String token) {
		this.token = token;
	}

	public Date getExpiration() {
		return expiration;
	}

	public void setExpiration(Date expiration) {
		this.expiration = expiration;
	}

}
