var viewModel;
var EditManifestController = function(data, params) {
    var self = this;
    self.trackingNum = params.trackingNum;
    self.formLoaded = ko.observable(false);
    self.loadForm = function() {
    	self.formLoaded(false);
    	var url = ctx + '/static/json/industry/emanifest/manifests/';
    	if(self.trackingNum()) {
    		url += self.trackingNum() + '.json'
        }
        else {
    		if(params.role == "tsdf") {
    			url += 'newTsdf.json';
			}
			else {
    			url += 'new.json';
            }
		}
        $.getJSON(url, function (manifest) {
            ko.utils.extend(self, new Manifest(manifest, params.role));
            self.role = params.role;
            self.currentStatus = ko.observable(new Status(ko.mapping.toJS(self.status)));
            self.availableStatuses = ko.computed(function () {
                return ko.utils.arrayFilter(lookups.status(), function (item) {
                    if (self.currentStatus().order() == 1) {
                        return item.order() <= 2;
                    }
                    else if (self.currentStatus().order() >= 2 && self.currentStatus().order() < 4) {
                        if (isTsdf()) {
                            return item.order() >= 2 && item.order() <= 5;
                        }
                        else {
                            return item.order() >= 1 && item.order() <= 2;
                        }
                    }
                    else if (self.currentStatus().order() >= 4) {
                        return item.order() >= 4 && item.order() <= 5;
                    }
                });
            });
            self.printTitle = ko.computed(function () {
                if (self.currentStatus().code() == "Pending" || self.currentStatus().code() == "Draft") {
                    return "Print Draft";
                }
                else {
                    return "Print Official";
                }
            });
            self.addHandlerComment = function () {
                self.handlerComments.push(new ViewHandlerComment());
            }
            self.removeHandlerComment = function (comment) {
                self.handlerComments.remove(comment);
            }
            self.dirty = ko.dirtyFlag(self, false);
            self.save = function () {
                if(!self.validate()) {
                	return;
				}
                switch (self.status().code()) {
                    case 'Draft':
                        rcra.notifications.showSuccessMessage('Manifest '
                            + self.manifestTrackingNumber()
                            + ' has been saved as a draft.<br>'
                            + '<a href="'
                            + ctx
                            + '/action/industry/secured/e-manifest/home/'
							+ rcra.emanifest.handlerId
							+ '">Return to Dashboard</a>');
                        break;
                    case 'Pending':
                    case 'In Transit':
                    case 'Received':
                        rcra.notifications.showSuccessMessage('Manifest '
                            + self.manifestTrackingNumber()
                            + ' has been set to '
                            + self.status().code()
                            + ' and saved.  All Handlers on this manifest have been notified.<br>'
                            + '<a href="'
                            + ctx
                            + '/action/industry/secured/e-manifest/home/'
                            + rcra.emanifest.handlerId
                            + '">Return to Dashboard</a>');
                        break;
                    case 'Scheduled':
                        rcra.notifications.showSuccessMessage('Manifest '
                            + self.manifestTrackingNumber()
                            + ' has been set to '
                            + self.status().code()
                            + ' and saved.  All Handlers on this manifest have been notified.  Close this message to print '
                            + 'official manifest.'
                            + '<br><a href="'
                            + ctx
                            + '/action/industry/secured/e-manifest/home/'
                            + rcra.emanifest.handlerId
                            + '">Return to Dashboard</a>');
                        break;
                    case 'Complete':
                        break;
                    default:
                        break;
                }
                self.currentStatus(lookups.status.lookupById(self.status().id()));
                scrollToElement('#dashboard-content');
                return true;
            }
            self.reviewManifest = function () {
                if(self.validToSign()) {
                    if (self.save()) {
                        pager.navigate(pager.activePage$().parentPage.find('review').path());
                    }
                }
            }

            self.deleteManifest = function () {
                rcra.notifications.showAlertDialog("Delete Manifest", "Are you sure you would like to delete this manifest?  This action cannot be undone.", {
                    type: BootstrapDialog.TYPE_WARNING,
                    buttons: [
                        {
                            label: 'Delete',
                            cssClass: 'btn-danger',
                            action: function (dialog) {
                            	console.log("deleting manifest " + rcra.emanifest.handlerId);
                                window.location.href = ctx + "/action/industry/secured/e-manifest/home/" + rcra.emanifest.handlerId;
                            }
                        }
                    ]
                })
            }

            self.selectedTransporter = ko.observable(null);
            self.selectedTransporter.subscribe(function (v) {
                self.addTransporter();
            });
            self.removeTransporter = function (t) {
                self.transporters.remove(t);
            }
            self.addTransporter = function () {
                if (self.selectedTransporter()) {
                    self.transporters.push(self.selectedTransporter());
                    setTimeout(function () {
                        // all subscriptions may not have been resolved we need to this
                        // to happen after they have been resolved.
                        // use time out to run this in a different thread.
                        self.selectedTransporter(null);
                    }, 0);
                }
            }
            self.generatorPartialEdit = ko.computed(function () {
                return self.role != 'tsdf' && self.currentStatus().id() == 3;
            });
            self.validationFields = setValidations(self);
            self.generator.subscribe(function() {
            	self.errors = ko.validation.group(self.validationFields.concat(self.generator), {
            		deep: true,
					live: true
				})
			});
            self.errors = ko.validation.group(self.validationFields, {
                deep: true,
                live: true
            });
            self.signErrors = null;
            self.validToSign = function() {
            	if(!self.signErrors) {
                    self.signErrors = ko.validation.group(setSignValidations(self), {deep: true});
				}
				if(self.errors().length > 0 && self.signErrors().length > 0) {
                    console.log("form is not valid to sign showing messages")
					if(self.errors().length > 0) {
                    	self.errors.showAllMessages();
                    }
                    if(self.signErrors().length > 0) {
                    	self.signErrors.showAllMessages();
                    }
                    return false;
				}
				else {
                    console.log("form is valid to sign");
                    return true;
				}
			}
            self.validate = function() {
            	var genErrors = ko.validation.group(self.validationFields, {deep: true, live: true});
            	if(self.errors().length > 0 || genErrors().length > 0) {
					self.errors.showAllMessages();
					genErrors.showAllMessages();
					return false;
				}
				return true;
			}
            self.formLoaded(true);
        });
    }
    self.loadForm();
    self.trackingNum.subscribe(function() {
    	self.loadForm();
	});
	self.dispose = function() {
		//TODO
    	console.log("dispose edit manifest controller");
	}
}
var ReviewManifestController = function(data, params) {
    var self = this;
    self.trackingNum = params.trackingNum;
    self.formLoaded = ko.observable(false);
    self.loadForm = function () {
        self.formLoaded(false);
        $.getJSON(ctx + '/static/json/industry/emanifest/manifests/' + self.trackingNum() + '.json', function (manifest) {
            ko.utils.extend(self, new Manifest(manifest, params.role));
            self.role = params.role;
            self.printTitle = ko.computed(function () {
                if (self.status().code() == "Pending" || self.status().code() == "Draft") {
                    return "Print Draft";
                }
                else {
                    return "Print Official";
                }
            });
            self.formLoaded(true);
        });
    }
    self.loadForm();
    self.trackingNum.subscribe(function () {
        self.loadForm();
    });
    self.dispose = function () {
        //TODO
        console.log("TODO dispose edit manifest controller");
    }
    self.editManifest = function() {

	}
}
var Manifest = function(data, role) {
	var self = this;
	data = $.extend({
		transporter : null,
		tsdf : null,
		generator : null,
		status : null,
		manifestTrackingNumber : null,
		handlingInstructions : null,
		internationalShipment : false,
		internationalShipmentInfo : null,
		additionalInfo: {},
		wasteSection : {
			wasteCollection: []
		}
	}, data);
	ko.mapping.fromJS(data, {
		'handlerComments' : {
			create : function(options) {
				return new ViewHandlerComment(options.data);
			}
		},
		'generator' : {
			create : function(options) {
				if(options.data) {
					return ko.observable(new Generator(options.data));
                }
                else {
					return ko.observable(null);
				}
			}
		},
		'transporters': {
			create: function(options) {
				return new Transporter(options.data);
			}
		},
		'status' : {
			create : function(options) {
				return ko.observable(lookups.status
						.lookupById(options.data.id));
			}
		},
		'tsdf' : {
			create : function(options) {
				if(options.data) {
					return ko.observable(new DesignatedFacility(options.data));
				}
				else {
					return ko.observable(null);
				}
			}
		},
		'wasteSection' : {
			create : function(options) {
				return ko.observable(new WasteSection(options.data, self));
			}
		},
		'internationalShipmentInfo' : {
			create : function(options) {
				return new InternationalShipmentInfo();
			}
		},
		'additionalInfo': {
			create: function(options) {
				return new AdditionalInfo(options.data);
			}
		},
		'discrepancy': {
			create: function(options) {
				return new DiscrepancySection(options.data, self);
			}
		}
	}, self);
	self.tsdfAsGenerator =  ko.observable(false);
	self.tsdfAsGenerator.subscribe(function(newVal) {
        if(newVal) {
            self.selectGenerator(self.tsdf());
            self.tsdf(null);
        }
        else {
            console.log("settting user back to tsdf");
            self.tsdf(self.generator());
            self.selectGenerator(null);
        }
	});
	self.selectGenerator = function(gen) {
		self.manualGeneratorEntry(false);
		self.generator(gen);
        setGeneratorValidations(self.generator(), self);
	}
	self.manualGeneratorEntry = ko.observable(false);
    self.editingGenerator = ko.observable(false);
    self.editGenerator = function() {
        self.editingGenerator(true);
        self.manualGeneratorEntry(true);
    }
	self.notFound = function() {
		self.generator(new Generator());
		self.manualGeneratorEntry(true);
		self.editingGenerator(false);
        setGeneratorValidations(self.generator(), self);
	}
}

