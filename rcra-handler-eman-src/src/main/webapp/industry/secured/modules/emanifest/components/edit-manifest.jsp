<script type="text/html" id="bs-switch">
    <div style="height: 34px; display: inline-block">
        <input id="international-shipment" class="switch switch-lg" type="checkbox"
               data-bind="attr:{readonly: $data.enable != undefined ? !enable : false},
                          bootstrapSwitchOn: flag"
               data-on-text="Yes" data-off-text="No"/>
    </div>
</script>
<!-- ko if: formLoaded -->
<eman-progress-bar params="currentStatus: currentStatus">
    <div id="eman-progress-bar"></div>
</eman-progress-bar>
<div class="panel panel-default panel-info">
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
        <!-- ko if: generatorPartialEdit-->
        <general-info-review params="tsdf: role == 'tsdf', form: $data"></general-info-review>
        <!-- /ko -->
        <!-- ko ifnot: generatorPartialEdit -->
        <general-info params="tsdf: role == 'tsdf', form: $data"></general-info>
        <!-- /ko -->
    </div>
</div>
<div class="panel panel-default panel-info">
    <div class="panel-heading">1-5. Generator Information</div>
    <div class="panel-body">
        <!-- ko ifnot: $parent.role == "tsdf" -->
            <generator-info-generator params="form: $data"></generator-info-generator>
        <!-- /ko -->
        <!-- ko if: $parent.role == "tsdf" -->
            <generator-info-tsdf params="form: $data"></generator-info-tsdf>
        <!-- /ko -->
    </div>
</div>
<div class="panel panel-default panel-info">
    <div class="panel-heading">6-7. Transporter Information</div>
    <div class="panel-body">
        <!-- ko if: generatorPartialEdit-->
        <transporter-review params="form: $data"></transporter-review>
        <!-- /ko -->
        <!-- ko ifnot: generatorPartialEdit-->
        <transporter params="form: $data"></transporter>
        <!-- /ko -->
    </div>
</div>
<div class="panel panel-default panel-info">
    <div class="panel-heading">8. Designated Facility Information</div>
    <div class="panel-body">
        <!-- ko if: role == "tsdf" -->
            <tsdf-info-tsdf params="form: $data"></tsdf-info-tsdf>
        <!-- /ko -->
        <!-- ko ifnot: role == "tsdf" -->
            <tsdf-info-generator params="form: $data"></tsdf-info-generator>
        <!-- /ko -->
    </div>
</div>
<div class="panel panel-default panel-info" id="waste-information-section">
    <div class="panel-heading">9-13. Waste Information</div>
    <div class="panel-body">
        <waste-section params="form: $data"></waste-section>
    </div>
</div>

<div class="panel panel-default panel-info">
    <div class="panel-heading">14. Special Handling Instructions and Additional Information</div>
    <div class="panel-body">
        <handling-instructions params="form: $data"></handling-instructions>
    </div>
</div>
<div class="panel panel-info" data-bind="if: status().code() == 'Received', slideVisible: status().code() == 'Received'">
    <div class="panel-heading">15. Generator's / Offeror's Certification</div>
    <div class="panel-body">
        <signator-section params="site: generator, siteType: 'Generator\'s / Offeror\'s'"></signator-section>
    </div>
</div>
<div class="panel panel-default panel-info"
     data-bind="with: internationalShipmentInfo, slideVisible: internationalShipment">
    <div class="panel-heading">16. International Shipment Information</div>
    <div class="panel-body">
        <international-shipment params="form: $data"></international-shipment>
    </div>
</div>
<div class="panel panel-info" data-bind="if: status().code() == 'Received', slideVisible: status().code() == 'Received'">
    <div class="panel-heading">17. Transporter Acknowledgement of Receipt of Materials</div>
    <div class="panel-body">
        <!-- ko foreach: transporters -->
        <signator-section params="site: $data, siteType: 'Transporter'"></signator-section>
        <!-- /ko -->
    </div>
</div>
<div class="panel panel-default panel-info" data-bind="if: status().code() == 'Received', slideVisible: status().code() == 'Received'">
    <div class="panel-heading">18. Discrepancy</div>
    <div class="panel-body">
        <discrepancy-section params="form: $data"></discrepancy-section>
    </div>
</div>
<div class="panel panel-info" data-bind="if: status().code() == 'Received', slideVisible: status().code() == 'Received'">
    <div class="panel-heading">19. Hazardous Waste Management Method Codes</div>
    <div class="panel-body">
        <p class="help-block">Add or edit codes in Waste Characteristics table in <a href="JavaScript:scrollToElement('#waste-information-section');">"Section 9-13. Waste Information"</a></p>
    </div>
</div>
<div class="form-inline" data-bind="validationOptions: {insertMessages: false}">
    <div class="row" style="margin-bottom: 15px">
        <div id="manifestButtonToolbar" class="col-sm-12 btn-toolbar">
            <button type="button" class="btn btn-primary btn-lg" data-bind="click: save">Save</button>
            <!-- ko if: currentStatus().code() == 'Received' -->
            <%--<button type="button" class="btn btn-primary btn-lg" data-bind="click: reviewManifest">Review</button>--%>
            <!-- /ko -->
            <!-- ko if: currentStatus().order() < 4 -->
            <button type="button" class="btn btn-danger btn-lg" data-bind="click: deleteManifest">Delete</button>
            <!-- /ko -->
            <a type="button" class="btn btn-default btn-lg" data-bind="attr: {
                            href: '${pageContext.request.contextPath}/action/industry/secured/e-manifest/home/' + rcra.emanifest.handlerId+'?tsdf='+(role=='tsdf')
                         }">Back to Dashboard</a>
        </div>
    </div>
</div>
<!-- /ko -->
