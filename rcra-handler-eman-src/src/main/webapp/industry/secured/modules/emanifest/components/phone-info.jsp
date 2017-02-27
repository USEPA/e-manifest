<%@ taglib prefix="stripes"
	uri="http://stripes.sourceforge.net/stripes-dynattr.tld"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions"%>
<stripes:layout-definition>
	<script>
		$(function(){
			if (!ko.components.isRegistered('phone-info')){
				ko.components.register('phone-info', {
					template: { element: 'phone-info'},
					viewModel : function(params) {
						var self = this;
						if (params == null)
							params = {};
						self.defaults = {
							elemWidthClass : 'col-sm-3'
						};
						self.elemWidthClass = ko.observable(params.elemWidthClass || self.defaults.elemWidthClass);
						self.phoneLabel = params.phoneLabel;
						self.phoneNumber = params.phoneNumber;
						self.phoneExtension = params.phoneExtension;
					}					
				});
			}
		});
	</script>

	<template id="phone-info">
		<div data-bind="css: elemWidthClass()" class="form-group">
					<label class="control-label" data-bind="text: phoneLabel"></label>
					<input class="form-control" type="text"
						data-bind="maskedPhone: phoneNumber" />
		</div>
		<div data-bind="attr:{class: elemWidthClass()}">
			<label class="control-label">Extension</label>
			<input class="form-control" type="text"
				data-bind="value: phoneExtension" />
		</div>
	</template>
</stripes:layout-definition>