var ManifestHandler = function(data) {
	var self = this;
	data = $.extend({
		epaSiteId : null,
		siteName : null,
		contactPhoneNumber : null,
		contactPhoneNumberExt : null,
		address : {},
		siteAddress : {},
		emergencyPhone : null,
		emergencyPhoneExt : null,
		signature: {}
	}, data);
	ko.mapping.fromJS(data, {
		'address': {
			create: function(options) {
				return new Address(options.data);
			}
		},
		'siteAddress': {
			create: function(options) {
				return new Address(options.data);
			}
		},
		'signature' : {
			create: function(options) {
				return ko.observable(new Signature(options.data));
			}
		}
	}, self);
	self.display = ko.computed(function() {
		return self.epaSiteId() + ' - ' + self.siteName();
	});
	self.siteAddressBackUp = null;
	self.siteAddressSame = ko.pureComputed({
		read: function() {
			return ko.mapping.toJSON(self.address) == ko.mapping.toJSON(self.siteAddress);
		},
		write: function(val) {
			if(val) {
				self.siteAddressBackUp = ko.mapping.toJS(self.siteAddress);
				ko.mapping.fromJS(ko.mapping.toJS(self.address), {}, self.siteAddress);
			}
			else {
				ko.mapping.fromJS(self.siteAddressBackUp, {}, self.siteAddress);
			}
		}
	});
	self.hasSameState = function(anotherManifestHandler){
		if (anotherManifestHandler != null && self.siteAddress != null && anotherManifestHandler.siteAddress != null) {
			return self.siteAddress.state() == anotherManifestHandler.siteAddress.state();
		}
		return false;
	};
}

var Generator = function(data) {
	var self = this;
	ko.utils.extend(self, new ManifestHandler(data));
}

var DesignatedFacility = function(data) {
	var self = this;
	ko.utils.extend(self, new ManifestHandler(data));
}

var Transporter = function(data) {
	var self = this;
	ko.utils.extend(self, new ManifestHandler(data));
}

var AdditionalInfo = function(data) {
	var self = this;
	ko.mapping.fromJS(data, {}, self);
	self.hasPreviousShipmentFlag = ko.observable(false);
	self.hasPreviousShipment = ko.pureComputed({
        read: function () {
            return self.originalManifestTrackingNumber() || self.hasPreviousShipmentFlag();
        },
		write: function(val) {
        	if (val) {
        		self.hasPreviousShipmentFlag(true);
			}
			else {
        		self.hasPreviousShipmentFlag(false);
        		self.originalManifestTrackingNumber(null);
			}
		}
    })
}

var ViewHandlerComment = function(data) {
	var self = this;
	data = $.extend({
		"label" : null,
		"description" : null,
		"epaSiteId" : rcra.emanifest.handlerId
	}, data);
	ko.mapping.fromJS(data, {}, self);
}

var UsDotDescription = function(data) {
	var self = this;
	data = $.extend({
		shippingName : null,
		hazardClass : null,
		packingGroup : null,
		unIdNumber : null,
		additionalDotInformation : null,
		wasteDescription : null,
		erResponseGuidebookNumber : null,
		emergencyPhone : null,
		emergencyPhoneExt : null,
		hazClassArray: ko.observableArray([]),
		packingGroupArray: ko.observableArray([]),
		unIdNumberArray: ko.observableArray([]),
		guideNumArray: ko.observableArray([]),
		selectedHazClass : ko.observable(),
		selectedEmergencyGuideNum: ko.observable(),
		selectedIdNum:  ko.observable(),
		selectedPackGroup: ko.observable()
	}, data);
	ko.mapping.fromJS(data, {
		'shippingName': {
			create: function(options) {
				if(options.data) {
					return ko.observable(new ShippingName(options.data));
				}
				else {
					return ko.observable(null);
				}
			}
		}
	}, self);
	self.shippingNameOrWasteDescription = ko.computed(function() {
		return self.shippingName() || self.wasteDescription();
	});
}
var Waste = function(data) {
	var self = this;
	data = $.extend({
		lineNumber: null,
		isHazardous : true,
		federalHazCodes : [],
		stateGenHazCodes : [],
		stateTsdfHazCodes : [],
		handlerComments : [],
		dotDescription : {},
		containerInfo : {},
		managementCode : null,
		managementCodeComment : null,
		specialHandlingInstructions : null,
		consentNumber: null
	}, data);
	ko.mapping.fromJS(data, {
        'dotDescription': {
            create: function(options) {
                return new UsDotDescription(options.data);
            }
        },
        'containerInfo': {
            create: function(options) {
                return new ContainerInfo(options.data);
            }
        },
        'managementCode': {
            create: function(options) {
                if(options.data) {
                    return ko.observable(new BaseLookupModel(options.data));
                }
                else {
                    return ko.observable(null);
                }
            }
        },
        'formCode': {
            create: function(options) {
                if(options.data) {
                    return ko.observable(new BaseLookupModel(options.data));
                }
                else {
                    return ko.observable(null);
                }
            }
        },
        'sourceCode': {
            create: function(options) {
                if(options.data) {
                    return ko.observable(new BaseLookupModel(options.data));
                }
                else {
                    return ko.observable(null);
                }
            }
        }
    }, self);

	self.clearFederalHazCodes = function() {
		self.federalHazCodes.removeAll();
	};
	self.clearStateGenHazCodes = function() {
		self.stateGenHazCodes.removeAll();
	}
	self.clearStateTsdfHazCodes = function() {
		self.stateTsdfHazCodes.removeAll();
	}
	self.displayWasteCodes = ko.computed(function() {
		var codes = "";
		ko.utils.arrayForEach(self.federalHazCodes(), function(elem) {
			codes += (elem) + ", ";
		});
		ko.utils.arrayForEach(self.stateGenHazCodes(), function(elem) {
			codes += (elem) + ", ";
		});
		ko.utils.arrayForEach(self.stateTsdfHazCodes(), function(elem) {
			codes += (elem) + ", ";
		});
		if (codes == '')
			return codes;
		else
			return codes.substr(0, codes.length - 2);
		;
	}, self, {
		deferEvaluation : true
	});
	self.dotDescriptionDisplay = ko.computed(function() {
		if (self.isHazardous()) {
			if (self.dotDescription.additionalDotInformation()) {
				return self.dotDescription.additionalDotInformation();
			} else {
				var text = '';
				var chemical = self.dotDescription.shippingName();
				if (chemical && chemical.shippingName && chemical.shippingName()) {
					text += (chemical.unIDNumber() + ", "+
							chemical.shippingName() + ", "
							+ chemical.hazardClass());
					if (chemical.packingGroup() != null) {
							text += ", " + chemical.packingGroup();
					}
				}
				return text;				
			}			
		} else {
			return self.dotDescription.wasteDescription();
		}
	});


	/*self.managementCode.subscribe(function(v) {
		self.managementCodeCommentVisible(v && (v.code() == 'H039' || v.code() == 'H129'));
	});*/
	self.managementCodeCommentVisible = ko.observable(false);
	self.errors = ko.validation.group(self, {deep: true});
	self.isMinimumValid = function() {
		var errors = ko.validation.group(self.dotDescription, {
			deep : true
		});
		if (errors().length <= 0) {
			return true;
		} else {
			errors.showAllMessages(true);
			return false;
		}
	}
}

