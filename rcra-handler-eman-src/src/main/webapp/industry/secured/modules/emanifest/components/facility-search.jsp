<div class="form-group">
    <label for="generator-quick-search" class="control-label">Enter EPA ID Number</label>
    <div class="input-group" data-bind="validationOptions: {insertMessages: false}">
        <input type="text" id="generator-quick-search" class="form-control" data-bind="value: epaIdNumber" minlength="12" maxlength="12"/>
        <div class="input-group-btn">
            <button class="btn btn-default"><span class="glyphicon glyphicon-search"></span></button>
        </div>
    </div>
    <a href="JavaScript:" class="pull-right unsavedCheckIgnore" data-bind="modal: {name: 'facility-search-modal', params: {reset: true}}">Advanced Search</a>
    <span class="help-block"><br>For demo purposes use <br>VAR000525113, VAD988177803 or VAR000521534</span>
    <span class="validationMessage" data-bind="validationMessage: epaIdNumber"></span>
    <span class="validationMessage" data-bind="text: quickSearchError, visible: quickSearchError"></span>
</div>