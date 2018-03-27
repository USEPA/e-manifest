package gov.epa.rcra.web.rest.api.client.manifest;

import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.List;

import javax.ws.rs.client.ClientBuilder;
import javax.ws.rs.client.Entity;
import javax.ws.rs.client.Invocation;
import javax.ws.rs.client.WebTarget;
import javax.ws.rs.core.GenericType;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import org.apache.commons.io.FileUtils;
import org.apache.commons.io.IOUtils;
import org.apache.commons.lang3.StringUtils;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.glassfish.jersey.client.ClientConfig;
import org.glassfish.jersey.filter.LoggingFilter;
import org.glassfish.jersey.jackson.JacksonFeature;
import org.glassfish.jersey.media.multipart.BodyPart;
import org.glassfish.jersey.media.multipart.FormDataMultiPart;
import org.glassfish.jersey.media.multipart.MultiPart;
import org.glassfish.jersey.media.multipart.MultiPartFeature;
import org.glassfish.jersey.media.multipart.MultiPartMediaTypes;
import org.glassfish.jersey.media.multipart.file.FileDataBodyPart;
import org.glassfish.jersey.uri.UriComponent;


import gov.epa.rcra.web.rest.api.client.BaseServicesClient;

/**
 * @author sergey
 */
public class ManifestServiceClient extends BaseServicesClient {
	private static final Log logger = LogFactory.getLog(ManifestServiceClient.class);

	protected String outputDir;
	
	public ManifestServiceClient(String restBase, String token) {
		this.restBase = restBase+"/emanifest";
		this.token = token;
	}
	
	public void executeMultipart(String path, String outputDir) {
		this.outputDir = outputDir;
		client = ClientBuilder.newClient(new ClientConfig()
				.register(LoggingFilter.class)).
				 register(JacksonFeature.class)
				 .register(MultiPartFeature.class);
		
		WebTarget webTarget = client.target(restBase).path(UriComponent.encode(path,UriComponent.Type.PATH));
		Invocation.Builder invocationBuilder = webTarget
				.request(MultiPartMediaTypes.MULTIPART_MIXED)
				.accept(MultiPartMediaTypes.MULTIPART_MIXED);
		invocationBuilder.header("Authorization", "Bearer " + token);
		Response resp = invocationBuilder.get();
		MultiPart multiPart = resp.readEntity(MultiPart.class);
		if (StringUtils.isBlank(outputDir)) {
			outputDir = System.getProperty("java.io.tmpdir");
		}
		logger.info("Saving attachments to: "+outputDir);
		for (BodyPart bp : multiPart.getBodyParts()){
			InputStream in = null;
			OutputStream out = null; 
			try {
				if (MediaType.APPLICATION_JSON_TYPE.equals(bp.getMediaType())) {
					//logger.info(bp.getEntityAs(String.class));
					FileUtils.writeStringToFile(new File(outputDir+File.separator+"manifest.json"), bp.getEntityAs(String.class));
				} else {
						in = bp.getEntityAs(InputStream.class);
						out = new BufferedOutputStream(new FileOutputStream(new File(outputDir+File.separator+"attachments.zip")));
						IOUtils.copy(in, out);
				}
			} catch (Throwable e) {
				logger.error("Error while executing get-with-attachments",e);
			}
			finally {
				IOUtils.closeQuietly(in);
				IOUtils.closeQuietly(out);
			}
		}
	}

	public void executeSave(String servicePath, String jsonPath, String attachmentPath) {
		try {
			String manifest = FileUtils.readFileToString(new File(jsonPath));
			client = ClientBuilder.newClient(new ClientConfig()
					.register(LoggingFilter.class)).
					 register(JacksonFeature.class)
					 .register(MultiPartFeature.class);
			
			WebTarget webTarget = client.target(restBase).path(UriComponent.encode(servicePath,UriComponent.Type.PATH));
	
			Invocation.Builder invocationBuilder = webTarget
					.request(MediaType.MULTIPART_FORM_DATA)
					.accept(MediaType.APPLICATION_JSON);
			invocationBuilder.header("Authorization", "Bearer " + token);
			MultiPart multipartEntity = null;
			if (attachmentPath != null) {
		        FileDataBodyPart fileDataBodyPart = new FileDataBodyPart("attachment",
		                new File(attachmentPath), MediaType.APPLICATION_OCTET_STREAM_TYPE);
				multipartEntity = new FormDataMultiPart()
			            .field("manifest", manifest, MediaType.APPLICATION_JSON_TYPE)
			            .bodyPart(fileDataBodyPart);
			} else {
				multipartEntity = new FormDataMultiPart()
			            .field("manifest", manifest, MediaType.APPLICATION_JSON_TYPE);			
			}
			
			Response response = invocationBuilder.post(
		            Entity.entity(multipartEntity, multipartEntity.getMediaType()));
			logger.info(response.readEntity(String.class));
		} catch (Throwable e) {
			logger.error("Error while executing save",e);
		}		
	}
	
	public void executeSearch(String servicePath, String jsonPath) {
		try {
			String criteria = FileUtils.readFileToString(new File(jsonPath));
			client = ClientBuilder.newClient(new ClientConfig()
					.register(LoggingFilter.class)).
					 register(JacksonFeature.class);
			
			WebTarget webTarget = client.target(restBase).path(UriComponent.encode(servicePath,UriComponent.Type.PATH));
			GenericType<List> genericType = new GenericType<List>(){};	
			Invocation.Builder invocationBuilder = webTarget
					.request(MediaType.TEXT_PLAIN)
					.accept(MediaType.APPLICATION_JSON);
			invocationBuilder.header("Authorization", "Bearer " + token);
			List response = invocationBuilder.post(
		            Entity.text(criteria),genericType);
			logger.info(response);
		} catch (Throwable e) {
			logger.error("Error while executing search",e);
		}		
	}
	
}