var ContainerInfo = function(data) {
	var self = this;
	data = $.extend({
		number : null,
		type : null,
		notListedType : null,
		quantity : null,
		unit : null,
		density : null,
		densityUnit : null,
        provideBRInfo : false,
        formCode : null,
        formCodeComment : null,
        sourceCode : null,
        sourceCodeComment : null
	}, data);
	ko.mapping.fromJS(data, {
		'type': {
			create: function(options) {
				if(options.data) {
					return ko.observable(new BaseLookupModel(options.data));
                }
                return ko.observable(null);
			}
		},
		'unit': {
			create: function(options) {
				if(options.data) {
					return ko.observable(new BaseLookupModel(options.data));
                }
                return ko.observable(null);
			}
		}
	}, self);
	self.number.extend({
		number : true,
		min : 1
	});
	self.showDensity = ko.computed(function() {
		var densityUnitCodes = [ 'G', 'L', 'N', 'Y' ];
		return (self.unit() != null && densityUnitCodes
				.indexOf(self.unit().code()) != -1);
	}, self, {
		deferEvaluation : true
	});
    // TODO maybe change this
    self.formCode.subscribe(function(v) {
        self.formCommentVisible(v && v.code() == 'W609');
    });
	/*self.sourceCode.subscribe(function(v) {
	 self.sourceCommentVisible(v && v.code() == 'G09');
	 });*/
    self.formCommentVisible = ko.observable(false);
    self.sourceCommentVisible = ko.observable(false);
}

var Signature = function(data, params) {
	var self = this;
	data = $.extend({
        printedName: null,
            signatureDate: null
	}, data);
	ko.mapping.fromJS(data, {}, self);
}

var ContainersController = function(data, params) {
	var self = this;
	ko.utils.extend(self, params.data().containerInfo);
}

var WasteSection = function(data, form) {
	var self = this;
	$.extend({
		wasteCollection: []
	}, data);
	ko.mapping.fromJS(data, {
		'wasteCollection' : {
				create : function(options) {
					return new Waste(options.data);
				}
			}
	}, self);
	self.currentlyEditedWaste = ko.observable(null);
	self.form = form;
	self.undoList = ko.observableArray([]);
	self.addOrSaveWaste = function() {
		if (self.wasteCollection().indexOf(self.currentlyEditedWaste()) == -1) {
            setWasteValidations(self.currentlyEditedWaste(), form);
			self.wasteCollection.push(self.currentlyEditedWaste());
		}
		self.currentlyEditedWaste(null);
	}
	self.cancel = function() {
		// self.showNewWaste(false);
		self.currentlyEditedWaste(null);
	}
	self.newLineNumber = function() {
		var maxLineNumber = 0;
        ko.utils.arrayForEach(self.wasteCollection(), function(waste) {
            maxLineNumber = Math.max(waste.lineNumber(), maxLineNumber);
        });
        return ++maxLineNumber;
	}
	self.startNewWaste = function() {
		var waste = new Waste({
			lineNumber: self.newLineNumber()
		});
		setWasteValidations(waste, self.form);
		openModal('edit-waste', undefined, {
			data: {
				waste: waste,
				form: self.form,
				generatorPartialEdit: self.form.generatorPartialEdit,
				isTsdf: isTsdf(),
				tsdf: self.form.tsdf,
				generator: self.form.generator,
				internationalShipment: self.form.internationalShipment,
				save: self.save
			}
		});
	}
	self.save = function(waste) {
		console.log("saving waste");
		console.log(waste);
		var unwrappedWaste = ko.utils.unwrapObservable(waste);
        if (self.wasteCollection().indexOf(unwrappedWaste) == -1) {
            self.wasteCollection.push(unwrappedWaste);
        }
	}
	self.editWaste = function(waste) {
        openModal('edit-waste', undefined, {
            data: {
                waste: waste,
				form: self.form,
                generatorPartialEdit: self.form.generatorPartialEdit,
                isTsdf: isTsdf(),
                tsdf: self.form.tsdf,
                generator: self.form.generator,
                internationalShipment: self.form.internationalShipment
            }
        });
	}
	self.removeWaste = function(waste) {
		self.wasteCollection.remove(waste);
		self.undoList.push(waste);
	}
	self.undo = function() {
		self.wasteCollection.push(self.undoList.pop());
	}
	self.hasErrors = ko.computed(function() {
		return true;
	});
}

var WasteModalController = function(data, params) {
	var self = this;
	self.waste = ko.observable(null);
	self.refresh = function(data) {
		ko.mapping.fromJS(data, {
			'ignore': ['waste', 'form']
		}, self);
		//set to null first to destroy the components and force them to refresh.
		self.waste(null);
		self.waste(data.waste);
		self.form = data.form;
	}
	self.addAndContinue = function() {
		if(self.waste().isMinimumValid()) {
            self.save(self.waste);
            //setting to null first will refresh the components
            self.waste(null);
            rcra.notifications.showSuccessMessage("Waste was successfully added to this manifest.");
            self.waste(new Waste());
            console.log(self.form);
            setWasteValidations(self.waste(), self.form);
            $('#manifestWasteSectionModal').animate({ scrollTop: 0 }, 'slow');
        }
        else {
            $('#manifestWasteSectionModal').animate({ scrollTop: 0 }, 'slow');
		}
	}
	self.saveAndClose = function() {
		if(self.waste().isMinimumValid()) {
            self.save(self.waste);
            //set to null to tear down the components
            self.waste(null);
            return 'save-and-close';
        }
        else {
            $('#manifestWasteSectionModal').animate({ scrollTop: 0 }, 'slow');
        }
	}
}

var DotDescriptionController = function(data, params) {
	var self = this;
	ko.utils.extend(self, params.data().dotDescription);
	self.isHazardous = params.data().isHazardous;
	self.generatorPartialEdit = params.generatorPartialEdit;
	self.tsdf = params.tsdf;

	//self.additionalDotInformation("");

	self.changeSelectedPackGroup = function(packGroup)
	{
		//Check to make sure there are not multiple packing groups
		if(self.hasMultiPackGroup() == false)
		{
			//Set the selected packGroup
			self.selectedPackGroup(packGroup);
		}

		//Return the packGroup string to display
		return packGroup;
	}

	self.hasMultiPackGroup = ko.computed(function(){
		if(self.shippingName() == null)
		{
			return false;
		}
		else if(self.shippingName().packingGroup() == null)
		{
			return false;
		}
		else
		{
			return self.shippingName().packingGroup().length > 1;
		}
	}, this);

	self.changeSelectedIdNum = function(IdNum)
	{
		//Check to make sure there are not multiple id numbers
		if(self.hasMultiIdNum() == false)
		{
			//Set the selected IdNum
			self.selectedIdNum(IdNum);
		}

		//Return the IdNum string to display
		return IdNum;
	}

	self.hasMultiIdNum = ko.computed(function(){
		if(self.shippingName() == null)
		{
			return false;
		}
		else if(self.shippingName().unIDNumber() == null)
		{
			return false;
		}
		else
		{
			return self.shippingName().unIDNumber().length > 1;
		}
	}, this);

	self.changeSelectedHazClass = function(hazClass){

		//Check to make sure there are not multiple hazard classes
		if(self.hasMultiHazClass() == false)
		{
			//Set the selected hazClass
			self.selectedHazClass(hazClass);
		}

		//Return the hazClass string to display
		return hazClass;
	}

	self.hasMultiHazClass = ko.computed(function(){
		if(self.shippingName() == null)
		{
			return false;
		}
		else if(self.shippingName().hazardClass() == null)
		{
			return false;
		}
		else
		{
			return self.shippingName().hazardClass().length > 1;
		}
	}, this);

	self.changeSelectedEmergencyGuideNum = function(guideNum)
	{
		//Check to make sure there are not multiple guide numbers
		if(self.hasMultiEmergencyGuideNum() == false)
		{
			//Set the selected guideNum
			self.selectedEmergencyGuideNum(guideNum);
		}

		//Return the guideNum string to display
		return guideNum;
	}

	self.hasMultiEmergencyGuideNum = ko.computed(function(){
		if(self.shippingName() == null)
		{
			return false;
		}
		else if(self.shippingName().emergencyGuideNumber() == null)
		{
			return false;
		}
		else
		{
			return self.shippingName().emergencyGuideNumber().length > 1;
		}
	}, this);


//	self.addInfoToTextBox = function(info){
//		info = info + ", ";
//
//		//add the string to the additionalDotInformation
//		self.additionalDotInformation(self.additionalDotInformation() + info);
//	}

	self.resetProperShippingName = function(){
		//Set the shipping name object to undefined this should reset all other fields.
		self.shippingName(undefined);
		self.selectedEmergencyGuideNum(undefined);
		self.selectedHazClass(undefined);
		self.selectedIdNum(undefined);
		self.selectedPackGroup(undefined);

		//reset DOT text field
		self.additionalDotInformation("");
	}

	self.isAllInputComplete = ko.computed(function(){

		//Check if the proper shipping name object has been set
		if(self.shippingName() != null)
		{
			if((self.shippingName().hazardClass() == null || self.selectedHazClass() != null) &&
				(self.shippingName().packingGroup() == null || self.selectedPackGroup() != null) &&
				(self.shippingName().unIDNumber() == null || self.selectedIdNum() != null))
			{
				return true;
			}
			else
			{
				return false;
			}

		}
		else
		{
			return false;
		}
	}, this).extend({notify: 'always'});

	self.buildDotDescription = function () {
		var DotInputString = "";

		if(self.shippingName().unIDNumber() != null && self.selectedIdNum() != null)
		{
			DotInputString += self.selectedIdNum() + ", ";
		}

		DotInputString += self.shippingName().shippingName() + ", ";

		if(self.shippingName().hazardClass() != null && self.selectedHazClass() != null)
		{
			DotInputString += self.selectedHazClass() + ", ";
		}

		if(self.shippingName().packingGroup() != null && self.selectedPackGroup() != null)
		{
			DotInputString += self.selectedPackGroup();
		}
		if (DotInputString.trim() != '' && 
				DotInputString.trim().lastIndexOf(',') == DotInputString.trim().length-1) {	
			DotInputString = DotInputString.substr(0,DotInputString.length-2);			
		}
		return DotInputString;
	}

	self.isAllInputComplete.subscribe(function(complete){
		if(complete)
		{
			self.additionalDotInformation("");

			self.additionalDotInformation(self.buildDotDescription());
		}
		else
		{
			//if not complete return an empty string
			self.additionalDotInformation("");
		}

	}, this);

	self.shippingName.subscribe(function(){
		self.selectedEmergencyGuideNum(undefined);
		self.selectedHazClass(undefined);
		self.selectedIdNum(undefined);
		self.selectedPackGroup(undefined);

		if(self.shippingName() != null)
		{
			if(self.shippingName().hazardClass() != null)
			{
				self.hazClassArray(self.shippingName().hazardClass());
			}
			else
			{
				self.hazClassArray.removeAll();
			}
			if(self.shippingName().packingGroup() != null)
			{
				self.packingGroupArray(self.shippingName().packingGroup());
			}
			else {
				self.packingGroupArray.removeAll();
			}
			if(self.shippingName().unIDNumber() != null)
			{
				self.unIdNumberArray(self.shippingName().unIDNumber());
			}
			else
			{
				self.unIdNumberArray.removeAll();
			}
			if(self.shippingName().emergencyGuideNumber() != null)
			{
				self.guideNumArray(self.shippingName().emergencyGuideNumber());
			}
			else
			{
				self.guideNumArray.removeAll();
			}

			//hazClassArray: ko.observableArray([]),
			//packingGroupArray: ko.observableArray([]),
			//unIdNumberArray: ko.observableArray([]),
			//guideNumArray: ko.observableArray([])
		}


		//reset DOT text field
		self.additionalDotInformation("");
	}, this);
}

