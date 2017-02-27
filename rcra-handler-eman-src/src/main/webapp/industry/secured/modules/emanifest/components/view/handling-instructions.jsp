<!-- ko with: form -->
<div class="row">
	<div class="col-sm-12 form-group">
		<label class="control-label" for="special-handling-instructions">Special Handling Instructions for this Manifest</label>
		<pre class="static-info help-block" data-bind="text: handlingInstructions"></pre>
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
					<th class="top-align" width="70%">Description</th>
				</tr>
			</thead>
			<tbody data-bind="foreach: handlerComments">
				<tr>
					<td width="15%">
						<span class="static-info" data-bind="text: epaSiteId"></span>
					</td>
					<td width="15%">
						<span id="comment-label" class="static-info" data-bind="text: label" />
					</td>
					<td width="70%">
						<span id="comment-description" class="static-info" style="width: 100%;"
							data-bind="text: description" />
					</td>
				</tr>
			</tbody>
		</table>
		<!-- /ko -->
	</div>
</div>
<!-- ko if: additionalInfo.originalManifestTrackingNumber -->
<div class="row">
	<div class="col-sm-12 form-group">
		<label class="control-label">Original Manifest Tracking Number</label>
		<span class="static-info" data-bind="text: additionalInfo.originalManifestTrackingNumber"></span>
	</div>
</div>
<!-- /ko -->
<!-- /ko -->