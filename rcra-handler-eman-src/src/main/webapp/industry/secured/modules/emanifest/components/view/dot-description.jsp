<div class="row"
	data-bind="slideVisible: isHazardous">
	<div class="col-sm-6">
		<div class="form-group required">
			<label class="control-label" for="usDotDescription_waste">Proper
				Shipping Name - ID Number </label>
			<span class="static-info help-block" data-bind="text: shippingName().shippingName() + ' - ' + shippingName().unIDNumber()"></span>
		</div>
	</div>
	<div class="col-sm-2">
		<div class="row">
			<div class="col-sm-12">
				<label>Hazard Class </label>
				<span class="static-info help-block" data-bind="text: shippingName() ? shippingName().hazardClass() : null"></span>
			</div>
		</div>
	</div>
	<div class="col-sm-2">
		<div class="row">
			<div class="col-sm-12">
				<label>Packing Group </label>
				<span class="static-info help-block" data-bind="text: shippingName() ? shippingName().packingGroup() : null"></span>
			</div>
		</div>
	</div>
</div>
<div class="row">
	<div class="col-sm-12">
		<div class="form-group"
			data-bind="visible: isHazardous">
			<label for="additionalDotInformation">
				Printed DOT Information </label>
			<span class="static-info help-block" data-bind="text: additionalDotInformation"></span>
		</div>
		<div class="form-group required"
			data-bind="visible: isHazardous()==false">
			<label class="control-label" for="wasteDescription">
				Waste Description </label>
			<span data-bind="text: wasteDescription"></span>
		</div>
	</div>
</div>
<div class="row">
	<div class="col-sm-6 form-group" data-bind="visible: isHazardous">
		<label for="erResponseGuidebookNumber" class="control-label">Emergency Response Guidebook Number</label>
			<span class="static-info help-block" data-bind="text: erResponseGuidebookNumber"></span>
		</select>
	</div>
</div>
<div class="row form-group">
	<phone-info-review params="elemWidthClass: 'col-sm-5 col-md-3', phoneLabel: 'Emergency Response Phone', phoneNumber: emergencyPhone, phoneExtension: emergencyPhoneExt"></phone-info-review>
</div>