var WasteCodesController= function(data, params) {
	var self = this;
	ko.utils.extend(self, params.data());
    self.generatorPartialEdit = params.generatorPartialEdit;
    self.tsdf = params.tsdf;
    self.generator = params.generator;
}

var WasteHandlingController = function(data, params) {
	var self = this;
	ko.utils.extend(self, params.data());
	self.internationalShipment = params.internationalShipment;
    self.addWasteHandlerComment = function() {
        self.handlerComments.push(new ViewHandlerComment());
    }
    self.removeWasteHandlerComment = function(data) {
        self.handlerComments.remove(data);
    }
}

var InternationalShipmentInfo = function(data) {
	var self = this;
	data = $.extend({
		importToUs : true, //defaulting to true until export is supported
		city : null,
		state : null,
		dateLeaving : null
	}, data);
	ko.mapping.fromJS(data, {}, self);
	self.dateLeaving.extend({
		date : true
	});
}

var DiscrepancySection = function(data, form) {
	var self = this;
	data = $.extend({
		discrepancy: false,
		types: [],
		rejectionType: null,
		fullRejectionType: null,
		referenceTrackingNumber: null,
		alternateFacility: null,
		comment: null
		
	}, data);
	ko.mapping.fromJS(data, {}, self);
	self.showReferenceTrackingNumber = ko.computed(function() {
		return self.discrepancy() && 
			(self.rejectionType() == 'Partial' || self.types.indexOf('Residue') != -1);
	})	
	self.alternateFacilities = ko.computed(function() {
		var options = [];
		options.push(form.generator());
		return options.concat(lookups.tsdfs());
	});
}

var BaseLookupModel = function(data) {
	var self = this;
	data = $.extend({
		code: null,
		description: null
	}, data);
	ko.mapping.fromJS(data, {}, self);
	self.display = ko.computed(function() {
		try {
			return self.code() + '-' + self.description();
		}
		catch (error) {
			console.log("error computing display for lookup: " + ko.toJSON(self));
			throw error;
		}
	});
}

var ShippingName = function(data) {
	var self = this;
	data = $.extend({
		hazardClass: null,
		packingGroup: null,
	        unIDNumber:null,
        	emergencyGuideNumber: null	
	}, data);
	ko.mapping.fromJS(data, {}, self);
}

