<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="stripes" uri="http://stripes.sourceforge.net/stripes-dynattr.tld" %>
<%@ taglib prefix="display" uri="http://displaytag.sf.net/el" %>
<%@ taglib prefix="security" uri="http://www.springframework.org/security/tags" %>
<stripes:layout-render name="/industry/secured/modules/emanifest/common/modal-layout.jsp" title="Waste" addClass="modal-lg modal-xlg" id="manifestWasteSectionModal">
	<stripes:layout-component name="body">
		<!-- ko if: waste -->
		<div class="row">
			<div class="col-sm-12">
				<div class="form-group required" data-bind="with: waste">
					<label class="control-label" for="hazWaste"> 9a. Hazardous Material? </label>
					<span class="static-info help-block" data-bind="text: isHazardous() ? 'Yes' : 'No'"></span>
				</div>
			</div>
		</div>
		<div class="panel panel-default panel-info">
			<div class="panel-heading">9b. U.S. DOT Description</div>
			<div class="panel-body">
				<dot-description-review params="data: waste()"></dot-description-review>
			</div>
		</div>
		<div class="panel panel-default panel-info">
			<div class="panel-heading">10-12. Containers and Quantity</div>
			<div class="panel-body">
				<containers-review params="data: waste()"></containers-review>
			</div>
		</div>
		<div class="panel panel-default panel-info">
			<div class="panel-heading">13. Hazardous Waste Codes</div>
			<div class="panel-body">
				<waste-codes-review params="data: waste()"></waste-codes-review>
			</div>
		</div>
		<div class="panel panel-default panel-info">
			<div class="panel-heading">Special Handling Instructions and Additional Information</div>
			<div class="panel-body">
				<waste-handling-instructions-review params="data: waste(), internationalShipment: internationalShipment"></waste-handling-instructions-review>
			</div>
		</div>
		<!-- /ko -->
	</stripes:layout-component>
	<stripes:layout-component name="footer">
		<button type="button" class="btn btn-default pull-left"
			data-bind="close: 'waste-close'">Close</button>
	</stripes:layout-component>
</stripes:layout-render>