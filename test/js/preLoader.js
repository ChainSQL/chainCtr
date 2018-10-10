var tools = require('./tools');
var config = require('./StaticConfig');
var Progress = require('./progress_bar');
var fs = require('fs');

chainsqlapi = require('chainsql').ChainsqlAPI;
chainSQL = new chainsqlapi();

// initial
chainsql_ws = config.ChainSQLEntry.URL;
chainsql_root = config.ChainSQLEntry.RootAccount;
var needNewAccounts = config.NewAccounts.length;
var newAccounts = new Array();

var createAccountPb = {
	pb: new Progress('账户创建', 50),
	completed: 0,
	total: needNewAccounts
};

var createTablePb = {
	pb: new Progress('表创建  ', 50),
	completed: 0,
	total: 0
};

var dropTablePb = {
	pb: new Progress('删除表  ', 50),
	completed: 0,
	total: 0
};

var grantPb = {
	pb: new Progress('表授权  ', 50),
	completed: 0,
	total: 0
};

var insertPb = {
	pb: new Progress('数据导入', 50),
	completed: 0,
	total: 0
};

var AccountPb = {
	pb: new Progress('账户文件', 50),
	completed: 0,
	total: needNewAccounts
};

function set_invokers() {

	if(fs.existsSync(config.LoginKeys.savePath) === false) {
		console.log('Path `' + config.LoginKeys.savePath + '` don\'t exists,so please create it first.');
		return;
	}
	
	for (var i = 0; i < needNewAccounts; i++) {
		tools.setup_invoker(createAnAccount);
	}
	tools.setup_invoker(sayBanner, '\r');

	// drop tables before creating tables
	dropTablePb.total = config.Tables.length;
	for(var x = 0; x < config.Tables.length; x++) {
		tools.setup_invoker(DropTable, config.Tables[x]);
	}
	tools.setup_invoker(sayBanner, '\r');

	// create tables
	createTablePb.total = config.Tables.length;
	for(var x = 0; x < config.Tables.length; x++) {
		tools.setup_invoker(CreateTable, config.Tables[x]);
	}
	tools.setup_invoker(sayBanner, '\r');

	// grants
	grantPb.total = needNewAccounts*config.Tables.length;
	for (var idx = 0; idx < needNewAccounts; idx++) {
		for (var y = 0; y < config.Tables.length; y++) {
			tools.setup_invoker(grant, {
				tableName: config.Tables[y].tableName,
				account: idx
			});
		}
	}
	tools.setup_invoker(sayBanner, '\r');

	// pre-load data into tables
	insertPb.total = config.Records.length;
	for(var z = 0; z < config.Records.length; z++) {
		var o = config.Records[z];
		tools.setup_invoker(insertRecord,{tableName: o.tableName, records: o.values});
	}
	tools.setup_invoker(sayBanner, '\r');

	// create login keys
	tools.setup_invoker(createLoginKeys);
	tools.setup_invoker(Done);
}

function createAnAccount() {
	var newAccount = chainSQL.generateAddress();

	createAccountPb.pb.render({
		completed: createAccountPb.completed,
		total: createAccountPb.total
	});

	chainSQL.pay(newAccount.address, 10)
	.then(function (data) {
		if (data.resultCode === 'tesSUCCESS') {
			newAccounts.push(newAccount);
			//console.log('Create a new account successfully. ', JSON.stringify(newAccount));
			createAccountPb.pb.render({
				completed: ++createAccountPb.completed,
				total: createAccountPb.total
			});
			tools.invoke();
		} else {
			console.log('\nCreate a new account unsuccessfully. ', JSON.stringify(data));
		}
	})
	.catch(function (error) {
		console.log('\nCreate a new account raise an exception. ', JSON.stringify(error));
	});
}

function sayBanner(say) {
	console.log(say);
	tools.invoke();
}

function DropTable(tableObject) {
	dropTablePb.pb.render({
		completed: dropTablePb.completed,
		total: dropTablePb.total
	});

	function next() {
		dropTablePb.pb.render({
			completed: ++dropTablePb.completed,
			total: dropTablePb.total
		});
		tools.invoke();
	}

	chainSQL.dropTable(tableObject.tableName)
	.submit({expect: 'validate_success'})
	.then(function(data) {
		if(data.status === 'validate_success') {
			next();
		} else {
			console.log('\nDrop a ', tableObject.tableName, ' table unsuccessfully. reason: ', data.status);
		}
	}).catch(function(error) {
		if(error.resultCode === 'tefTABLE_NOTEXIST') {
			next();
		} else {
			console.log('\nDrop a ', tableObject.tableName, ' table unsuccessfully. Exception reason: ', JSON.stringify(error));
		}
	});
}