var Address = function(data) {
	var self = this;
	var data = $.extend({
		street: null,
		street2: null,
		city: null,
		state: null,
		country: null,
		zip: null
	}, data);
	ko.mapping.fromJS(data, {}, self);
}
var ProgressBar = function(data, params) {
	var self = this;
	self.statuses = ko.observableArray([]);
	ko.mapping.fromJS(data, {}, self.statuses);
	self.currentStatus = params.currentStatus;
}
var Status = function(data) {
	var self = this;
	ko.mapping.fromJS(data, {}, self);
}
var FacilitySearchController = function(data, params) {
	var self = this;
	self.epaIdNumber = ko.observable(null);
	self.epaIdNumber.extend({
		pattern: {
	    	params: '[A-Z]{2}[A-Z0-9]{2,10}',
        	message: 'EPA ID Number must start with State Code followed by 2-10 alphanumeric characters.'
		},
		required: {
			params: true,
			message: ' '//don't display message when the user enters nothing
		}
	});
	self.quickSearchError = ko.observable(null);
	self.errors = ko.validation.group([self.epaIdNumber]);
	self.epaIdNumber.subscribe(function() {
	    self.quickSearchError(null);
	    if(self.errors().length > 0) {
	        self.errors.showAllMessages();
        }
        else {
            console.log("search for " + self.epaIdNumber());
            $.ajax({
                url: ctx + "/static/json/industry/emanifest/generators.json",
                type: "GET",
                success: function (data) {
                    for (var i = 0; i < data.length; ++i) {
                        var generator = data[i];
                        console.log("comparing");
                        console.log(generator.epaSiteId);
                        console.log(self.epaIdNumber());
                        if (generator.epaSiteId == self.epaIdNumber()) {
                            params.selectGenerator(new Generator(generator));
                            return;
                        }
                    }
                    self.quickSearchError('No generator found with EPA ID: ' + self.epaIdNumber());
                }
            });
        }
	});
    postal.channel('modal').subscribe('facility-search-modal.close.selected', function(message, envelope) {
        params.selectGenerator(message.data);
    });
    postal.channel('modal').subscribe('facility-search-modal.close.not-found', function() {
    	params.notFound();
	})
}
var FacilitySearchModalController = function(data) {
	var self = this;
    self.searchCriteria = new FacilitySearchCriteria(null);
    self.criteriaErrors = ko.validation.group(self.searchCriteria, {observable: false});
    //Search criteria validation rules
    var conditionalRequiredValidator = {
        validator: function (val) {
            var criteriaFieldsEmpty = !self.searchCriteria.zip()
                && !self.searchCriteria.handlerId()
                && !self.searchCriteria.handlerName();
            return !criteriaFieldsEmpty;
        }
    };

    self.searchCriteria.state.extend({required: true});
    self.searchCriteria.handlerId.extend({validation: conditionalRequiredValidator});
    self.searchCriteria.handlerName.extend({validation: conditionalRequiredValidator});
    self.searchCriteria.zip.extend({ validation: conditionalRequiredValidator});

    self.searchResults = {
        data : ko.observableArray([])
    };

    self.conditionalCriteriaIsValid = ko.computed(function () {
        return !(!self.searchCriteria.handlerId.isValid()
        || !self.searchCriteria.handlerName.isValid()
        || !self.searchCriteria.zip.isValid());
    });

    self.conditionalValidationMessage = ko.observable(null);

    self.navigateResults = function() {

    };

    //navigation
    var pages = {
        SEARCH : "Search",
        RESULTS : "Search Results"
    }
    self.search = function() {
        console.log("search");
        if (self.criteriaErrors().length > 0) {
            self.criteriaErrors.showAllMessages(true);
            if (!self.conditionalCriteriaIsValid()) {
                var validationMessage = "Site ID, Name or Zip is required.";
                self.conditionalValidationMessage(validationMessage);
                self.conditionalCriteriaIsValid.subscribe(function (newVal) {
                    if (newVal == true) {
                        self.conditionalValidationMessage(undefined);
                    } else {
                        self.conditionalValidationMessage(validationMessage);
                    }
                });
            }
            return false;
        }
        var criteria = ko.mapping.toJS(self.searchCriteria);

        $.ajax({
            url : ctx + "/static/json/industry/emanifest/generators.json",
            type : "POST",
            data : JSON.stringify(criteria),
            contentType : rcra.xhrSettings.mimeTypes.JSON,
            beforeSend : rcra.xhrSettings.setJsonAcceptHeader,
            success : function(data) {
                ko.mapping.fromJS(data, {
                    '': {
                        create : function(options) {
                            return new Generator(options.data);
                        }
                    }
                }, self.searchResults.data);
                self.activePage(pages.RESULTS);
            }
        });
        self.showResults(true);
    }
    self.clearCriteria = function() {
        self.searchCriteria.reset();
    }
    self.activePage = ko.observable(pages.SEARCH);
    self.showSearch = ko.pureComputed({
        read: function() {
            return self.activePage() == pages.SEARCH;
        },
        write: function(value) {
            if(value) {
                self.activePage(pages.SEARCH);
            }
        }
    });
    self.showResults = ko.pureComputed({
        read: function() {
            return self.activePage() == pages.RESULTS;
        },
        write: function(value) {
            if(value) {
                self.activePage(pages.RESULTS);
            }
        }
    });
    self.selectGenerator = function(generator) {
        popupRegistry['facility-search-modal'].closeModal('selected', generator);
    }
    self.facilityNotFound = function() {
    	popupRegistry['facility-search-modal'].closeModal('not-found');
	}
}
var FacilitySearchCriteria = function(data) {
	var self = this;
	data = $.extend({
		handlerId: null,
		handlerName: null,
		streetNumber: null,
		streetName: null,
		city: null,
		state: null,
		county: null,
		zip: null
	}, data);
	ko.mapping.fromJS(data, {}, self);
	self.reset = function() {
		ko.mapping.fromJS(data, {}, self);
	}
}
function setValidations(form) {
	var validationFields = [];
	validationFields.push(form.generator);
	form.generator.extend({
		required : {
			onlyIf : function() {
				return validationApplicable(form, 'pending');
			}
		}
	});
	validationFields.push(form.tsdf);
	form.tsdf.extend({
		required : {
			onlyIf : function() {
				return validationApplicable(form, 'pending');
			}
		}
	});
	validationFields.push(form.transporters);
	form.transporters.extend({
		required : {
			onlyIf : function() {
				return validationApplicable(form, 'scheduled')
			}
		},
		minLength : {
			value : 1,
			onlyIf : function() {
				return validationApplicable(form, 'scheduled')
			}
		}
	});
	validationFields.push(form.wasteSection().wasteCollection);
	//validationFields.push(form.wasteSection().currentlyEditedWaste);
	form.wasteSection().wasteCollection.extend({
		required : {
			onlyIf : function() {
				return validationApplicable(form, 'scheduled')
			}
		},
		minLength : {
			value : 1,
			onlyIf : function() {
				return validationApplicable(form, 'scheduled')
			}
		},
		validation: {
			validator: function(wastes) {
				for(var i = 0; i < wastes.length; ++i) {
					var waste = wastes[i];
					if(waste.federalHazCodes().length > 0) {
						return true;
					}
					if(waste.stateGenHazCodes().length > 0) {
						return true;
					} 
					if(waste.stateTsdfHazCodes().length > 0) {
						return true;
					}
				}
				return false;
			},
			message: "You must select at least one waste code.",
			onlyIf: function() {
				return validationApplicable(form, 'scheduled');
			}
		}
	});
	console.log(form);
	form.additionalInfo.originalManifestTrackingNumber.extend({
		required: {
			onlyIf: function() {
				return validationApplicable(form, 'scheduled') && form.additionalInfo.hasPreviousShipment();
			}
		},
		pattern: {
			params: '[0-9]{9}[A-Z]{3}',
			message: 'Invalid format.  Tracking Number must be 9 digits followed by 3 upper case letters'
		}
	});
	validationFields.push(form.additionalInfo.originalManifestTrackingNumber);
	form.discrepancy.referenceTrackingNumber.extend({
		required: {
			onlyIf:  function() {
				return form.discrepancy.discrepancy() 
						&& form.discrepancy.showReferenceTrackingNumber()
						&& validationApplicable(form, 'received');
			}
		}
	});
	form.discrepancy.comment.extend({
		required: {
			onlyIf: function() {
				return form.discrepancy.discrepancy() && validationApplicable(form, 'received');
			}
		}
	});
	ko.utils.arrayForEach(form.wasteSection().wasteCollection, function(waste) {
		setWasteValidations(waste, form);
	});
	var generatorValidateFields = setGeneratorValidations(form.generator(), form);
	validationFields.concat(generatorValidateFields);
	for ( var i = 0; i < form.wasteSection().wasteCollection().length; ++i) {
		setWasteValidations(form.wasteSection().wasteCollection()[i], form);
	}
	return validationFields;
}
function setGeneratorValidations(generator, form) {
	if(generator) {
	    var generatorErrors = [];
		generator.siteName.extend({
			required: {
				onlyIf: function() {
					return validationApplicable(form, 'pending');
				}
			}
		});
		generatorErrors.push(generator.siteName);
		generator.address.street.extend({
			required: {
				onlyIf: function() {
					return validationApplicable(form, 'pending');
				}
			}
		});
		generator.address.city.extend({
			required: {
				onlyIf: function() {
					return validationApplicable(form, 'pending');
				}
			}
		});
		generator.address.state.extend({
			required: {
				onlyIf: function() {
					return validationApplicable(form, 'pending');
				}
			}
		});
		generator.address.zip.extend({
			required: {
				onlyIf: function() {
					return validationApplicable(form, 'pending');
				}
			}
		});
        generatorErrors.push(generator.address);
		generator.siteAddress.street.extend({
			required: {
				onlyIf: function() {
					return validationApplicable(form, 'pending');
				}
			}
		});
		generator.siteAddress.city.extend({
			required: {
				onlyIf: function() {
					return validationApplicable(form, 'pending');
				}
			}
		});
		generator.siteAddress.state.extend({
			required: {
				onlyIf: function() {
					return validationApplicable(form, 'pending');
				}
			}
		});
		generator.siteAddress.zip.extend({
			required: {
				onlyIf: function() {
					return validationApplicable(form, 'pending');
				}
			}
		});
        generatorErrors.push(generator.siteAddress);
        generator.emergencyPhone.extend({
            required : {
                onlyIf : function() {
                    return validationApplicable(form, 'pending');
                }
            }
        });
        generatorErrors.push(generator.emergencyPhone);
        generator.contactPhoneNumber.extend({
            required : {
                onlyIf : function() {
                    return validationApplicable(form, 'pending');
                }
            }
        });
        generatorErrors.push(generator.emergencyPhoneExt);
        return generatorErrors;
	}
}
function setWasteValidations(waste, form) {
	waste.dotDescription.shippingName.extend({required: {
			onlyIf: function () {
				return waste.isHazardous();
			}
		}
	});


	waste.dotDescription.selectedHazClass.extend({
		required: {
			onlyIf: function(){
				return waste.dotDescription.hazClassArray().length > 1;
			}
		}
	});

	waste.dotDescription.selectedPackGroup.extend({
		required: {
			onlyIf: function(){
				return waste.dotDescription.packingGroupArray().length > 1;
			}
		}
	});

	waste.dotDescription.additionalDotInformation.extend({required: true});


//	waste.dotDescription.selectedEmergencyGuideNum.extend({
//		required: {
//			onlyIf: function(){
//				return waste.dotDescription.guideNumArray().length > 1;
//			}
//		}
//	});
	waste.dotDescription.selectedIdNum.extend({
		required: {
			onlyIf: function(){
				return waste.dotDescription.unIdNumberArray().length > 1;
			}
		}
	});

	waste.containerInfo.formCode.extend({
		required : {
			onlyIf : function() {
				return validationApplicable(form, 'scheduled') && waste.containerInfo.provideBRInfo();
			}
		}
	});
	waste.containerInfo.sourceCode.extend({
		required : {
			onlyIf : function() {
				return validationApplicable(form, 'scheduled') && waste.containerInfo.provideBRInfo();
			}
		}
	});
	waste.containerInfo.density.extend({
		required: {
			onlyIf: function(){
				return validationApplicable(form, 'scheduled') && waste.containerInfo.provideBRInfo()
					&& waste.containerInfo.showDensity();
			}
		}
	});
	waste.containerInfo.densityUnit.extend({
		required: {
			onlyIf: function() {
				return validationApplicable(form, 'scheduled') && waste.containerInfo.provideBRInfo()
					&& waste.containerInfo.showDensity();
			}
		}
	});
	waste.managementCode.extend({
		required : {
			onlyIf : function() {
				return validationApplicable(form, "received");
			}
		}
	});
	waste.containerInfo.number.extend({
		required : {
			onlyIf : function() {
				return validationApplicable(form, "scheduled");
			}
		}
	});
	waste.containerInfo.type.extend({
		required : {
			onlyIf : function() {
				return validationApplicable(form, "scheduled");
			}
		}
	});
	waste.containerInfo.notListedType.extend({
		required : {
			onlyIf : function() {
				return validationApplicable(form, "scheduled") && waste.containerInfo.type() && waste.containerInfo.type().code() == "NL";
			}
		}
	});
	waste.containerInfo.quantity.extend({
		required: {
			onlyIf: function() {
                return validationApplicable(form, "scheduled");
			}
		}
	})
	waste.containerInfo.unit.extend({
		required : {
			onlyIf : function() {
				return validationApplicable(form, "scheduled");
			}
		}
	});
	waste.federalHazCodes.extend({
		required: {
			message: "At least one hazardous waste code (state or federal) must be selected",
			onlyIf: function() {
				return validationApplicable(form, "scheduled") &&
						waste.isHazardous() &&
						( waste.stateGenHazCodes().length <= 0 &&
						  waste.stateTsdfHazCodes().length <= 0)
			}
		}
	})
	waste.stateGenHazCodes.extend({
		required: {
			message: "At least one hazardous waste code (state or federal) must be selected",
			onlyIf: function() {
				return validationApplicable(form, "scheduled") &&
						waste.isHazardous() &&
						(waste.federalHazCodes().length <= 0 &&
						 waste.stateTsdfHazCodes().length <= 0)
			}
		}
	});
	waste.stateTsdfHazCodes.extend({
		required: {
			message: "At least one hazardous waste code (state or federal) must be selected",
			onlyIf: function() {
				return validationApplicable(form, "scheduled") &&
						waste.isHazardous() &&
						(waste.federalHazCodes().length <= 0 &&
						 waste.stateGenHazCodes().length <= 0)
			}
		}
	});
	waste.errors = ko.validation.group(waste, {deep: true});
}
function setSignValidations(form) {
    var validationFields = [];
    ko.utils.arrayForEach(form.transporters(), function(transporter) {
        transporter.signature().printedName.extend({
            required: {
                onlyIf: function () {
                    return validationApplicable(form, 'received');
                }
            }
        });
        transporter.signature().signatureDate.extend({
            required: {
                onlyIf: function () {
                    return validationApplicable(form, 'received');
                }
            }
        });
        //notifies the binding for required astericks to refresh
        transporter.signature.notifySubscribers();
        validationFields.push(transporter);
    });
    if(form.generator()) {
        form.generator().signature().printedName.extend({
            required: {
                onlyIf: function () {
                    return validationApplicable(form, 'received');
                }
            }
        });
        form.generator().signature().signatureDate.extend({
            required: {
                onlyIf: function () {
                    return validationApplicable(form, 'received');
                }
            }
        });
    }
    form.generator().signature.notifySubscribers();
    validationFields.push(form.generator());
    return validationFields;
}
function validationApplicable(form, status) {
	switch (status) {
	case 'draft':
		return form.status().order() >= 1;
	case 'pending':
		return form.status().order() >= 2;
	case 'scheduled':
		return form.status().order() >= 3;
	case 'in transit':
		return form.status().order() >= 4;
	case 'received':
		return form.status().order() >= 5;
	case 'complete':
		return form.status().order() >= 6;
	default:
		return false;
	}
}
var lookups = {};
var LookupViewModel = function(settings) {
	var self = this;
	self.value = settings.lookupArray;
	self.loadDeferred = null;
	self.load = settings.load || function() {
		if (!self.loadDeferred) {
			self.loadDeferred = $.getJSON(settings.url, function(data) {
				var options = settings.viewModel ? {
					'' : {
						create : function(options) {
							return new settings.viewModel(options.data);
						}
					}
				} : {};
				ko.mapping.fromJS(data, options, self.value);
			});
		}
		return self.loadDeferred;
	}
}
function registerLookupWithSettings(name, settings) {
	if (lookups[name]) {
		throw name + " is already a registered lookup";
	}
	if (lookups[name + 'VM']) {
		throw name
				+ "VM is already registed this name must be free to register a lookup.  This name holds the control for the lookup.";
	}
	lookups[name] = ko.observableArray([]);
	settings = $.extend({
		lookupArray : lookups[name],
		name : name
	}, settings);
	lookups[name + 'VM'] = new LookupViewModel(settings);
}
function registerLookup(name, url, viewModel) {
	registerLookupWithSettings(name, {
		url : url,
		viewModel : viewModel
	});
}
function registerLookupCustomLoad(name, loadFunc) {
	registerLookupWithSettings(name, {
		load : loadFunc
	});
}
function loadLookup(name) {
	var vm = lookups[name + 'VM'];
	if (vm) {
		return vm.load();
	} else {
		throw name + ' is not' +
		' a registered lookup';
	}
}
registerLookup('federalHazardousWasteCodeOptions', ctx
		+ '/static/json/industry/emanifest/federal-haz-codes.json', null);
