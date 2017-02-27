<!-- ko with: form -->
<div class="row">
	<div class="col-sm-12 form-group table-responsive">
		<p class="validationMessage" data-bind="validationElement: wasteSection().wasteCollection, validationMessage: wasteSection().wasteCollection"></p>
		<label class="constrol-label" for="waste-table" data-bind="slideVisible: wasteSection().wasteCollection().length > 0">Waste
			Characteristics (Total lines: <span data-bind="text: wasteSection().wasteCollection().length"></span>)</label>
		<!-- ko if: wasteSection().wasteCollection().length > 0 -->
		<table id="waste-table" class="table table-striped table-bordered"
			data-bind="slideVisible: wasteSection().wasteCollection().length > 0, validationOptions: {insertMessages: false}">
			<thead class="bg-warning">
				<tr class="info">
					<th data-bind="visible: wasteSection().hasErrors"><span class="glyphicon glyphicon-exclamation-sign"></span></th>
					<th>Line Number</th>
					<th>U.S. DOT Description</th>
					<th>Containers</th>
					<th>Type</th>
					<th>Total Qty.</th>
					<th>Units</th>
					<th>Waste Codes</th>
					<th>Management <br> Method <br> Code</th>							
					<th>Action</th>
				</tr>
			</thead>
			<tbody data-bind="foreach: wasteSection().wasteCollection">
				<tr data-bind="css: {danger: errors().length > 0}">
					<td data-bind="visible: $parent.wasteSection().hasErrors()">
						<!-- ko if: errors().length > 0 -->
							<%-- for auto error scroll to scroll to this row --%>
							<span class="validationMessage">
								<label class="label label-danger" data-bind="text: errors().length" title="Errors needing attention"></label>
							</span>
						<!-- /ko -->
						<!-- ko if: errors().length == 0 -->
							<span class="text-success glyphicon glyphicon-ok"></span>
						<!-- /ko -->
					</td>
					<td>
						<span data-bind="text: lineNumber"></span>
					</td>
					<td>
						<span data-bind="text: dotDescriptionDisplay"></span>
					</td>
					<td>
						<span data-bind="text: containerInfo.number">
					</td>
					<td>
						<span data-bind="text: containerInfo.type()==null?'':containerInfo.type().code">
					</td>
					<td>
						<span data-bind="text: containerInfo.quantity">
					</td>
					<td>
						<span data-bind="text: containerInfo.unit()==null?'':containerInfo.unit().code">
					</td>
					<td>
						<span data-bind="text: displayWasteCodes()">
					</td>	
					<td><span data-bind="text: managementCode() ? managementCode().code() : null"></td>							
					<td>
						<a href="JavaScript:" title="Edit" class="unsavedCheckIgnore"
								data-bind="modal: {
												name: 'edit-waste',
												params: {
													data: {
														waste: $data,
														form: $parent,
														generatorPartialEdit: $parent.generatorPartialEdit,
														isTsdf: isTsdf(),
														tsdf: $parent.tsdf,
														generator: $parent.generator,
														internationalShipment: $parent.internationalShipment,
														save: $parent.wasteSection().save
													}
												}
											}">
							<span class="glyphicon glyphicon-pencil"></span>
						</a>&nbsp; 
						<a title="Remove" href="#" class="unsavedCheckIgnore"
								data-bind="click: function(){$parent.wasteSection().removeWaste($data);}">
							<span class="glyphicon glyphicon-remove"></span>
						</a>
					</td>
				</tr>
			</tbody>
		</table>
		<!-- /ko -->
		<!-- ko if: wasteSection().undoList().length > 0 -->
			<a href="JavaScript:;" data-bind="click: function(){wasteSection().undo()}">Undo Waste Remove</a>
		<!-- /ko -->
		<!-- ko ifnot: generatorPartialEdit -->
			<div>
				<button class="btn btn-primary" data-bind="click: function(){wasteSection().startNewWaste();}">Add
					Waste to Manifest</button>
			</div>
		<!-- /ko -->
	</div>
</div>
<!-- /ko -->