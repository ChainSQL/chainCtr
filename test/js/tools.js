var crypto = require('crypto');

const functionEntry = function(fun, arguments) {
    this.fun = fun;
    this.arguments = arguments;
}

const functionChain = function(callback) {
    this.callback = callback;
    this.functionlist = []; // list of functionEntry
    this.stack_head = -1;
    this.stack_tail = -1;
    this.default_callback = null;
}

functionChain.prototype.push = function(entry) {
    this.functionlist.push(entry);
    this.stack_tail++;
}

functionChain.prototype.pop = function() {
    if ((this.stack_head++) > this.stack_tail) {
        return null;
    }
    
    return this.functionlist[this.stack_head];
}

Function.prototype.getName = function(){
    return this.name || this.toString().match(/function\s*([^(]*)\(/)[1]
}

funcChain = new functionChain();

function invoke() {
    var f = funcChain.pop();
    if(f != null) {
        if (f.fun.getName() === 'assign') {
            f.fun(f.arguments.tableName,f.arguments.user); 
        } else if (f.fun.getName() === 'renameTable') {
            f.fun(f.arguments.tableName,f.arguments.newTableName);
        } else {
            f.fun(f.arguments);   
        }
    }
}

function setup_invoker(f, args) {
    funcChain.push(new functionEntry(f, args));
}

function invoke_expect() {
    var f = funcChain.pop();
    if(f != null) {
        f.fun(f.arguments.tableName,f.arguments.expect, f.arguments.message);
    }
}

module.exports = {
    invoke: invoke,
    setup_invoker: setup_invoker,
    invoke_expect: invoke_expect
};


/**
 * 加密函数
 * @param text      需要加密的内容
 * @param secret    秘钥
 * @returns {Query|*}  密文
 */
function encrypt(text, secret) {
    var cipher = crypto.createCipher('aes-256-cbc', secret);
    var crypted = cipher.update(text, 'utf8', 'hex');
    crypted += cipher.final('hex');
    return crypted;
}
module.exports.encrypt = encrypt;

/**
 * 解密函数
 * @param encrytion     需要解密的内容
 * @param secret        秘钥
 * @returns {Query|*}
 */
function decrypt(encrytion, secret) {
    var dec;
    try {
        var decipher = crypto.createDecipher('aes-256-cbc', secret);
        dec = decipher.update(encrytion, 'hex', 'utf8');
        dec += decipher.final('utf8');
    } catch (e) {}
    return dec;
}
module.exports.decrypt = decrypt;