registerLookup('stateHazardousWasteCodeOptions', ctx
		+ '/static/json/industry/emanifest/state-haz-codes.json', null);
registerLookup('dotDescriptions', ctx
		+ '/static/json/industry/emanifest/dot-descriptions2.json', null);
registerLookup('units', ctx + '/static/json/industry/emanifest/units.json', null);
registerLookup('containerTypes', ctx
		+ '/static/json/industry/emanifest/container-types.json', null);
registerLookup('densityUnits', ctx
		+ '/static/json/industry/emanifest/density-units.json', null);
registerLookup('formCodes', ctx + '/static/json/industry/emanifest/form-codes.json',
		null);
registerLookup('sourceCodes', ctx + '/static/json/industry/emanifest/source-codes.json',
		null);
registerLookup('guideBookNumbers', ctx
		+ '/static/json/industry/emanifest/guide-book.json', null);
registerLookup('states', ctx + '/static/json/industry/states.json', null);
registerLookup('methodCodes', ctx + '/static/json/industry/emanifest/method-codes.json',
		null);
registerLookup('transporters',
		ctx + '/static/json/industry/emanifest/transporters.json', Transporter);
registerLookup('tsdfs', ctx + '/static/json/industry/emanifest/des-facilities.json',
		DesignatedFacility);
registerLookup('status', ctx + '/static/json/industry/emanifest/statuses.json', null);

resetScroll = function() {
	$(document).scrollTop(0);
}

scrollToElement = function(id) {
	$('html, body').animate({
		scrollTop : $(id).offset().top - 50
	}, 2000);
}
// TODO find a place for this stuff
var asyncViewModelLoader = {
	loadViewModel : function(name, viewModelConfig, callback) {
        if(viewModelConfig.url && viewModelConfig.viewModelClass) {
            $.getJSON(viewModelConfig.url, function(data) {
                callback(function(params, componentInfo) {
                    var model = new viewModelConfig.viewModelClass(data, params);
                    return model;
                })
            });
        }
        else if(viewModelConfig.viewModelClass) {
            callback(function(params, componentInfo) {
                return new viewModelConfig.viewModelClass(null, params);
            });
        }
        else {
            callback(null);
        }
	},
	loadTemplate : function(name, templateConfig, callback) {
		if (templateConfig.url) {
			$.get(templateConfig.url, null, function(data) {
				callback($.parseHTML(data));
			})
		} else {
			callback(null);
		}
	}
}
var modalLoader = {
		loadViewModel: function(name, viewModelConfig, callback) {
			if(viewModelConfig.modal) {
				callback(function(params, componentInfo) {
					popupId = params.id || name;
					var settings = $.extend({
						name: popupId,
						model: viewModelConfig.viewModelClass ? new viewModelConfig.viewModelClass() : null,
					}, viewModelConfig.settings);
					popupRegistry[popupId] = new ModalControl(settings);
					postal.publish({
						channel: 'modal',
						topic: popupId + '.init'
					});
					return popupRegistry[popupId];
				});
			}
			else {
				callback(null);
			}
		},
		loadTemplate: function(name, templateConfig, callback) {
			if(templateConfig.modal) {
				$.get(ctx + '/action/industry/secured/e-manifest/components/' + templateConfig.modal, function(data) {
					callback($.parseHTML(data));
				});
			}
			else {
				callback(null);
			}
		}
	}
