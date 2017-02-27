<!-- ko with: form -->
<div class="row">
	<div class="col-sm-12 form-group radio">
		<label class="control-label" for="import-to-us">
			<input id="import-to-us" name="shipment-import-export" type="radio"
					data-bind="checked: importToUs, checkedValue: true"></input>
			Import to U.S.
		</label>
	</div>
</div>
<div class="row">
	<div class="col-sm-12 form-group radio disabled">
		<label class="control-label text-muted" for="export-from-us" title="Exports are currently not supported in the application.  Support will be added at a later time.">
			<input id="export-from-us" name="shipment-import-export"
					type="radio" data-bind="checked: importToUs, checkedValue: false" disabled></input>
			Export from U.S. 
		</label>
	</div>
</div>
<div class="row">
	<div class="col-sm-12 form-group">
		<label class="control-label" data-bind="text: (importToUs() == true)?'Port of Entry':'Port of Exit'">Port of Entry/Exit</label>
	</div>
</div>
<div class="row">
	<div class="col-sm-4 form-group">
		<label class="control-label" for="port-city">City</label> <input
			id="port-city" class="form-control" type="text"
			data-bind="value: city" />
	</div>
	<div class="col-sm-4 form-group">
		<label class="control-label" for="port-state">State</label> <select
			id="port-state" class="form-control"
			data-bind="value: state, 
					lookup: 'states', 
					optionsText: 'name',
					valueAllowUnset: true">
		</select>
	</div>
	<div class="col-sm-4 form-group" data-bind="fadeVisible: importToUs() == false">
		<label class="control-label" for="port-date-leaving">Date
			Leaving U.S.</label> <input id="port-date-leaving" class="form-control"
			type="text" data-bind="value: dateLeaving" />
	</div>	
</div>
<!-- /ko -->