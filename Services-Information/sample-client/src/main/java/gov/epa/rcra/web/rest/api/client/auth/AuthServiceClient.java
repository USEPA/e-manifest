package gov.epa.rcra.web.rest.api.client.auth;

import java.io.File;
import java.util.Properties;

import javax.ws.rs.client.Invocation;
import javax.ws.rs.client.WebTarget;
import javax.ws.rs.core.GenericType;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.Response.Status;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import gov.epa.rcra.web.rest.api.client.BaseServicesClient;

/**
 * @author sergey
 */
public class AuthServiceClient extends BaseServicesClient {
	private static final Log logger = LogFactory.getLog(AuthServiceClient.class);
	

	protected String restBase;
	protected String apiId;
	protected String apiKey;
	

	public AuthServiceClient(String apiId, String apiKey,String restEndpointBase) {
		super();
		restBase = restEndpointBase;
		this.apiId = apiId;
		this.apiKey = apiKey;
		
	}
	
	public void authenticate() {

		try {
			GenericType<AuthResponse> genericType = new GenericType<AuthResponse>(){};			
			WebTarget authTarget = client.target(restBase).path("auth")
					.path(apiId)
					.path(apiKey);
			Invocation.Builder invocationBuilder = authTarget
					.request(MediaType.APPLICATION_JSON_TYPE)
					.accept(MediaType.APPLICATION_JSON_TYPE);
			Response response = invocationBuilder.get();
			handleAuthResponse(genericType, response);
		} catch (Throwable e) {
			logger.error("Error during authentication",e);
		}
	}
	
	
	
	protected void  handleAuthResponse(GenericType<AuthResponse> genericType, Response response) {
		if (Status.OK.getStatusCode() == response.getStatus()) {
			AuthResponse resp = response.readEntity(genericType);
			Properties p = new Properties();
			p.put("baseUrl", restBase);
			p.put("token", resp.getToken());
			File f = AuthInfoLoader.save(p);
			logger.info("Authenticated successfully");				
			logger.info("Token stored in: "+f.getAbsolutePath());				
		} else {
			logger.info("Failed authentication");			
			logger.info(response.readEntity(String.class));
		}
	}
	

}