ko.components.loaders.unshift(asyncViewModelLoader);
ko.components.loaders.unshift(modalLoader);
ko.components.register('edit-manifest', {
	viewModel: {
        viewModelClass: EditManifestController
	},
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/edit-manifest'
	}
});
ko.components.register('review-manifest', {
    viewModel: {
        viewModelClass: ReviewManifestController
    },
    template: {
        url: ctx + '/action/industry/secured/e-manifest/components/review-manifest'
    }
});
//sections
ko.components.register('eman-progress-bar', {
	viewModel : {
		url : ctx + '/static/json/industry/emanifest/statuses.json',
		viewModelClass : ProgressBar
	},
	template : {
		url : ctx + '/action/industry/secured/e-manifest/components/progressBar'
	}
});
ko.components.register('general-info', {
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/edit/general-info'
	}
});
ko.components.register('handling-instructions', {
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/edit/handling-instructions'
	}
});
ko.components.register('international-shipment', {
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/edit/international-shipment'
	}
});
ko.components.register('transporter', {
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/edit/transporter'
	}
});
ko.components.register('waste-section', {
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/edit/waste-section'
	}
});
ko.components.register('address-info-edit', {
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/edit/address-info'
	}
});
ko.components.register('facility-info-edit', {
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/edit/facility-info'
	}
})
ko.components.register('facility-info-review', {
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/view/facility-info'
	}
});
ko.components.register('phone-info-review', {
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/view/phone-info'
	}
});
ko.components.register('general-info-review', {
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/view/general-info'
	}
});
ko.components.register('handling-instructions-review', {
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/view/handling-instructions'
	}
});
ko.components.register('international-shipment-review', {
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/view/international-shipment'
	}
});
ko.components.register('transporter-review', {
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/view/transporter'
	}
});
ko.components.register('waste-section-review', {
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/view/waste-section'
	}
});
ko.components.register('dot-description', {
	viewModel: {
		viewModelClass: DotDescriptionController
	},
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/edit/dot-description'
	}
});
ko.components.register('containers', {
    viewModel: {
        viewModelClass: ContainersController
    },
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/edit/containers'
	}
});
ko.components.register('waste-codes', {
	viewModel: {
		viewModelClass: WasteCodesController
	},
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/edit/waste-codes'
	}
});
ko.components.register('waste-handling-instructions', {
	viewModel: {
		viewModelClass: WasteHandlingController
	},
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/edit/waste-handling-instructions'
	}
});
ko.components.register('waste-codes-review', {
    viewModel: {
        viewModelClass: WasteCodesController
    },
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/view/waste-codes'
	}
});
ko.components.register('dot-description-review', {
    viewModel: {
        viewModelClass: DotDescriptionController
    },
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/view/dot-description'
	}
});
ko.components.register('containers-review', {
    viewModel: {
        viewModelClass: ContainersController
    },
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/view/containers'
	}
});
ko.components.register('waste-handling-instructions-review', {
    viewModel: {
        viewModelClass: WasteHandlingController
    },
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/view/waste-handling-instructions'
	}
})
ko.components.register('discrepancy-section', {
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/edit/discrepancy-section'
	}
});
ko.components.register('signator-section', {
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/edit/signator-section'
	}
});
ko.components.register('generator-info-generator', {
	template: {
		url: ctx + '/action/industry/secured/e-manifest/components/edit/generator-info-generator'
	}
});
ko.components.register('generator-info-tsdf', {
    template: {
        url: ctx + '/action/industry/secured/e-manifest/components/edit/generator-info-tsdf'
    }
});
ko.components.register('tsdf-info-generator', {
    template: {
        url: ctx + '/action/industry/secured/e-manifest/components/edit/tsdf-info-generator'
    }
});
ko.components.register('tsdf-info-tsdf', {
    template: {
        url: ctx + '/action/industry/secured/e-manifest/components/edit/tsdf-info-tsdf'
    }
});
ko.components.register('bs-switch', {
	template: {
		element: 'bs-switch'
	}
});
ko.components.register('facility-search', {
    viewModel: {
        viewModelClass: FacilitySearchController
    },
    template: {
		url: ctx + '/action/industry/secured/e-manifest/components/facility-search'
    }
});
//modals
ko.components.register('unsaved-data', {
	viewModel: {
		modal: true
	},
	template: {
		modal: 'unsaved-data'
	}
});
ko.components.register('edit-waste', {
	viewModel: {
		modal: true,
		viewModelClass: WasteModalController
	},
	template: {
		modal: 'edit/waste-modal'
	}
});
ko.components.register('review-waste', {
	viewModel: {
		modal: true,
		viewModelClass: WasteModalController
	},
	template: {
		modal: 'view/waste-modal'
	}
});
ko.components.register('facility-search-modal', {
	viewModel: {
		modal: true,
		viewModelClass: FacilitySearchModalController,
		settings: {
			reset: function(model) {
				console.log(model());
				model().showSearch(true);
				model().clearCriteria();
			}
		}
	},
	template: {
		modal: 'facility-search-modal'
	}
});

ko.observableArray.fn.lookup = function(value, compareFunc) {
	return ko.utils.arrayFirst(this(), function(item) {
		return compareFunc(item, value);
	});
}

ko.observableArray.fn.lookupByProp = function(value, property) {
	return this.lookup(value, function(item, value) {
		return ko.utils.unwrapObservable(item[property]) == ko.utils
				.unwrapObservable(value);
	});
}

ko.observableArray.fn.lookupById = function(value) {
	return this.lookup(value, function(item, value) {
		return ko.utils.unwrapObservable(item.id) == ko.utils
				.unwrapObservable(value);
	});
}
ko.bindingHandlers.select2 = {
	after : [ 'options', 'lookup', 'value', 'lookupValue' ],
	init : function(element, valueAccessor, allBindings) {
		var options = ko.toJS(valueAccessor()) || {};
		// timeout fixes a problem with select2 not showing the intial value.
		setTimeout(function() {
			$(element).select2(options);
			var subscribeToBinding = function(binding) {
				if (allBindings.has(binding) && allBindings()[binding] && allBindings()[binding].subscribe) {
					allBindings()[binding].subscribe(function(newVal) {
						setTimeout(function() {
							// use another thread so all other subscriptions
							// finish first
							$(element).trigger("change.select2");
						}, 0);
					});
				}
			}
			subscribeToBinding('options');
			subscribeToBinding('value');
			subscribeToBinding('lookupValue');

		}, 0);
	},
	update : function(element, valueAccessor, allBindingsAccessor, viewModel) {
		var observable = allBindingsAccessor().value || {};
		if (typeof allBindingsAccessor().selectedOptions == "function") {
			observable = allBindingsAccessor().selectedOptions;
		}
		var value = ko.utils.unwrapObservable(observable);
		$(element).select2("val", value);
		$(element).on("change",function(e){
			if (e.val == "" && e.removed != null && allBindingsAccessor()["lookupValue"]) //this is remove event
				allBindingsAccessor().lookupValue(null);
		});
	}
};
ko.dirtyFlag = function(root, isInitiallyDirty, settings) {
	if(settings && settings.initDirty) {
		isInitiallyDirty = true;
	}
    var result = function() {},
        _initialState = ko.observable(ko.mapping.toJSON(root, settings)),
        _isInitiallyDirty = ko.observable(isInitiallyDirty);

    result.isDirty = function() {    	
        return _isInitiallyDirty() || _initialState() !== ko.mapping.toJSON(root, settings);
    };

    result.reset = function() {
        _initialState(ko.mapping.toJSON(root, settings));
        _isInitiallyDirty(false);
    };
    
    result.debug = function() {
    	console.log("settings");
    	console.log(settings);
    	console.log("original data");
    	console.log(_initialState());
    	console.log("current data");
    	console.log(ko.mapping.toJSON(root, settings));
    	console.log("is dirty? " + result.isDirty());
    }
    
    return result;
};
/*
 * Modal Controls
 */
var ModalControl = function(settings) {
    var self = this;
    self.name = ko.observable(settings.name);
    self.open = ko.observable(false);
    self.popupModel = ko.observable(settings.model || {});
    self.openModal = function(params) {
    	params = params || {};
        if(params.reset) {
            self.reset();
        }
        else if(params.data) {
            var data = params.copy ? ko.mapping.toJS(params.data) : params.data;
            self.refreshData(data);
        }
        self.open(true);
    }
    self.reset = function() {
        if(!settings.reset) {
            throw "No reset function was set for modal " + self.name();
        }
        settings.reset(self.popupModel);
    }
    self.refreshData = function(data) {
    	console.log("refreshing data");
    	console.log(data);
    	if(self.popupModel().refresh) {
    		console.log("calling property on popup model");
			self.popupModel().refresh(data);
		}
		else {
    		console.log("using generic method");
            var mapSettings = settings.mapSettings || {};
            ko.mapping.fromJS(data, mapSettings, self.popupModel)
		}
    }
    self.closeModal = function(event, data) {
        self.open(false);
    	postal.publish({
            channel: "modal",
            topic: self.name() + ".close." + event,
            data: {
                result: event,
                name: self.name(),
                data: data || self.popupModel()
            }
        });
    }
}
var popupRegistry = {};

