<%@ page contentType="text/html;charset=UTF-8" language="java"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="stripes" uri="http://stripes.sourceforge.net/stripes-dynattr.tld"%>
<%@ taglib prefix="display" uri="http://displaytag.sf.net/el"%>
<%@ taglib prefix="security" uri="http://www.springframework.org/security/tags"%>
<%-- 
This part is just to simulate creating/editing a manifest for the mockups.  When we implement this for real we would 
do something different.
--%>
<c:choose>
	<c:when test="${not empty actionBean.trackingNumber }">
		<c:set var="jsonUrl" value="${pageContext.request.contextPath}/static/json/industry/emanifest/manifests/${actionBean.trackingNumber}.json"></c:set>
	</c:when>
	<c:when test="${empty actionBean.trackingNumber and actionBean.tsdf }">
		<c:set var="jsonUrl" value="${pageContext.request.contextPath}/static/json/industry/emanifest/manifests/newTsdf.json"></c:set>
	</c:when>
	<c:otherwise>
		<c:set var="jsonUrl" value="${pageContext.request.contextPath}/static/json/industry/emanifest/manifests/new.json"></c:set>
	</c:otherwise>
</c:choose>

<c:choose>
	<c:when test="${actionBean.tsdf}">
		<c:set var="tsdf" value="true"></c:set>
	</c:when>
	<c:otherwise>
		<c:set var="tsdf" value="false"></c:set>
	</c:otherwise>
</c:choose>

