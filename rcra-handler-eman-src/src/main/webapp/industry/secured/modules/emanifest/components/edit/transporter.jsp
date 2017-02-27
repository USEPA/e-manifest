<!-- ko with: form -->
<div class="row">
	<div class="col-sm-12 form-group">
		<label class="control-label" for="transporter">EPA ID - Name</label>
		<select class="form-control"
			data-bind="lookup: 'transporters', 
					optionsCaption: '',
			  		optionsText: 'display',
			  		optionsValue: 'epaSiteId', 
			  		lookupValue: selectedTransporter,
			  		select2: {allowClear: true, placeholder: 'Select Transporter'},
			  		validationElement: transporters"></select>
		<span class="validationMessage" data-bind="validationMessage: transporters"></span>
	</div>
</div>
<div class="row">
	<div class="col-sm-12 table-responsive" data-bind="slideVisible: transporters().length>0">
		<table style="width: 100%" id="transporterTable"
			class="table table-striped table-bordered table-hover dataTable responsive no-wrap">
			<caption>
				<h4 class="panel-title pull-left">
					<strong>Selected Transporters</strong>
				</h4>
			</caption>
			<thead>
				<tr>
					<th class="top-align" width="30%">ID</th>
					<th class="top-align" width="70%">Name</th>
					<th class="top-align" width="70%">Action</th>
				</tr>
			</thead>
			<tbody data-bind="foreach: transporters">
				<tr>
					<td width="30%">
						<span data-bind="text: epaSiteId"></span>
					</td>
					<td width="70%">
						<span data-bind="text: siteName()"></span>
					</td>
					<td width="5%" style="text-align: center;">
						<a href="#" class="unsavedCheckIgnore" data-bind="click: function(){$parent.removeTransporter($data);}"><span title="Remove"
							class="glyphicon glyphicon-remove" aria-hidden="true"></span></a>
					</td>
				</tr>
			</tbody>
		</table>
	</div>
</div>
<!-- /ko -->