package gov.epa.rcra.web.rest.api.client.cli.commands;

import javax.ws.rs.core.NewCookie;

import org.apache.commons.lang3.StringUtils;

import com.beust.jcommander.Parameter;
import com.beust.jcommander.Parameters;

import gov.epa.rcra.web.rest.api.client.auth.AuthServiceClient;

@Parameters(commandDescription="Authenticate",commandNames="auth")
public class AuthenticateCommand extends BaseCommand {
	
	@Parameter(names = { "--api-id"}, description = "API Id", required=true,help=true)
	private String apiId;
	
	@Parameter(names = { "--api-key"}, description = "API Key", required=true,help=true)
	private String apiKey;

	@Parameter(names = { "--url"}, description = "Main Services End Point", required=true,help=true)
	private String url;
	
	protected AuthServiceClient client;
	
	public String getApiId() {
		return apiId;
	}

	public void setApiId(String apiId) {
		this.apiId = apiId;
	}

	public String getApiKey() {
		return apiKey;
	}

	public void setApiKey(String apiKey) {
		this.apiKey = apiKey;
	}

	public String getUrl() {
		return url;
	}

	public void setUrl(String url) {
		this.url = url;
	}

	public void run () {
		if (StringUtils.isNotBlank(apiId) && StringUtils.isNotBlank(apiKey) && 
				StringUtils.isNotBlank("url")) {
			AuthServiceClient client = new AuthServiceClient(apiId,
					apiKey, url);
			client.authenticate();
		} else {
			throw new IllegalArgumentException("api id, key and url required");
		}
	}
	
	private NewCookie c;
	
	public NewCookie getCookie() {
		return c;
	}
	
}
