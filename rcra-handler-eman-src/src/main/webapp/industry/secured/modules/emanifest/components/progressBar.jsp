<%@ taglib prefix="stripes" uri="http://stripes.sourceforge.net/stripes-dynattr.tld" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<ul class="eman-progress-bar" data-bind="foreach: statuses">
	<li data-bind="css: {
			'complete': order() < $parent.currentStatus().order(),
			'active': order() == $parent.currentStatus().order()
		}">
		<span class="fa fa-2x" data-bind="css: icon"></span> 
		<span class="status-text hidden-xs" data-bind="text: code"></span>
	</li>
</ul>