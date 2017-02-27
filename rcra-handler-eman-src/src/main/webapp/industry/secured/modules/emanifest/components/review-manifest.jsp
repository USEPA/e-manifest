<!-- ko if: formLoaded -->
<div class="panel panel-info">
	<div class="panel-heading">
		<span>General Information</span>
		<span class="pull-right">
			<a href="JavaScript:;"><span class="glyphicon glyphicon-share"></span></a>
			<a href="${pageContext.request.contextPath}/static/docs/ManifestBlank.pdf" target="_blank"
			   data-bind="attr: {title: printTitle}">
                <span class="glyphicon glyphicon-print"></span>
            </a>
			<a href="JavaScript:;" data-bind="popover: {
			            options: { title: 'Revision History Details', placement: 'bottom' },
			            template: 'eman-revision-history',
			            data: $data
			            }"
			   class="unsavedCheckIgnore">
			 	<span class="glyphicon glyphicon-list" aria-hidden="true"></span>
			</a>
		</span>
	</div>
	<div class="panel-body">
		<general-info-review params="form: $data"></general-info-review>
	</div>
</div>
<div class="panel panel-info" data-bind="with: generator">
	<div class="panel-heading">1-5. Generator Information</div>
	<div class="panel-body">
		<facility-info-review params="facilityInfo: $data"></facility-info-review>
	</div>
</div>
<div class="panel panel-info">
	<div class="panel-heading">6-7. Transporter Information</div>
	<div class="panel-body">
		<transporter-review params="form: $data"></transporter-review>
	</div>
</div>
<div class="panel panel-info" data-bind="with: tsdf">
	<div class="panel-heading">8. Designated Facility Information</div>
	<div class="panel-body">
		<facility-info-review params="facilityInfo: $data, emergencyPhoneVisible: false"></facility-info-review>
	</div>
</div>
<div class="panel panel-info">
	<div class="panel-heading">9-13. Waste Information</div>
	<div class="panel-body">
		<waste-section-review params="form: $data"></waste-section-review>
	</div>
</div>
<div class="panel panel-info">
	<div class="panel-heading">14. Special Handling Instructions and Additional Information</div>
	<div class="panel-body">
		<handling-instructions-review params="form: $data"></handling-instructions-review>
	</div>
</div>
<div class="panel panel-info" data-bind="with: internationalShipmentInfo, slideVisible: internationalShipment">
	<div class="panel-heading">16. International Shipment Information</div>
	<div class="panel-body">
		<international-shipment-review params="form: $data"></international-shipment-review>
	</div>
</div>
<div class="form-inline">
	<div class="row" style="margin-bottom: 15px">
		<div id="manifestButtonToolbar" class="col-sm-12 btn-toolbar">
			<!-- ko if: role == 'tsdf' -->
			<button class="btn btn-primary btn-lg" type="button" data-bind="click: function(){alert('Cromerr widget will go here later');}">Sign</button>
			<a href="../edit" type="button" class="btn btn-success btn-lg unsavedCheckIgnore" data-bind="page-href: '../edit'">Make Changes</a>
			<!-- /ko -->
			<a type="button" class="btn btn-default btn-lg" data-bind="attr: {
                            href: '${pageContext.request.contextPath}/action/industry/secured/e-manifest/home/' + rcra.emanifest.handlerId
                         }">Back to Dashboard</a>
		</div>
	</div>	
</div>
<!-- /ko -->