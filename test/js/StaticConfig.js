var stringRandom = require('string-random');

var Tables = [
    {
        tableName: 'Accounts',
        raw:[
        {'field':'ID', 'type':'varchar','length':64,'PK':1},
        {'field':'AccountName', 'type':'varchar','length':128},
        {'field':'AccountAddress', 'type':'varchar','length':64},
        {'field':'Roler', 'type':'varchar','length':64},
        {'field':'CreateTime', 'type':'datetime'},
        {'field':'Tel', 'type':'varchar','length':16}]
    },
    {
        tableName: 'Rolers',
        raw:[
        {'field':'ID', 'type':'varchar','length':64,'PK':1},
        {'field':'Name', 'type':'varchar','length':128}],
    },
    {
        tableName: 'FileItems',
        raw:[
        {'field':'ID', 'type':'varchar','length':64,'PK':1},
        {'field':'Name', 'type':'varchar','length':128},
        {'field':'CreateTime', 'type':'datetime'}],
    },
    {
        tableName: 'BindRoleWithFileItem',
        raw:[
        {'field':'ID', 'type':'varchar','length':64,'PK':1},
        {'field':'FileItemID', 'type':'varchar','length':64},
        {'field':'Roler', 'type':'varchar','length':64},
        {'field':'Active', 'type':'int'}]
    },
    {
        tableName: 'Projects',
        raw:[
        {'field':'ID', 'type':'varchar','length':64,'PK':1},
        {'field':'Name', 'type':'varchar','length':128},
        {'field':'Manager', 'type':'varchar','length':128},
        {'field':'TradePool', 'type':'varchar','length':128},
        {'field':'Beneficiary', 'type':'varchar','length':128},
        {'field':'Scale', 'type':'varchar','length':12},
        {'field':'Credibility', 'type':'int'},
        {'field':'Remark', 'type':'varchar','length':400},
        {'field':'StartTime', 'type':'datetime'}]
    },
    {
        tableName: 'BindRoleWithProject',
        raw:[
        {'field':'ID', 'type':'varchar','length':64,'PK':1},
        {'field':'ProjectID', 'type':'varchar','length':64},
        {'field':'RoleID', 'type':'varchar','length':64},
        {'field':'AccountID', 'type':'varchar','length':64}]
    },
    {
        tableName: 'UploadedFileItem',
        raw:[
        {'field':'ID', 'type':'varchar','length':64,'PK':1},
        {'field':'ProjectID', 'type':'varchar','length':64},
        {'field':'FileItemID', 'type':'varchar','length':64},
        {'field':'Hash', 'type':'varchar','length':64},
        {'field':'Attachment', 'type':'varchar','length':128},
        {'field':'UploadTime', 'type':'datetime'},
        {'field':'Remark', 'type':'varchar','length':400},
        {'field':'Version', 'type':'varchar','length':64},
        {'field':'Finished', 'type':'int'}]
    },
    {
        tableName: 'Feedback',
        raw:[
        {'field':'ID', 'type':'varchar','length':64,'PK':1},
        {'field':'ProjectID', 'type':'varchar','length':64},
        {'field':'UploadedID', 'type':'varchar','length':64},
        {'field':'Provider', 'type':'int'},
        {'field':'Status', 'type':'int'},
        {'field':'Comments', 'type':'varchar','length':400},
        {'field':'DissentHash', 'type':'varchar','length':64},
        {'field':'ProvideTime', 'type':'datetime'}]
    }
];

var NewAccounts = [
    {ID:stringRandom(12), AccountName:'招商银行股份有限公司'},
    {ID:stringRandom(12), AccountName:'华润深国投有限公司'},
    {ID:stringRandom(12), AccountName:'中债资信评估有限公司'},
    {ID:stringRandom(12), AccountName:'中诚信国际信用评级有限责任公司'},
    {ID:stringRandom(12), AccountName:'北京市中伦律师事务所'},
    {ID:stringRandom(12), AccountName:'德勤华永会计师事务所'}
];

var Records = [
    {
        tableName: 'Accounts',
        values: NewAccounts
    },
    {
        tableName: 'Rolers',
        values: [
            {ID:stringRandom(12), Name:'委托人/发起机构'},
            {ID:stringRandom(12), Name:'受托人/受托机构/发行人'},
            {ID:stringRandom(12), Name:'主承销商/簿记管理人'},
            {ID:stringRandom(12), Name:'贷款服务机构'},
            {ID:stringRandom(12), Name:'审计师'},
            {ID:stringRandom(12), Name:'法律顾问'},
            {ID:stringRandom(12), Name:'会计顾问/税务顾问'},
            {ID:stringRandom(12), Name:'评级机构'},
            {ID:stringRandom(12), Name:'承销团'},
            {ID:stringRandom(12), Name:'资金保管机构'},
            {ID:stringRandom(12), Name:'受益人'}
        ]
    },
    {
        tableName: 'FileItems',
        values: [
            {ID:stringRandom(12), Name:'主定义表'},
            {ID:stringRandom(12), Name:'信托合同'},
            {ID:stringRandom(12), Name:'服务合同'},
            {ID:stringRandom(12), Name:'资金保管合同'},
            {ID:stringRandom(12), Name:'主承销协议'},
            {ID:stringRandom(12), Name:'承销团协议'},
            {ID:stringRandom(12), Name:'收费文件'},
            {ID:stringRandom(12), Name:'现金流'},
            {ID:stringRandom(12), Name:'信托月报'}
        ]
    }
];

var ChainSQLEntry = {
    URL: 'ws://127.0.0.1:6007',
    RootAccount:{
        'secret': 'xnoPBzXtMeMyMHUVTgbuqAfg1SUTb',
        'address': 'zHb9CJAWyB4zj91VRWn96DkukG4bwdtyTh'
    },
};

var MYSQLEntry = {
    host: 'SKY-20160717UWK',
    port: 3306,
    user: 'root',
    pwd: '3.16',
    db: 'ripple',
    charset: 'utf8'
};

var LoginKeys = {
    secret: 'poc',
    savePath: './accounts/'
};

module.exports = {
    Tables:                 Tables,
    Records:                Records,
    NewAccounts:            NewAccounts,

    ChainSQLEntry:          ChainSQLEntry,
    MYSQLEntry:             MYSQLEntry,
    LoginKeys:              LoginKeys,
};
