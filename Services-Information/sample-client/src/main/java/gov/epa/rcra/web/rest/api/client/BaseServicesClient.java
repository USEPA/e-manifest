package gov.epa.rcra.web.rest.api.client;

import javax.ws.rs.client.Client;
import javax.ws.rs.client.ClientBuilder;
import javax.ws.rs.client.Invocation;
import javax.ws.rs.client.WebTarget;
import javax.ws.rs.core.MediaType;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.glassfish.jersey.client.ClientConfig;
import org.glassfish.jersey.filter.LoggingFilter;
import org.glassfish.jersey.jackson.JacksonFeature;
import org.glassfish.jersey.uri.UriComponent;

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
	
	
	public void execute(String path) {
	
		client = ClientBuilder.newClient(new ClientConfig()
				.register(LoggingFilter.class)).
				 register(JacksonFeature.class);
		
		WebTarget webTarget = client.target(restBase).path(UriComponent.encode(path,UriComponent.Type.PATH));
		Invocation.Builder invocationBuilder = webTarget
				.request(MediaType.APPLICATION_JSON_TYPE)
				.accept(MediaType.APPLICATION_JSON_TYPE);
		invocationBuilder.header("Authorization", "Bearer " + token);
		logger.info(invocationBuilder.get().readEntity(String.class));
	}
	

	

}
