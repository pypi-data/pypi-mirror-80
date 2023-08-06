define([
    'base/js/namespace',
    'base/js/events'
], function(Jupyter) {

    var Notebook = require('notebook/js/notebook').Notebook
    "use strict";
    var mod_name = "DolphinDB Extension";
    var log_prefix = ' [' + mod_name + '] ';
	
	var creds;

	var handle_output = function(out) {
		console.log(out);
		if(out.msg_type === "stream") {
			var json_text = out.content.text;
			var res = JSON.parse(json_text);
			console.log(res);
			creds = res;
		}
	};

	var retrieve_creds = function() {
		var code_input = 'retrieve-credentials';
		var kernel = Jupyter.notebook.kernel;
		var callbacks = { 'iopub' : {'output' : handle_output}};
		kernel.execute(code_input, callbacks, {silent: false});
	};

	retrieve_creds();

    var getUserInput = function() {
		require([
			'jquery',
			'base/js/dialog'
		], function($, dialog) {
			// user's selection: to be determined when onchange event gets triggered later
			var idx = null; 
			var server = null;
			var port = null;
			var username = null;
			var password = null;
			// radio buttons for selection
			var selection = $('<table class="table" id="cred"/>');
			for(var item in creds) {
				var cred = creds[item];
				var option = cred['server'] + ': ' + cred['port'] + ' - ' + cred['user'];
				selection.append($('<tr><td><input name="option" type="radio" onclick="document.option_selected(this)" value=' + item + '>' + '		' + option + '</td></tr>'));
			}
			// body
			var body = $('<div/>');
			body.append($('<h4/>').text('Select server'));
			body.append($('<p/>').html(selection));
			// onclick event on radio buttons
			document.option_selected = function(myRadio) {
				idx = myRadio.value;
				var selected = creds[idx];
				server = selected['server'];
				port = selected['port'];
				username = selected['user'];
				password = selected['password'];
			};
			// dialog
			dialog.modal({
				title: 'Connect to DolphinDB',
				body: body,
				buttons: {
					// use selected one from previous and connect to ddb
					'Connect': {
						class: "btn-primary",
						click: function() {
							if(idx === null) {
								alert('Please select the credential you want to use to connect to DolphinDB server :)');
							} else {
								Jupyter.notebook.kernel.execute('connect-to-ddb-pre ' + server + ' ' + port + ' ' + username + ' ' + password);
							}
						}
					},
					// get new credential from user input
					'New': {
						class: "btn-success",
						click: function() {
							// disable keyboard shortcuts temporarily
							Jupyter.keyboard_manager.disable();
							// get user's new credential through html form in dialog
							var body = $('<div/>');
							body.append($('<h4/>').text('Please enter your new credential info'));
							body.html(
								'<form>\
								<div class="form-group">\
								<label for="server">Server: </label>\
								<input class="form-control" id="server" type="text">\
								</div>\
								<div class="form-group">\
								<label for="port">Port: </label>\
								<input class="form-control" id="port" type="text">\
								</div>\
								<div class="form-group">\
								<label for="username">Username: </label>\
								<input class="form-control" id="username" type="text">\
								</div>\
								<div class="form-group">\
								<label for="password">Password: </label>\
								<input class="form-control" id="password" type="password">\
								</div>\
								</form>'
							);
							// dialog
							dialog.modal({
								title: 'Connect to DolphinDB',
								body: body,
								buttons: {
									'Save & Connect': {
										class: "btn-primary",
										click: function() {
											// use user's input to connect to DolphinDB
											var server = $("#server").val();
											var port = $("#port").val();
											var username = $("#username").val();
											var password = $("#password").val();
											Jupyter.notebook.kernel.execute('connect-to-ddb-new ' + server + ' ' + port + ' ' + username + ' ' + password);
										}
									},
									'Cancel': {}
								}
							});
							return true;
						}
					},
					// delete selected credential
					'Delete': {
						click: function() {
							if(idx === null) {
								alert('Please select the credential you want to delete');
							} else {
								Jupyter.notebook.kernel.execute('delete-cred-at ' + idx);
								alert('Completed deletion of the credential you selected :)');
							}
						}
					}
				}
			});
			return true;
		});        
    };

    var dolphinDB_button = function() {
        var action = {
            icon: 'fa-user',
            help: 'Connect to DolphinDB Server',
            help_index: 'zz',
            handler: getUserInput
        };
        var prefix = 'dolphindb_extensions';
        var action_name = 'get-user-input';
        var full_action_name = Jupyter.actions.register(action, action_name, prefix);
        Jupyter.toolbar.add_buttons_group([full_action_name]);
    };

    var load_ipython_extension = function() {
        // if a dolphindb_kernel is available: add button
        if(typeof Jupyter.notebook.kernel !== "undefined" && Jupyter.notebook.kernel !== null && Jupyter.notebook.kernel.name === 'dolphindb') {
            console.log(log_prefix + 'Kernel is available -- DolphinDB_Extension initializing ');
            dolphinDB_button();
        }
        // else (kernel is not ready): do nothing, wait for the kernel
    };

    return {
        load_ipython_extension: load_ipython_extension
    };
});

