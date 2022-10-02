
// 生成随机数的类
var XorShift = function() {
    function t() {}
    return Object.defineProperty(t, "instance", {
        get: function() {
            return this._instance || (this._instance = new t()), this._instance;
        },
        enumerable: !1,
        configurable: !0
    }), t.prototype.setSeed = function(t) {
        if (!Array.isArray(t) || 4 !== t.length) throw new TypeError("seed must be an array with 4 numbers");
        this._state0U = 0 | t[0], this._state0L = 0 | t[1], this._state1U = 0 | t[2], this._state1L = 0 | t[3];
    }, t.prototype.randomint = function() {
        var t = this._state0U, e = this._state0L, o = this._state1U, n = this._state1L, i = (n >>> 0) + (e >>> 0), a = o + t + (i / 2 >>> 31) >>> 0, r = i >>> 0;
        this._state0U = o, this._state0L = n;
        var c = 0, s = 0;
        return c = (t ^= c = t << 23 | (-512 & e) >>> 9) ^ o, s = (e ^= s = e << 23) ^ n, 
        c ^= t >>> 18, s ^= e >>> 18 | (262143 & t) << 14, c ^= o >>> 5, s ^= n >>> 5 | (31 & o) << 27, 
        this._state1U = c, this._state1L = s, [ a, r ];
    }, t.prototype.random = function() {
        var t = this.randomint();
        return 2.3283064365386963e-10 * t[0] + 2.220446049250313e-16 * (t[1] >>> 12);
    }, t._instance = null, t;
}();

// 打乱数组的方法
function shuffle(array, seed) {
    var xorshift = XorShift.instance;
    // 设置随机种子
    xorshift.setSeed(seed);
    // 先获取一次随机值
    xorshift.random();
    // 数组下标从后往前遍历
    for (var i = array.length - 1; i >= 0; i--) {
        // 获取0到1之间的随机值
        var random = xorshift.random();
        // 计算出随机的下标
        var j = Math.floor(random * (i + 1));
        // 交换两个下标
        var temp = array[j];
        array[j] = array[i];
        array[i] = temp;
    }
    // 将数组反序排列
    array.reverse();
    return array;
}

// 测试方法
function test() {
    var numbers = [
        1, 1, 1,
        2, 2, 2,
        3, 3, 3,
    ];
    console.log(numbers);

    var seed = [0, 0, 0, 0];
    shuffle(numbers, seed);
    console.log(numbers);

    var type2name = {
        1 : "🌱",
        2 : "🥕",
        3 : "🌽",
    };
    var names = [];
    for (var i = 0; i < numbers.length; i++) {
        names.push(type2name[numbers[i]]);
    }
    console.log(names);
}

//test()
