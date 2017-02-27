<%@ taglib prefix="stripes"
	uri="http://stripes.sourceforge.net/stripes-dynattr.tld"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions"%>
<stripes:layout-definition>
	<script>
		$(function(){
			if (!ko.components.isRegistered('address-info')){
				ko.components.register('address-info', {
					template: { element: 'address-info'}
				});
			}
		});
	</script>

	<template id="address-info">
		<label class="control-label" data-bind="text: addressLabel"></label>
		<address class="help-block static-info" data-bind="with: address">
			<span data-bind="text: street"></span>,
			<span data-bind="text: city"></span>, <span data-bind="text: state"></span>
			<span data-bind="text: zip"></span>
		</address>	
	</template>
</stripes:layout-definition>