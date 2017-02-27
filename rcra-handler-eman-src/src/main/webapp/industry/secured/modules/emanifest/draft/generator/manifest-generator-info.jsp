<%@ taglib prefix="stripes" uri="http://stripes.sourceforge.net/stripes-dynattr.tld" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<stripes:layout-definition>
<div class="panel panel-default panel-info" data-bind="with: generator">
	<div class="panel-heading">1-5. Generator Information</div>
	<div class="panel-body">
		<facility-info params="facilityInfo: $data"></facility-info>
	</div>	
</div>
</stripes:layout-definition>