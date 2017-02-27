<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="stripes" uri="http://stripes.sourceforge.net/stripes-dynattr.tld" %>
<%@ taglib prefix="display" uri="http://displaytag.sf.net/el" %>
<%@ taglib prefix="security" uri="http://www.springframework.org/security/tags" %>
<c:choose>
	<c:when test="${actionBean.tsdf }">
		<c:set var="tempRole" value="tsdf"></c:set>
		<c:set var="fakeTsdfHandlerId" value="OHR000116806"/>
	</c:when>
	<c:otherwise>
		<c:set var="tempRole" value="generator"></c:set>
	</c:otherwise>
</c:choose>
<stripes:layout-render name="/industry/secured/modules/common/layout-dashboard.jsp" title="e-Manifest Home" tab="emanifest">
	<stripes:layout-component name="additionalHead">
		<script>
			//TODO move this somewhere else
			var ctx = "${pageContext.request.contextPath}";
		</script>
		<script src="${pageContext.request.contextPath}/static/js/emanifest.js"></script>
		<script>
			var inprogressDataTable;
			var receivedDataTable;
			$(function() {
				var handlerId = '${actionBean.handlerId}';
				inprogressDataTable = ${actionBean.tsdf} ? tsdfInprogressTable() : generatorInprogressTable();
				receivedDataTable = ${actionBean.tsdf} ? tsdfReceivedTable() : generatorReceivedTable();
				var HandlerViewModel = function(data) {
					var self = this;
					ko.mapping.fromJS(data, {}, self);
				}
				var TsdfViewModel = function(data) {
					var self = this;
					self.filter = ko.observableArray([
						"Incoming",
						"Outgoing"
					]);
					self.selectedFilter = ko.observable("Incoming");
					self.selectedFilter.subscribe(function(newFilter) {
						self.updateTables(newFilter);
					});
					self.updateTables = function(newFilter) {
						if(newFilter === "Incoming") {
							inprogressDataTable.column(1).visible(true);
							inprogressDataTable.column(2).visible(true);
							inprogressDataTable.column(3).visible(false);
							inprogressDataTable.column(4).visible(false);
							receivedDataTable.column(1).visible(true);
							receivedDataTable.column(2).visible(true);
							receivedDataTable.column(3).visible(false);
							receivedDataTable.column(4).visible(false);
							inprogressDataTable.columns(1).search('').draw();
							receivedDataTable.columns(1).search('').draw();
							inprogressDataTable.columns(3).search('${fakeTsdfHandlerId}').draw();
							receivedDataTable.columns(3).search('${fakeTsdfHandlerId}').draw();
						}
						else if(newFilter === "Outgoing") {
							inprogressDataTable.column(1).visible(false);
							inprogressDataTable.column(2).visible(false);
							inprogressDataTable.column(3).visible(true);
							inprogressDataTable.column(4).visible(true);
							receivedDataTable.column(1).visible(false);
							receivedDataTable.column(2).visible(false);
							receivedDataTable.column(3).visible(true);
							receivedDataTable.column(4).visible(true);
							inprogressDataTable.columns(3).search('').draw();
							receivedDataTable.columns(3).search('').draw();
							inprogressDataTable.columns(1).search('${fakeTsdfHandlerId}').draw();
							receivedDataTable.columns(1).search('${fakeTsdfHandlerId}').draw();
						}
					}
					self.updateTables(self.selectedFilter());
				}
				var GeneratorViewModel = function() {
					var self = this;
				}
				var vm = ${actionBean.tsdf} ? new TsdfViewModel() : new GeneratorViewModel();
				ko.applyBindings(vm, $('#dashboard-content').get(0));
			});
			function tsdfInprogressTable() {
				return $('#manifests-inprogress').DataTable({
					searching: true,
					responsive: true,
					lengthChange: true,
					ajax: '${pageContext.request.contextPath}/static/json/industry/emanifest/manifests-inprogress-${tempRole}.json',
					columns: [
						{
							"orderable": true,
							"data": "manifestTrackingNumber",
							"width": "90px"
						},
						{
							"orderable": true,
							"data": "generator.epaSiteId",
							"width": "92px"
						},
						{
							"orderable": true,
							"data": "generator.siteName",
							"render": function(data, type, full, meta) {
								var truncated = rcra.truncate(data, 60);
								return '<span title="' + data + '">' + truncated + '</span>';
							}
						},
						{
							"orderable": true,
							"data": "tsdf.epaSiteId",
							"width": "92px"
						},
						{
							"orderable": true,
							"data": "tsdf.siteName",
							"render": function(data, type, full, meta) {
								var truncated = rcra.truncate(data, 60);
								return '<span title="' + data + '">' + truncated + '</span>';
							}
						},
						{
							"orderable": true,
							"data": "updatedDate",
							"render": function(data, type, full, meta) {
								return '<span title="' + full.updatedBy.firstName + ' ' + full.updatedBy.lastName + '">' + data + '</span>';
							},
							"width": "135px"
						},
						{
							"orderable": true,
							"data": "status.code",
							"width": "45px"
						},
						{
							"orderable": false,
							"data": "status",
							"render": function(data, type, full, meta) {
								var actions = '<a href="${pageContext.request.contextPath}/action/industry/secured/e-manifest/drafts/${actionBean.handlerId}/' + full.manifestTrackingNumber + '?tsdf=true#!/manifest?trackingNum=' + full.manifestTrackingNumber + '/edit"><span class="glyphicon glyphicon-pencil" title="Edit"></span></a>';
								actions += ' <a href="#"><span class="glyphicon glyphicon-duplicate" title="Copy"></span></a>';
								return actions
							},
							"width": "70px"
						}
					],
					language: {
						"emptyTable": "No manifests are currently in progress."
					},
					order: [[5, "desc"]]
				});
			}
			function tsdfReceivedTable() {
				return $('#manifests-received').DataTable({
					searching: true,
					responsive: true,
					lengthChange: true,
					ajax: '${pageContext.request.contextPath}/static/json/industry/emanifest/manifests-received-${tempRole}.json',
					columns: [
						{
							"orderable": true,
							"data": "manifestTrackingNumber",
							"width": "90px"
						},
						{
							"orderable": true,
							"data": "generator.epaSiteId",
							"width": "92px"
						},
						{
							"orderable": true,
							"data": "generator.siteName",
							"render": function(data, type, full, meta) {
								var truncated = rcra.truncate(data, 60);
								return '<span title="' + data + '">' + truncated + '</span>';
							}
						},
						{
							"orderable": true,
							"data": "tsdf.epaSiteId",
							"width": "92px"
						},
						{
							"orderable": true,
							"data": "tsdf.siteName",
							"render": function(data, type, full, meta) {
								var truncated = rcra.truncate(data, 60);
								return '<span title="' + data + '">' + truncated + '</span>';
							}
						},
						{
							"orderable": true,
							"data": "updatedDate",
							"render": function(data, type, full, meta) {
								return '<span title="' + full.updatedBy.firstName + ' ' + full.updatedBy.lastName + '">' + data + '</span>';
							},
							"width": "135px"
						},
						{
							"orderable": true,
							"data": "status.description",
							"width": "45px"
						},
						{
							"orderable": false,
							"render": function(data, type, full, meta) {
								return '<a href="#"><span class="glyphicon glyphicon-eye-open" title="View"></span></a>' +
										' <a href="#"><span class="glyphicon glyphicon-pencil" title="Edit"></span></a>' +
										' <a href="#"><span class="glyphicon glyphicon-duplicate" title="Copy"></span></a>';
							},
							"width": "70px"
						}
					],
					language: {
						"emptyTable": "No manifests have been recieved."
					},
					order: [[5, "desc"]]
				});
			}
			function generatorInprogressTable() {
				return $('#manifests-inprogress').DataTable({
					searching: true,
					responsive: true,
					lengthChange: true,
					ajax: '${pageContext.request.contextPath}/static/json/industry/emanifest/manifests-inprogress-${tempRole}.json',
					columns: [
						{
							"orderable": true,
							"data": "manifestTrackingNumber",
							"width": "90px"
						},
						{
							"orderable": true,
							"data": "tsdf.epaSiteId",
							"width": "92px"
						},
						{
							"orderable": true,
							"data": "tsdf.siteName",
							"render": function(data, type, full, meta) {
								var truncated = rcra.truncate(data, 60);
								return '<span title="' + data + '">' + truncated + '</span>';
							}
						},
						{
							"orderable": true,
							"data": "updatedDate",
							"render": function(data, type, full, meta) {
								return '<span title="' + full.updatedBy.firstName + ' ' + full.updatedBy.lastName + '">' + data + '</span>';
							},
							"width": "135px"
						},
						{
							"orderable": true,
							"data": "status.code",
							"width": "45px"
						},
						{
							"orderable": false,
							"data": "status",
							"render": function(data, type, full, meta) {
								var manifestUrl = '${pageContext.request.contextPath}/action/industry/secured/e-manifest/drafts/${actionBean.handlerId}/' + full.manifestTrackingNumber + '#!/manifest?trackingNum=' + full.manifestTrackingNumber;
								var actions = '';
								if(data.order <= 3) {
									actions += '<a href="' + manifestUrl + '/edit"><span class="glyphicon glyphicon-pencil" title="Edit"></span></a>';
								}
								else {
									actions += '<a href="' + manifestUrl + '/review"><span class="glyphicon glyphicon-eye-open" title="View"></span></a>';
								}
								actions += ' <a href="#"><span class="glyphicon glyphicon-duplicate" title="Copy"></span></a>';
								return actions
							},
							"width": "70px"
						}
					],
					language: {
						"emptyTable": "No manifests are currently in progress."
					},
					order: [[3, "desc"]]
				});
			}
			function generatorReceivedTable() {
				return $('#manifests-received').DataTable({
					searching: true,
					responsive: true,
					lengthChange: true,
					ajax: '${pageContext.request.contextPath}/static/json/industry/emanifest/manifests-received-${tempRole}.json',
					columns: [
						{
							"orderable": true,
							"data": "manifestTrackingNumber",
							"width": "90px"
						},
						{
							"orderable": true,
							"data": "tsdf.epaSiteId",
							"width": "92px"
						},
						{
							"orderable": true,
							"data": "tsdf.siteName",
							"render": function(data, type, full, meta) {
								var truncated = rcra.truncate(data, 60);
								return '<span title="' + data + '">' + truncated + '</span>';
							}
						},
						{
							"orderable": true,
							"data": "updatedDate",
							"render": function(data, type, full, meta) {
								return '<span title="' + full.updatedBy.firstName + ' ' + full.updatedBy.lastName + '">' + data + '</span>';
							},
							"width": "135px"
						},
						{
							"orderable": true,
							"data": "status.description",
							"width": "45px"
						},
						{
							"orderable": false,
							"render": function(data, type, full, meta) {
								return '<a href="#"><span class="glyphicon glyphicon-eye-open" title="View"></span></a>' +
										' <a href="#"><span class="glyphicon glyphicon-duplicate" title="Copy"></span></a>';
							},
							"width": "70px"
						}
					],
					language: {
						"emptyTable": "No manifests have been recieved."
					},
					order: [[3, "desc"]]
				});
			}
		</script>
		<style>
			.role-view {
				text-align: right;
			}
			td .glyphicon {
				margin-right: 5px;
			}
		</style>
	</stripes:layout-component>
    <stripes:layout-component name="breadCrumbs">
        <ol class="breadcrumb">
			<li><a href="${pageContext.request.contextPath}/action/industry/secured/home">My Sites</a></li>
			<li><a href="${pageContext.request.contextPath}/action/industry/secured/sites/details/${actionBean.handlerId}">${actionBean.handlerId}</a></li>
            <li class="active">e-Manifest Dashboard</li>
        </ol>
    </stripes:layout-component>
    <stripes:layout-component name="tabContent">
		<c:choose>
			<c:when test="${actionBean.tsdf}">
				<a href="?tsdf=false" class="pull-left">Generator View (Beta Version)</a>
			</c:when>
			<c:otherwise>
				<a href="?tsdf=true" style="display:block; height: 25.5px">TSDF View (Beta Version)</a>
			</c:otherwise>
		</c:choose>
    	<c:if test="${actionBean.tsdf }">
	    	<div class="role-view">
	    		<label for="role">Filter:</label>
	    		<select id="role" data-bind="options: filter, value: selectedFilter"></select>
	    	</div>
    	</c:if>
		<div class="panel panel-default">
    		<div class="panel-heading">In Progress</div>
    		<div class="panel-body">
    			<table id="manifests-inprogress" class="table table-striped table-bordered" style="width: 100%">
    				<thead>
	    				<tr class="info">
	    					<th>Manifest ID#</th>
	    					<c:if test="${actionBean.tsdf }">
		    					<th>Generator ID</th>
		    					<th>Generator Name</th>
	    					</c:if>
	    					<th>TSDF ID</th>
	    					<th>TSDF Name</th>
	    					<th>Last Updated Date</th>
	    					<th>Status</th>
	    					<th>Actions</th>
	    				</tr>
    				</thead>
    				<tbody></tbody>
    			</table>
    			<div class="btn-group">
					<a href="${pageContext.request.contextPath}/action/industry/secured/e-manifest/drafts/${actionBean.handlerId}/?tsdf=${actionBean.tsdf}#!/manifest/edit" class="btn btn-success">
						Create New Manifest
					</a>
				</div>
    		</div>
    	</div>
    	<div class="panel panel-default">
    		<div class="panel-heading">Received</div>
    		<div class="panel-body">
    			<table id="manifests-received" class="table table-striped table-bordered" style="width: 100%">
    				<thead>
	    				<tr class="info">
	    					<th>Manifest ID#</th>
	    					<c:if test="${actionBean.tsdf }">
		    					<th>Generator ID</th>
		    					<th>Generator Name</th>
	    					</c:if>
	    					<th>TSDF ID</th>
	    					<th>TSDF Name</th>
	    					<th>Last Updated Date</th>
	    					<th>Status</th>
	    					<th>Actions</th>
	    				</tr>
    				</thead>
    				<tbody></tbody>
    			</table>
    		</div>
    	</div>
<%--     	<c:choose> --%>
<%--     		<c:when test="${actionBean.tsdf }"> --%>
<!--     			<a href="?tsdf=false">View as Generator (this is for mockups only and will be removed later)</a> -->
<%--     		</c:when> --%>
<%--     		<c:otherwise> --%>
<!--     			<a href="?tsdf=true">View as TSDF (this is for mockups only and will be removed later)</a> -->
<%--     		</c:otherwise> --%>
<%--     	</c:choose> --%>
	</stripes:layout-component>
</stripes:layout-render>