function CreateTable(tableObject) {

	createTablePb.pb.render({
		completed: createTablePb.completed,
		total: createTablePb.total
	});

	chainSQL.createTable(tableObject.tableName, tableObject.raw)
	.submit({expect: 'validate_success'})
	.then(function(data) {
		if(data.status === 'validate_success') {
			//console.log('Create a ', tableObject.tableName, ' table successfully. ' );
			createTablePb.pb.render({
				completed: ++createTablePb.completed,
				total: createTablePb.total
			});
			tools.invoke();
		} else {
			console.log('\nCreate a ', tableObject.tableName, ' table unsuccessfully. reason: ', data.status);
		}
	}).catch(function(error) {
		console.log('\nCreate a ', tableObject.tableName, ' table unsuccessfully. Exception reason: ', JSON.stringify(error));
	});
}

function grant(grantObject) {
	if(grant.account >= newAccounts.length) {
		return;
	}

	grantPb.pb.render({
		completed: grantPb.completed,
		total: grantPb.total
	});
	
	var account = newAccounts[grantObject.account];
	var role = {select:true,insert:true,update:true,delete:false};
	chainSQL.grant(grantObject.tableName, account.address, 
		role)
	.submit({expect: 'validate_success'})
	.then(function (data) {
		if (data.status === 'validate_success') {
			grantPb.pb.render({
				completed: ++grantPb.completed,
				total: grantPb.total
			});

			tools.invoke();
		} else {
			console.log('\nGrant a ', account.address, 
						' with role [', grantObject.tableName,
						' , ', JSON.stringify(role),
						'] unsuccessfully. reason: ', data.status );

		}
	}).catch(function(error) {
			console.log('\nGrant a ', account.address, 
						' with role [', grantObject.tableName,
						' , ', JSON.stringify(role),
						'] unsuccessfully. Exception reason: ', JSON.stringify(error) );
	});
}

function insertRecord(recordObject) {
	var records = recordObject.records;
	var tableName = recordObject.tableName;

	insertPb.pb.render({
		completed: insertPb.completed,
		total: insertPb.total
	});

	if(tableName === 'Accounts') {
		for(var i = 0; i < needNewAccounts; i++) {
			records[i].AccountAddress = newAccounts[i].address;
		}
	}

	chainSQL.table(tableName).insert(records).submit({
		expect: 'validate_success'
	}).then(function(data) {
        if (data.status === 'validate_success') {
			//console.log('Load data successfully in ', tableName);
			insertPb.pb.render({
				completed: ++insertPb.completed,
				total: insertPb.total
			});
			tools.invoke();
        } else {
			console.log('\nLoad data unsuccessfully in ', tableName, '. reason: ', data.status);
		}
	}).catch(function(e) {
			console.log('\nLoad data unsuccessfully in ', tableName, '. exception reason: ', JSON.stringify(e));
	});
}

function createLoginKeys() {
	var saveFiles = new Array();
	for(var i = 0; i < needNewAccounts; i++) {
		var enryption = tools.encrypt(JSON.stringify(newAccounts[i]), config.LoginKeys.secret);
		var saveFile = config.LoginKeys.savePath + config.NewAccounts[i].AccountName;
		try {
			fs.writeFileSync(saveFile, enryption);
		} catch(e) {
			console.log(e);
		} finally {
			saveFiles.push(saveFile);

			AccountPb.pb.render({
				completed: i + 1,
				total: AccountPb.total
			});
		}
	}

	// print all files 
	console.log('\n');
	console.log(saveFiles);
	console.log('总共保存 ' + saveFiles.length + ' 个账户文件');

	tools.invoke();
}

function Done() {
	console.log('All Done.');
	process.exit(0);
}

function load() {
	chainSQL.connect(chainsql_ws, function (error, data) {
		if (error) {
			console.log('connect chainsql failure. ', chainsql_ws);
			console.log('reason: ', error);
		} else {
			chainSQL.as(chainsql_root);	
			set_invokers();
			tools.invoke();
		}
	});
}

module.exports = {
	load:load
};