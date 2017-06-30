package gov.epa.rcra.web.rest.api.client;

import javax.ws.rs.client.Client;
import javax.ws.rs.client.ClientBuilder;
import javax.ws.rs.client.Invocation;
import javax.ws.rs.client.WebTarget;
import javax.ws.rs.core.GenericType;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.glassfish.jersey.client.ClientConfig;
import org.glassfish.jersey.filter.LoggingFilter;
import org.glassfish.jersey.jackson.JacksonFeature;

public class BaseServicesClient {

	private static final Log logger = LogFactory.getLog(BaseServicesClient.class);

	protected String restBase;
	protected Client client;
	protected String token;
	

	
	public String getToken() {
		return token;
	}

	public void setToken(String token) {
		this.token = token;
	}

	public BaseServicesClient () {
		client = ClientBuilder.newClient(new ClientConfig()
				.register(LoggingFilter.class)).
				 register(JacksonFeature.class);		
	}

	public Client getClient() {
		return client;
	}

	public void setClient(Client client) {
		this.client = client;
	}

	public String getRestBase() {
		return restBase;
	}

	public void setRestBase(String restBase) {
		this.restBase = restBase;
	}
	
	
	protected <T extends Object> void  handleResponse(GenericType<T> genericType, Response response) {
		logger.info(response.readEntity(genericType));
	}

	public void execute(String path) {
	
		client = ClientBuilder.newClient(new ClientConfig()
				.register(LoggingFilter.class)).
				 register(JacksonFeature.class);
		GenericType<String> genericType = new GenericType<String>(){};
		
		WebTarget webTarget = client.target(restBase).path(path);
		Invocation.Builder invocationBuilder = webTarget
				.request(MediaType.APPLICATION_JSON_TYPE)
				.accept(MediaType.APPLICATION_JSON_TYPE);
		invocationBuilder.header("Authorization", "Bearer " + token);
		logger.info(invocationBuilder.get(genericType));
	}
	

	

}