function openModal(name, id, settings) {
    var popupId = id || name;
    if(!popupRegistry[popupId]) {
        var params = {
            id: id
        };
        var subscription = postal.subscribe({
            channel: 'modal',
            topic: popupId + '.init',
            callback: function(data, envelope) {
                popupRegistry[popupId].openModal(settings);
                postal.unsubscribe(subscription);
            }
        });
        var modalComponent = $('<div data-bind="component: {name: \'' + name + '\', params: ' + ko.toJSON(params) + '}"></div>');
        $('#popups').append(modalComponent);
        ko.applyBindings(null, modalComponent.get(0));
        popupRegistry[popupId] = "pending";
    }
    else if (popupRegistry[popupId] == "pending") {
        //modal is loading
    }
    else {
        popupRegistry[popupId].openModal(settings);
    }
}
/**
 * This binding is a wrapper for the options binding. If you provide a string
 * this will look for the options in the global lookup variable. Otherwise this
 * works exactly like the options binding.
 */
ko.bindingHandlers.lookup = {
	init : function(element, valueAccessor, allBindings, viewModel,
			bindingContext) {
		var value = valueAccessor();
		var options = value.options || value;
		options = typeof options === 'string' ? lookups[options] : options;
		return ko.bindingHandlers.options.init(element, function() {
			return options
		}, allBindings, viewModel, bindingContext);
	},
	update : function(element, valueAccessor, allBindings, viewModel,
			bindingContext) {
		var value = valueAccessor();
		var options = value.options || value;
		options = typeof options === 'string' ? lookups[options] : options;
		var result = ko.bindingHandlers.options.update(element, function() {
			return options
		}, allBindings, viewModel, bindingContext);
		$(element).trigger('change.select2');
		return result;
	}
}
function retrieveOptionsFromBindings(allBindings) {
	var options = allBindings().options || allBindings().lookup;
	if (typeof options == 'string') {
		return lookups[options];
	}
	return options;
}
var debugArray = [];
ko.bindingHandlers.lookupValue = {
	init : function(element, valueAccessor, allBindings, viewModel,
			bindingContext) {
		var value = valueAccessor();
		var unwrappedValue = ko.utils.unwrapObservable(value);
		// We will need a value binding on the element so see if there is one if
		// not create it.
		var selectValue;
		// make sure we won't get any errors before trying to initialize it so
		// we can provide a better message to the user.
		if (allBindings.has('optionsValue')) {
			// TODO initialize this
			selectValue = ko.observable();
			debugArray.push(selectValue);
		} else {// friendly error the user so they can fix the problem
			throw "When using the lookupValue binding you must provide the 'optionsValue' binding";
		}
		// get the lookup array for this select from the options binding and set
		// up a function so we can find values in the lookup.
		var selectArray = retrieveOptionsFromBindings(allBindings);
		var comparisionFunc = function(item, value) {
			return ko.utils.unwrapObservable(item[allBindings().optionsValue]) == ko.utils
					.unwrapObservable(value);
		};
		// see if we have a property already if so we will need to update the
		// value attribute so the select list gets updated correctly.
		if (unwrappedValue
				&& unwrappedValue[allBindings().optionsValue]
				&& unwrappedValue[allBindings().optionsValue]()) {
			selectValue(unwrappedValue[allBindings().optionsValue]());
		}
		// the select value may also be defaulted if so update the lookupValue
		else if (ko.utils.unwrapObservable(selectValue)) {
			var val = ko.utils.arrayFirst(selectArray(), function(item) {
				return comparisionFunc(item, ko.utils
						.unwrapObservable(selectValue));
			});
			value(val);
		}
		// set up the subscribe event so we can keep the main object updated
		// when the select changes
		selectValue.subscribe(function(newVal) {
			if (newVal) {
				var val = ko.utils.arrayFirst(selectArray(), function(item) {
					return comparisionFunc(item, ko.utils
							.unwrapObservable(newVal));
				});
				value(val);
			}
		});
		// if the lookupValue property changes we need to copy the property to
		// the select value so the drop down updates
		if (!(value)) {
			throw "The value your provided to the lookupValue binding is "
					+ value
					+ ".  This must be defined for the lookupValue to work.";
		}
		if(!value.subscribe) {
			console.log(value)
			throw "The value you provided must be an observable for the lookupValue binding to work.";
		}
		value.subscribe(function(newVal) {
			if (newVal) {
				selectValue(ko.utils
						.unwrapObservable(newVal[allBindings().optionsValue]));
			} else {
				selectValue(undefined);
			}
		});
		// if the options change we need to look up the id again
		var options = retrieveOptionsFromBindings(allBindings);
		if (!(options)) {
			throw "The options provided in your select is "
					+ allBindings().options
					+ ".  This must be defined for the lookupValue to work.  Did you forget to add the options or lookup binding to your select?  If you are mapping it asynchronously try setting it to ko.observableArray([])";
		}
		options.subscribe(function(newOpts) {
			var val = ko.utils.arrayFirst(selectArray(), function(item) {
				return comparisionFunc(item, ko.utils
						.unwrapObservable(selectValue));
			});
			value(val);
		});
		// bind the temporary variable to the value binding so it gets updated.
		return ko.bindingHandlers.value.init(element, function() {
			return selectValue
		}, allBindings, viewModel, bindingContext);
	}
}
//add lookupValue to the validatable bindings so the user can see validation messages
ko.validation.makeBindingHandlerValidatable("lookupValue");
ko.bindingHandlers.BSModal = {
	init : function(element, valueAccessor) {
		var value = valueAccessor();
		$(element).modal({
			keyboard : false,
			show : ko.unwrap(value),
			backdrop: 'static'
		});
	},
	update : function(element, valueAccessor) {
		var value = valueAccessor();
		ko.unwrap(value) ? $(element).modal('show') : $(element).modal('hide');
	}
};
ko.bindingHandlers.modal = {
	init: function(element, valueAccessor, allbindings, viewModel, bindingContext) {
		var settings = valueAccessor();
		return ko.bindingHandlers.click.init(element, function() {
			return function() {
				openModal(settings.name, settings.id, settings.params);
			}
		}, allbindings, viewModel, bindingContext)
	}
}
ko.bindingHandlers.close = {
	init: function(element, valueAccessor, allbindings, viewModel, bindingContext) {
		var value = valueAccessor();
		return ko.bindingHandlers.click.init(element, function() {
			return function() {
				if(typeof value == "function") {
					var result = value()
					if(result) {
						bindingContext.$data.closeModal(result);
					}
				}
				else {
					bindingContext.$data.closeModal(value);
                }
			}
		}, allbindings, viewModel, bindingContext)
	}
}
ko.bindingHandlers.consentNumber = {
	init: function(element, valueAccessor, allBindings, viewModel, bindingContext) {
		var mask = "999999I99999";
		ko.bindingHandlers.maskedInput.init(element, valueAccessor, allBindings, viewModel, mask);
	},
	update: function(element, valueAccessor, allBindings, viewModel, bindingContext) {
		ko.bindingHandlers.maskedInput.update(element, valueAccessor, allBindings, viewModel, bindingContext);
	}
};
ko.bindingHandlers.manifestTrackingNumber = {
	init: function(element, valueAccessor, allBindings, viewModel, bindingContext) {
        var mask = "999999999AAA";
        ko.bindingHandlers.maskedInput.init(element, valueAccessor, allBindings, viewModel, mask);
    },
	update: function(element, valueAccessor, allBindings, viewModel, bindingContext) {
		ko.bindingHandlers.maskedInput.update(element, valueAccessor, allBindings, viewModel, bindingContext);
	}
}
ko.bindingHandlers.fadeVisible = {
    init: function(element, valueAccessor) {
        // Initially set the element to be instantly visible/hidden depending on the value
        var value = valueAccessor();
        $(element).toggle(ko.unwrap(value)); // Use "unwrapObservable" so we can handle values that may or may not be observable
    },
    update: function(element, valueAccessor) {
        // Whenever the value subsequently changes, slowly fade the element in or out
        var value = valueAccessor();
        ko.unwrap(value) ? $(element).fadeIn() : $(element).fadeOut();
    }
};

ko.bindingHandlers.slideVisible = {
    init: function(element, valueAccessor) {
        // Initially set the element to be instantly visible/hidden depending on the value
        var value = valueAccessor();
        $(element).toggle(ko.unwrap(value)); // Use "unwrapObservable" so we can handle values that may or may not be observable
    },
    update: function(element, valueAccessor) {
        // Whenever the value subsequently changes, slowly fade the element in or out
        var value = valueAccessor();
        ko.unwrap(value) ? $(element).slideDown() : $(element).slideUp();
    }
};
//grabbed this from br submission view
rcra.truncate = function(description, cutoff) {
    var wordBreak = true;

    description = description.toString(); // cast numbers

    if (description.length < cutoff) {
        return description;
    }

    var shortened = description.substr(0, cutoff - 1);

    // Find the last white space character in the string
    if (wordBreak) {
        shortened = shortened.replace(/\s([^\s]*)$/, '');
    }

    return shortened + '...';
};
