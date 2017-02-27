<div class="row">
	<div class="col-sm-2 col-md-1">
		<div class="form-group">
			<label for="containersNumber" class="control-label">Number</label>
			<input type="text" id="containersNumber" class="form-control" maxlength="3"
				data-bind="textInput: number" />
		</div>
	</div>
	<div class="col-sm-6 col-md-6">
		<div class="form-group">
			<label for="containersType" class="control-label">Type</label>
			<select id="containersType" class="form-control"
				data-bind="lookup: 'containerTypes', 
						optionsText: function(item){ return item.code() +'-'+item.description();}, 
						optionsCaption: '',
						optionsValue: 'code', 
						lookupValue: type,
						select2: {allowClear: true, placeholder: 'Select Type'}"></select>
		</div>
	</div>
	<div class="col-sm-3"
		data-bind="fadeVisible: type() && type().code() == 'NL'">
		<div class="form-group">
			<label for="notListedType" class="control-label">Not
				Listed Type</label> <input type="text" id="notListedType"
				class="form-control" data-bind="value: notListedType" />
		</div>
	</div>
	<div class="col-sm-3 col-md-2">
		<div class="form-group">
			<label class="control-label" for="containersTotalQuantity">Quantity
				</label> <input id="containersTotalQuantity" type="text" maxlength="6"
				class="form-control" data-bind="textInput: quantity" />
		</div>
	</div>
	<div class="col-sm-4 col-md-3">
		<div class="form-group">
			<label for="containersUnit" class="control-label" style="white-space: nowrap;">Unit Wt./Vol.</label> 
			<select id="containersUnit" class="form-control"
					data-bind="lookup: 'units', 
							optionsText: function(item){ 
								return item.code() +'-'+item.description();
							}, 
							optionsCaption: '',
							optionsValue: 'code', 
							lookupValue: unit,
							select2: {allowClear: true, placeholder: 'Select Unit'}"></select>
		</div>
	</div>
</div>
<div class="row">
	<div class="col-sm-12">
		<div class="panel panel-default">
			<div class="panel-heading">Biennial Report Information</div>
			<div class="panel-body">
				<div class="row">
					<div class="col-sm-12">
						<div class="form-group">
							<label for="hazWaste">Provide
								BR Information? </label>
							<div style="height: 34px;">
								<input type="checkbox" class="switch" id="hazWaste"
									data-bind="bootstrapSwitchOn: provideBRInfo"
									data-on-text="Yes" data-off-text="No">
							</div>
						</div>
					</div>
				</div>
				<div id="brInfo" data-bind="slideVisible: provideBRInfo">
					<div class="row">
						<div class="col-sm-2">
							<div class="form-group"
								data-bind="slideVisible: showDensity">
								<label class="control-label" for="containersDensity">Density</label>
								<input id="containersDensity" type="text"
									class="form-control"
									data-bind="textInput: density" />
							</div>
						</div>
						<div class="col-sm-3">
							<div class="form-group"
								data-bind="slideVisible: showDensity">
								<label class="control-label" for="containersDensityUnits">Density Units</label> 
								<select id="containersDensityUnits" class="form-control"
										data-bind="lookup: 'densityUnits', 
												optionsCaption: '',
												valueAllowUnset: true,
												value: densityUnit,
												select2: {allowClear: true, placeholder: 'Select Density Unit'}"></select>
							</div>
						</div>
					</div>
					<div class="row">
						<div class="col-sm-12">
							<div class="form-group">
								<label for="formCode" class="control-label">Form Code</label> 
									<select id="formCode" class="form-control"
											data-bind="lookup: 'formCodes', 
											optionsCaption: '',
											optionsText: function(item){ 
												return item.code() +'-'+item.description();
											}, 
											optionsValue: 'code', 
											lookupValue: formCode, 
											select2: {allowClear: true, placeholder: 'Select Form Code'}">
								</select>

							</div>
						</div>
					</div>
					<div class="row">
						<div class="col-sm-12">
							<div class="form-group"
								data-bind="slideVisible: formCommentVisible()">
								<label for="formCodeComment" class="control-label">Form
									Code Comment</label>
								<textarea id="formCodeComment" class="form-control"
									data-bind="textInput: formCodeComment"></textarea>
							</div>
						</div>
					</div>
					<div class="row">
						<div class="col-sm-12">
							<div class="form-group">
								<label for="sourceCode" class="control-label">Source Code</label> 
								<select id="sourceCode" class="form-control"
										data-bind="lookup: 'sourceCodes', 
												optionsCaption: '',
											  	optionsText: function(item){ 
											  		return item.code() +'-'+item.description();
											  	}, 
											  	optionsCaption: '', 
											  	optionsValue: 'code', 
											  	lookupValue: sourceCode, 
											  	select2: {allowClear: true, placeholder: 'Select Source Code'}">
								</select>
							</div>
						</div>
					</div>
					<div class="row">
						<div class="col-sm-12">
							<div class="form-group"
								data-bind="slideVisible: sourceCommentVisible()">
								<label for="sourceCodeComment" class="control-label">Source
									Code Comment</label>
								<textarea id="sourceCodeComment" class="form-control"
									data-bind="textInput: sourceCodeComment"></textarea>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>