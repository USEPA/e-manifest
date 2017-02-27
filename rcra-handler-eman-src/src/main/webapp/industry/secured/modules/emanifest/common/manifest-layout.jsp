<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="stripes" uri="http://stripes.sourceforge.net/stripes-dynattr.tld" %>
<%@ taglib prefix="display" uri="http://displaytag.sf.net/el" %>
<stripes:layout-definition>
  <stripes:layout-render name="/industry/layout/layout.jsp" tab="Home">
    <%--<stripes:layout-component name="additionalHead">
      <script src="${pageContext.request.contextPath}/static/js/postal/postal.min.js"></script>
    </stripes:layout-component>--%>
    <stripes:layout-component name="container">
      <script src="${pageContext.request.contextPath}/static/js/postal/postal.min.js"></script>
      <!-- Font Awesome -->
      <link href="${pageContext.request.contextPath}/static/css/font-awesome.min.css" rel="stylesheet"/>
      ${breadCrumbs}
      <div class="row">
        <div class="col-sm-12">
          <div id="dashboard-content">
              ${tabContent}
          </div>
        </div>
      </div>
      <div id="popups"></div>
    </stripes:layout-component>
  </stripes:layout-render>
</stripes:layout-definition>