<stripes:layout-render name="/industry/secured/modules/emanifest/common/manifest-layout.jsp" title="e-Manifest Form" tab="Home">
	<stripes:layout-component name="additionalHead">
		<script>
			//TODO move this somewhere else
			var ctx = "${pageContext.request.contextPath}";
		</script>
		<script src="${pageContext.request.contextPath}/static/js/emanifest.js"></script>
		<script>			
			$(function(){
			    rcra.emanifest = {
			        handlerId: "${actionBean.handlerId}"
				};
			    var ViewModel = function(role) {
			        var self = this;
			        self.role = role;
                    self.component = function(name, params) {
                        return function(page, callback) {
                            var componentDiv = $('<div></div>');
                            if(params) {
                                componentDiv.attr('data-bind', "component: {name: '" + name + "', params: " + params + "}");
                            }
                            else {
                                componentDiv.attr('data-bind', "component: '" + name + "'");
                            }
                            $(page.element).html(componentDiv);
                            callback();
                        }
                    }
                    self.disposeComponent = function(page, callback) {
                        if(callback) {
                            $(page.element).hide();
                            callback();
                            $(page.element).children().each(function(index, child) {
                                ko.utils.domNodeDisposal.removeNode(child);
                            });
                        }

                    }
				}
				$.when(
					loadLookup('federalHazardousWasteCodeOptions'),
					loadLookup('stateHazardousWasteCodeOptions'),
					loadLookup('dotDescriptions'),
					loadLookup('units'),
					loadLookup('containerTypes'),
					loadLookup('densityUnits'),
					loadLookup('formCodes'),
					loadLookup('sourceCodes'),
					loadLookup('guideBookNumbers'),
					loadLookup('states'),
					loadLookup('methodCodes'),
					loadLookup('transporters'),
					loadLookup('tsdfs'),
					loadLookup('status')
				).done(function(){
					console.log("loaded all lookups");
					viewModel = new ViewModel(isTsdf() ? 'tsdf':'generator');
					pager.extendWithPage(viewModel);
					ko.applyBindings(viewModel, $('#dashboard-content').get(0));
					pager.start();	
					//TODO hacky way to get around this look into how we can trigger this after all the content is shown
					setTimeout(setUnsavedEvents, 1000);
				});
			});
			function isTsdf() {
				return ${tsdf};
			}
			function setUnsavedEvents() {
				$("a:not([target='_blank']):not(.dropdown-toggle):not(.unsavedCheckIgnore):not([class*='select2']):not([data-target='#manifestWasteSectionModal'])").click(function(event) {
					var url = $(event.target).attr('href');
					rcra.notifications.showAlertDialog(null, "All unsaved data will be lost.",
						{
							type: BootstrapDialog.TYPE_WARNING,
							buttons: [
								{
									label: 'Continue',
									cssClass: 'btn-primary',
									action: function (dialog) {
										if (url) {
											window.location.href = url;
										}
										dialog.close();
									}
								}
							]
						});
					return false;
				});
			}
		</script>
		<style>
			.finish-later {
				margin-right: 40px;
			}
			/*TODO move these styles*/
			.eman-progress-bar {
				display: flex;
				flex-flow: row nowrap;
				justify-content: space-between;
				margin: 0 50px 35px 50px;
				padding: 0;
				/* Permalink - use to edit and share this gradient: http://colorzilla.com/gradient-editor/#b4e391+0,bcbcbc+50,b4e391+100&0+40,1+50,0+60 */
				background: -moz-linear-gradient(top, rgba(180,227,145,0) 0%, rgba(186,196,179,0) 40%, rgba(188,188,188,1) 50%, rgba(186,196,179,0) 60%, rgba(180,227,145,0) 100%); /* FF3.6-15 */
				background: -webkit-linear-gradient(top, rgba(180,227,145,0) 0%,rgba(186,196,179,0) 40%,rgba(188,188,188,1) 50%,rgba(186,196,179,0) 60%,rgba(180,227,145,0) 100%); /* Chrome10-25,Safari5.1-6 */
				background: linear-gradient(to bottom, rgba(180,227,145,0) 0%,rgba(186,196,179,0) 40%,rgba(188,188,188,1) 50%,rgba(186,196,179,0) 60%,rgba(180,227,145,0) 100%); /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */
				filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#00b4e391', endColorstr='#00b4e391',GradientType=0 ); /* IE6-9 */
			}
			.eman-progress-bar > li {
				list-style-type: none;
				padding: 0 3px 0 4px;
				background-color: white;
				position: relative;
				color: #BCBCBC;
			}
			.eman-progress-bar > li > .status-text {
				content: "status";
				position: absolute;
				bottom: -20px;
				left: -50px;
				right: -50px;
				text-align: center;
				font-size: 15px;
				text-transform: uppercase;
			}
			.eman-progress-bar > .active {
				font-weight: bold;
				color: #339933;
			}
			.eman-progress-bar > .complete {
				color: #339933;
			}
			.panel-heading .glyphicon {
				font-size: 150%;
			}
			pre.static-info {
				background-color: inherit;
				border: none;
				border-radius: unset;
				padding: 0;
				margin: 0;
				font-size: inherit;
				font-family: inherit;
				line-height: inherit;
			}
			p.error {
				color: #D8000C;
			}
			.control-label + .checkbox {
				margin-top: 0;
			}
			/* For revision details popover */
			.panel-info > .panel-heading .form-group {
				color: #333;
			}
			.revision-details {
				width: 150px;
			}
			.modal-lg.modal-xlg {
				width: 1000px;
			}
		</style>
		<stripes:layout-render name="/industry/secured/modules/emanifest/components/phone-info.jsp"/>
		<stripes:layout-render name="/industry/secured/modules/emanifest/components/address-info.jsp"/>
		<stripes:layout-render name="/industry/secured/modules/emanifest/components/manifest-facility-info.jsp"/>
		<stripes:layout-render name="/industry/secured/modules/emanifest/components/international-switch.jsp"/>
	</stripes:layout-component>
	<stripes:layout-component name="breadCrumbs">
		<ol class="breadcrumb">
			<li><a href="${pageContext.request.contextPath}/action/industry/secured/home">My Sites</a></li>
			<li><a href="${pageContext.request.contextPath}/action/industry/secured/myrcraid/home/${actionBean.handlerId}">${actionBean.handlerId}</a></li>
			<li><a href="${pageContext.request.contextPath}/action/industry/secured/e-manifest/home/${actionBean.handlerId}?tsdf=${tsdf}">e-Manifest Dashboard</a></li>
			<c:choose>
				<c:when test="${actionBean.trackingNumber==null}">
					<li class="active">e-Manifest</span></li>			
				</c:when>
				<c:otherwise>
					<li class="active">e-Manifest - ${actionBean.trackingNumber}</span></li>				
				</c:otherwise>
			</c:choose>			
		</ol>
	</stripes:layout-component>
	<stripes:layout-component name="tabContent">
		<script type="text/html" id="eman-revision-history">
			<div class="revision-details">
				<div class="row">
					<div class="col-sm-12 form-group">
						<label class="control-label">Created By</label>
						<span class="static-info help-block" data-bind="text: createdBy.firstName() + ' ' + createdBy.lastName()"></span>
					</div>
				</div>
				<div class="row">
					<div class="col-sm-12 form-group">
						<label class="control-label">Created Date</label>
						<span class="static-info help-block" data-bind="text: createdDate"></span>
					</div>
				</div>
				<div class="row">
					<div class="col-sm-12 form-group">
						<label class="control-label">Last Updated By</label>
						<span class="static-info help-block" data-bind="text: updatedBy.firstName() + ' ' + createdBy.lastName()"></span>
					</div>
				</div>
				<div class="row">
					<div class="col-sm-12 form-group">
						<label class="control-label">Last Updated Date</label>
						<span class="static-info help-block" data-bind="text: updatedDate"></span>
					</div>
				</div>
			</div>
		</script>
		<div data-bind="page: {id: 'manifest', params: ['trackingNum']}">
			<div data-bind="page: {id: 'edit', scrollToTop: true, sourceOnShow: component('edit-manifest', '{trackingNum: trackingNum, role: role}'), hideElement: disposeComponent}">
			</div>
			<div data-bind="page: {id: 'review', scrollToTop: true, sourceOnShow: component('review-manifest', '{trackingNum: trackingNum, role: role}'), hideElement: disposeComponent}">
			</div>
		</div>
	</stripes:layout-component>
</stripes:layout-render>