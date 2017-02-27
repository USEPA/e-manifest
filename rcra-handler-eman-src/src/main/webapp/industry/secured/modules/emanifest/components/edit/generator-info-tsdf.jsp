<!-- ko with: form -->
    <div class="row">
        <div class="col-sm-3">
            <div data-bind="slideVisible: !tsdfAsGenerator()">
                <facility-search params="selectGenerator: selectGenerator, notFound: notFound"></facility-search>
            </div>
        </div>
        <div class="col-sm-4 col-sm-offset-5">
            <label>
                <bs-switch params="flag: tsdfAsGenerator, switchSize: 'switch-lg'"></bs-switch>
                Select this Site as Generator
            </label>
        </div>
    </div>
    <hr>
    <div data-bind="slideVisible: generator">
        <!-- ko if: manualGeneratorEntry -->
        <facility-info-edit params="facilityInfo: generator, editMode: editingGenerator"></facility-info-edit>
        <!-- /ko -->
        <!-- ko ifnot: manualGeneratorEntry -->
        <facility-info params="facilityInfo: generator"></facility-info>
        <button class="btn btn-primary" data-bind="click: editGenerator">Edit</button>
        <!-- /ko -->
    </div>
<!-- /ko -->