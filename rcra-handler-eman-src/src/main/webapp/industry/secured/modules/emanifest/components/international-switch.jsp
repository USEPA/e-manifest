<%@ taglib prefix="stripes"
	uri="http://stripes.sourceforge.net/stripes-dynattr.tld"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions"%>
<stripes:layout-definition>
	<script>
		$(function(){
			if (!ko.components.isRegistered('international-switch')){
				ko.components.register('international-switch', {
					template: { element: 'international-switch'},
				    viewModel: function (params){
				    	var self = this;
						self= $.extend(self,params);
						if (typeof self.enable 	===  "undefined") {
							self.enable = true;
						}					
				    }
				});
			}
		});
	</script>
	<template id="international-switch">
	<div class="row">
		<div class="col-sm-12 form-group">
			<label class="control-label" for="international-shipment">International
				Shipment (Import Only)</label>
			<div style="height: 34px;">
				<input id="international-shipment" class="switch switch-lg"
					type="checkbox"
					data-bind=" attr:{readonly: !enable}, bootstrapSwitchOn: flag"
					data-on-text="Yes" data-off-text="No"/>
			</div>
		</div>
	</div>
	</template>
</stripes:layout-definition>