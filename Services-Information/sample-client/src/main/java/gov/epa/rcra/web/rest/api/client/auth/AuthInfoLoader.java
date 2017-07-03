package gov.epa.rcra.web.rest.api.client.auth;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.util.Properties;

import org.apache.commons.io.IOUtils;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

public class AuthInfoLoader {

	private static final Log logger = LogFactory.getLog(AuthInfoLoader.class);

	public static final String CONF_DIR_PATH ="conf";
	public static final String TOKEN_FILE_PATH = "eman-token.txt";
	
	
	public static File save (Properties props) {
		FileOutputStream out = null;
		File tokenFile = null;
		try {
			File confDir = new File(CONF_DIR_PATH);
			confDir.mkdirs();
			tokenFile = new File(confDir,TOKEN_FILE_PATH);				
			props.store(new FileOutputStream(tokenFile), "");			
		} catch (Throwable e) {
			logger.error(e);
		}
		finally {
			if (out != null) {
				IOUtils.closeQuietly(out);
			}
		}
		return tokenFile; 
	}
	
	public static Properties load() {
		FileInputStream in = null;
		Properties p = new Properties();
		try {
			File tokenFile = new File(CONF_DIR_PATH,TOKEN_FILE_PATH);
			p = new Properties();
			p.load(in = new FileInputStream(tokenFile));			
		} catch (Throwable e) {
			logger.error(e);
		} finally {
			if (in != null) {
				IOUtils.closeQuietly(in);
			}
		}
		if (p.size() != 2 || p.getProperty("baseUrl") == null || p.getProperty("token") == null ) {
			throw new IllegalArgumentException("No valid auth info found, please run auth command first.");
		}		
		return p;

	}
}
