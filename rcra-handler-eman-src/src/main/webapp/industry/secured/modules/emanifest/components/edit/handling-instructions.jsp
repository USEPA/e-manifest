<!-- ko with: form -->
<div class="row">
	<div class="col-sm-12 form-group">
		<label class="control-label" for="special-handling-instructions">Special Handling Instructions for this Manifest</label>
		<textarea id="special-handling-instructions" class="form-control" data-bind="value: handlingInstructions"></textarea>
	</div>
</div>
<div class="row">
	<div class="col-sm-12 form-group table-responsive">
		<label class="control-label">Handler Defined Data for this Manifest</label>
		<!-- ko if: handlerComments().length > 0 -->
		<table style="width: 100%" id="wasteHandlerCommentsTable"
			class="table table-striped table-bordered table-hover dataTable responsive no-wrap">
			<thead>
				<tr>
					<th class="top-align" width="15%">EPA ID Number</th>
					<th class="top-align" width="15%">Label</th>
					<th class="top-align" width="60%">Description</th>
					<th class="top-align" width="5%">Action</th>
				</tr>
			</thead>
			<tbody data-bind="foreach: handlerComments">
				<tr>
					<td width="15%">
						<span data-bind="text: epaSiteId"></span>
					</td>
					<td width="15%">
						<input id="comment-label" class="form-control" type="text" data-bind="value: label" />
					</td>
					<td width="60%">
						<input id="comment-description" class="form-control" style="width: 100%;" type="text"
							data-bind="value: description" />
					</td>
					<td width="5%" style="text-align: center;">
						<a href="#" data-bind="click: function(){$parent.removeHandlerComment($data);}"><span title="Remove"
							class="glyphicon glyphicon-remove" aria-hidden="true"></span></a>
					</td>
				</tr>
			</tbody>
		</table>
		<!-- /ko -->
		<div>
			<button href="JavaScript:;" class="btn btn-primary" data-bind="click: addHandlerComment, text: (handlerComments().length==0?'Add Comment':'Add Another Comment')">Add Another</a>
		</div>
	</div>
</div>
<div class="row">
	<div class="col-sm-12 form-group">
		<div class="checkbox">
			<label>
				<input type="checkbox" name="has-previous-shipment" data-bind="checked: additionalInfo.hasPreviousShipment"/>
				Does this shipment contain a residue or rejected waste from the previous shipment?
			</label>
		</div>
	</div>
</div>
<div class="row" data-bind="slideVisible: additionalInfo.hasPreviousShipment">
	<div class="col-sm-12 form-group">
		<label class="control-label">Original Manifest Tracking Number</label>
		<input type="text" class="form-control" data-bind="manifestTrackingNumber: additionalInfo.originalManifestTrackingNumber"/>
	</div>
</div>
<!-- /ko -->