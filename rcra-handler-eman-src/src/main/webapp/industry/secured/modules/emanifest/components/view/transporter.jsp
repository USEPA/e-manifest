<!-- ko with: form -->
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
				</tr>
			</tbody>
		</table>
	</div>
</div>
<!-- /ko -->