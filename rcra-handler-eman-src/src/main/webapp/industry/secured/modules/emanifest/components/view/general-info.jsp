<!-- ko with: form -->
<div class="row form-group">
	<div class="col-sm-12">
		<label class="control-label" for="manifestTrackingNumber">Manifest Tracking Number</label> 
		<span class="help-block static-info" id="manifestTrackingNumber" data-bind="text: manifestTrackingNumber"></span>
	</div>
</div>	
<hr>
<div class="row">
	<div class="col-sm-12 form-group">			
		<label class="control-label" for="status">Status</label>
		<span class="help-block static-info" id="status" data-bind="text: status().code"/>
	</div>
</div>
<hr>
<international-switch params="flag: internationalShipment, enable: false"></international-switch>
<!-- /ko -->