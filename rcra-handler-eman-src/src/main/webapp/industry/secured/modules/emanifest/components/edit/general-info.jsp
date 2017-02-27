<!-- ko with: form -->
<div class="row form-group">
	<div class="col-sm-12">
		<label class="control-label" for="manifestTrackingNumber">Manifest Tracking Number</label> 
		<span class="help-block static-info" id="manifestTrackingNumber" data-bind="text: manifestTrackingNumber"></span>
	</div>
</div>	
<hr>
<div class="row">
	<div class="col-sm-12">			
		<label class="control-label" for="status">Status</label>
	</div>
</div>
<div class="row">
	<div class="col-sm-12"			
			data-bind="foreach: availableStatuses">			
		<div class="row">
			<div class="col-sm-12">			
                      <label class="radio-label">
                          <input name="status"
                                 data-bind="value: $data, checked: $parent.status"
                                 type="radio"/>
                        	<span style="margin-left: 5px;" data-bind="text: code"></span>
                        	 - 
                        	<span data-bind="text: description"></span>
                      </label>					
			</div>								
		</div>			
	</div>
</div>
<hr>
<international-switch params="flag: internationalShipment, enable: isTsdf()"></international-switch>
<!-- /ko -->