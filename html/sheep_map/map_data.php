<?php header("Content-Type: application/x-javascript; charset=UTF-8");?>
<?php
    class MyDB extends SQLite3{
        function __construct(){
            $this->open('../sheep_maps.db');
        }
    }
    $db = new MyDB();
    if(!$db){
        echo "window.alert('".$db->lastErrorMsg()."');\n";
        //echo $db->lastErrorMsg();
    } else {
        echo "console.log('成功打开数据文件');\n";
        //echo "成功创建或打开数据文件\n";
    }
    if(is_array($_GET)&&count($_GET)>0){//判断是否有Get参数
        if(isset($_GET["id"])){//判断所需要的参数是否存在，isset用来检测变量是否设置，返回true or false
            $id = $_GET["id"];//存在
        }
    }
    if($id == null){
        $ret1 = $db->query("SELECT MAX(ID),MAP_INFO from MAPS");
        while($row = $ret1->fetchArray()){
            $map_info = $row["MAP_INFO"];
            $id = $row["MAX(ID)"];
            echo "const map_data = $map_info;\n";  
        }
    } else {
        $ret1 = $db->query("SELECT ID,MAP_INFO from MAPS WHERE ID = $id");
        while($row = $ret1->fetchArray()){
            $map_info = $row["MAP_INFO"];
            echo "const map_data = $map_info;\n";  
        }
        if($map_info == null){
            echo "window.alert('没有查询到 id=$id 的关卡地图数据！关卡地图数据可能已过期或者id不正确!')\n";
        }
    }
    $ret2 = $db->query("SELECT MIN(ID) from MAPS");
    while($row = $ret2->fetchArray()){
        $min_id = $row["MIN(ID)"];
        if(($id - $min_id) >= 100){
            $ret3 = $db->exec("DELETE from MAPS where ID=$min_id;");
            if(!$ret3){
                echo "window.alert('".$db->lastErrorMsg()."');\n";
            } else {
                echo "console.log('".$db->changes()."  成功删除数据');\n";
            }
        }
    }
?>

import * as THREE from 'three';

import { OrbitControls } from 'OrbitControls';

let camera, controls, scene, renderer;
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
const removed_blocks = [];

// 显示解答步骤的变量
var block_objects = {}
var solve_index = 0;
var highlight_mesh = null;
var solve_interval = null;

var material_blocks = [];
var mask_material_blocks = [];
var material_side;

// 卡槽
var slots = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
var counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
var slot_objects = [];

init();
//render(); // remove when using next line for animation loop (requestAnimationFrame)
animate();

bindEvent();

function init() {

    scene = new THREE.Scene();
    scene.background = new THREE.Color( 0xcff998 );
    //scene.fog = new THREE.FogExp2( 0xcccccc, 0.002 );

    renderer = new THREE.WebGLRenderer( { antialias: true } );
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.setSize( window.innerWidth, window.innerHeight );
    document.body.appendChild( renderer.domElement );

    //camera = new THREE.PerspectiveCamera( 90, window.innerWidth / window.innerHeight, 1, 2000 );
    camera = new THREE.OrthographicCamera( window.innerWidth / - 2, window.innerWidth / 2, window.innerHeight / 2, window.innerHeight / - 2, 1, 2000 );
    camera.setViewOffset( window.innerWidth, window.innerHeight, 0, -200, window.innerWidth, window.innerHeight );
    camera.position.set( 0, 0, 0 );

    // controls

    controls = new OrbitControls( camera, renderer.domElement );
    controls.listenToKeyEvents( window ); // optional

    //controls.addEventListener( 'change', render ); // call this only in static scenes (i.e., if there is no animation loop)

    controls.enableDamping = true; // an animation loop is required when either damping or auto-rotation are enabled
    controls.dampingFactor = 0.05;

    controls.screenSpacePanning = false;

    controls.minDistance = 100;
    controls.maxDistance = 500;

    controls.maxPolarAngle = Math.PI / 2;

    // 构建地图遮挡关系
    var mask_data = [];
    for (var row = 0; row < 80; row++) {
        var rows = [];
        for (var col = 0; col < 64; col++) {
            rows.push(null);
        }
        mask_data.push(rows);
    }
    const layers = map_data['layers'];
    const level_data = map_data['levelData'];
    for (let i = 0; i < layers.length; i++) {
        var layer = layers[i];
        var block_datas = level_data[layer];
        for (let j = 0; j < block_datas.length; j++) {
            var block_data = block_datas[j];
            counter[block_data.type] += 1;
            block_data.pre_blocks = [];     // 遮挡住的方块
            block_data.next_blocks = [];    // 被遮挡的方块
            // 取走方块方法
            block_data.take_away = function() {
                for (var i = 0; i < this.pre_blocks.length; i++) {
                    var pre_block = this.pre_blocks[i];
                    pre_block.next_blocks.pop(this);
                    update_block_material(block_objects[pre_block.id]);
                }
                counter[this.type] -= 1;
                slots[this.type] += 1;
                if (slots[this.type] >= 3) {
                    slots[this.type] = 0;
                }
                update_slots();
            }
            // 放回方块方法
            block_data.put_back = function() {
                for (var i = 0; i < this.pre_blocks.length; i++) {
                    var pre_block = this.pre_blocks[i];
                    pre_block.next_blocks.push(this);
                    update_block_material(block_objects[pre_block.id]);
                }
                counter[this.type] += 1;
                slots[this.type] -= 1;
                if (slots[this.type] < 0) {
                    slots[this.type] = 2;
                }
                update_slots();
            }
            // 是否可以移除
            block_data.removable = function() {
                return this.next_blocks.length == 0;
            }
            // 找出被当前方块遮挡住的方块
            var pre_blocks = [];
            for (var col = block_data.rolNum; col < block_data.rolNum+8; col++) {
                for (var row = block_data.rowNum; row < block_data.rowNum+8; row++) {
                    var pre_block = mask_data[row][col];
                    if (pre_block) {
                        pre_blocks.push(pre_block);
                    }
                    mask_data[row][col] = block_data;
                }
            }
            // 构建方块的遮挡关系
            for (var k = 0; k < pre_blocks.length; k++) {
                var pre_block = pre_blocks[k];
                if (block_data.pre_blocks.indexOf(pre_block) < 0) {
                    block_data.pre_blocks.push(pre_block);
                }
                if (pre_block.next_blocks.indexOf(block_data) < 0) {
                    pre_block.next_blocks.push(block_data);
                }
            }
        }
    }
    //console.log(mask_data);

    // 方块图案
    const textureLoader = new THREE.TextureLoader();
    material_side = new THREE.MeshLambertMaterial({
        map: textureLoader.load('sheep_images/side.png'),
    })
    for (let i = 0; i <= 16; i++) {
        material_blocks.push(new THREE.MeshLambertMaterial({
            map: textureLoader.load(`sheep_images/${i}.png`),
        }));
        mask_material_blocks.push(new THREE.MeshLambertMaterial({
            map: textureLoader.load(`sheep_images/mask/${i}.png`),
        }));
    }

    // 创建方块
    var geometry = new THREE.BoxGeometry(8, 2, 8);
    for (let i = 0; i < layers.length; i++) {
        var layer = layers[i];
        var block_datas = level_data[layer];
        for (let j = 0; j < block_datas.length; j++) {
            var block_data = block_datas[j];
            print_block_info(block_data, false);
            const block_object = new THREE.Mesh(geometry, null);
            block_object.position.x = block_data['rolNum'] - 28;
            block_object.position.y = (block_data['layerNum'] - 1) * 3.5;
            block_object.position.z = block_data['rowNum'] - 36;
            block_object.updateMatrix();
            block_object.matrixAutoUpdate = false;
            block_object.block_data = block_data;
            scene.add(block_object);
            block_objects[block_data['id']] = block_object;
            update_block_material(block_object);
        }
    }

    // 卡槽方块
    for (let i = 0; i < 7; i++) {
        const block_object = new THREE.Mesh(geometry, null);
        block_object.position.x = 8 * i - 24;
        block_object.position.y = 0;
        block_object.position.z = -64;
        block_object.updateMatrix();
        block_object.matrixAutoUpdate = false;
        scene.add(block_object);
        slot_objects.push(block_object);
        var block_data = {
            "type" : 0,
            "pre_blocks" : [],
            "next_blocks" : [],
            "is_slot" : true,
        }
        block_data.removable = function() {
            return true;
        }
        block_object.block_data = block_data;
        update_block_material(block_object);
    }

    if (map_data['operations'] != null) {

        // 高亮指示器
        geometry = new THREE.BoxGeometry(8, 2, 8);
        const material = new THREE.MeshBasicMaterial({color:0xff0000, opacity:0.6, transparent:true})
        highlight_mesh = new THREE.Mesh(geometry, material);
        highlight_mesh.position.x = 1000;
        highlight_mesh.position.y = 1000;
        highlight_mesh.position.z = 1000;
        highlight_mesh.updateMatrix();
        highlight_mesh.matrixAutoUpdate = false;
        scene.add(highlight_mesh);
        update_highlight_mesh();

        document.getElementById('auto_solve').text = "【自动解答】";
        document.getElementById('single_step_solve').text = "【单步解答】";
    }

    // lights
    const dirLight0 = new THREE.DirectionalLight( 0xffffff );
    dirLight0.position.set( 0, 100, 0 );
    scene.add( dirLight0 );

    const dirLight1 = new THREE.DirectionalLight( 0xffffff );
    dirLight1.position.set( 1, 0, 1 );
    scene.add( dirLight1 );

    const dirLight2 = new THREE.DirectionalLight( 0xffffff );
    dirLight2.position.set( - 1, - 1, - 1 );
    scene.add( dirLight2 );

    const ambientLight = new THREE.AmbientLight( 0x222222 );
    scene.add( ambientLight );

    window.addEventListener( 'resize', onWindowResize );

    document.addEventListener( 'click', onMouseClick );
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize( window.innerWidth, window.innerHeight );
}

function onMouseClick(event) {

    //将鼠标点击位置的屏幕坐标转换成threejs中的标准坐标
    mouse.x = (event.clientX/window.innerWidth) * 2 - 1;
    mouse.y = -((event.clientY/window.innerHeight) * 2 - 1);
 
    // 通过鼠标点的位置和当前相机的矩阵计算出raycaster
    raycaster.setFromCamera( mouse, camera );
 
    // 获取raycaster直线和所有模型相交的数组集合
    var intersects = raycaster.intersectObjects( scene.children );
    //console.log(intersects);
 
    if (intersects.length > 0) {
        var object = intersects[0].object;
        var block_data = object.block_data;
        if (!block_data.removable()) {
            return;
        }
        if (block_data.is_slot) {
            return;
        }
        if (map_data['operations'] != null) {
                        alert("有解的情况禁止手动移除方块，不然把解答途中的方块移除掉会导致局面出现问题。");
                        return;
                    }
        if (is_game_over()) {
            return;
        }
        print_block_info(block_data, true);
        removed_blocks.push(object);
        scene.remove(object);
        block_data.take_away();
    }
}

function animate() {
    requestAnimationFrame( animate );
    controls.update(); // only required if controls.enableDamping = true, or if controls.autoRotate = true
    render();
}

function render() {
    renderer.render( scene, camera );
}

// 打印方块信息
function print_block_info(block_data, is_remove) {

    var type2name = {
        1:  "青草",
        2:  "胡萝卜",
        3:  "玉米",
        4:  "树桩",
        5:  "草叉",
        6:  "白菜",
        7:  "羊毛",
        8:  "刷子",
        9:  "剪刀",
        10: "奶瓶",
        11: "水桶",
        12: "手套",
        13: "铃铛",
        14: "火堆",
        15: "毛球",
        16: "干草"
    }

    var layer = block_data['layerNum'];
    var x = block_data['rolNum'];
    var y = block_data['rowNum'];
    var type = block_data['type'];
    var name = type2name[type];
    var info = `层数:${layer}, 坐标:(${x}, ${y}), 类型:${type}(${name})`
    if (is_remove) {
        info = "移除方块 >> " + info;
    }
    console.log(info);
}

// 游戏是否结束
function is_game_over() {
    var sum = 0;
    for (var i = 0; i < slots.length; i++) {
        sum += slots[i];
    }
    return sum >= 7;
}

// 更新方块图案
function update_block_material(block_object) {
    var material = null;
    var block_data = block_object.block_data; 
    if (block_data.removable()) {
        material = material_blocks[block_data.type];
    } else {
        material = mask_material_blocks[block_data.type];
    }
    var materials = block_object.material;
    if (materials == null) {
        materials = [material_side, material_side, material, material_side, material_side, material_side];
    } else {
        materials[2] = material;
    }
    block_object.material = materials;
}

// 更新卡槽方块
function update_slots() {
    for (let i = 0; i < 7; i++) {
        var object = slot_objects[i];
        object.block_data.type = 0;
        update_block_material(object);
    }

    var index = 0;
    for (let i = 0; i < slots.length; i++) {
        for (let j = 0; j < slots[i]; j++) {
            if (index >= 7) {
                return;
            }
            var object = slot_objects[index];
            object.block_data.type = i;
            update_block_material(object);
            index += 1;
        }
    }
}

// 更新高亮方块位置
function update_highlight_mesh() {
    if (solve_index < map_data['operations'].length) {
        var block_id = map_data['operations'][solve_index];
        var block_object = block_objects[block_id];
        highlight_mesh.position.x = block_object.position.x;
        highlight_mesh.position.y = block_object.position.y;
        highlight_mesh.position.z = block_object.position.z;
    } else {
        highlight_mesh.position.x = 1000;
        highlight_mesh.position.y = 1000;
        highlight_mesh.position.z = 1000;
    }
    highlight_mesh.updateMatrix();
}

// 撤销移除
function undo() {
    const object = removed_blocks.pop();
    if (object) {
        scene.add(object);
        object.block_data.put_back();
        if (solve_index > 0) {
            solve_index -= 1;
        }
        update_highlight_mesh();
    }
}

// 自动解答
function auto_solve() {
    var auto_solve_element = document.getElementById('auto_solve');
    if (solve_interval == null) {
        solve_interval = setInterval(function() {
            single_step_solve();
        }, 1500);
        auto_solve_element.text = '【停止解答】';
    } else {
        clearInterval(solve_interval);
        solve_interval = null;
        auto_solve_element.text = '【自动解答】';
    }
}

// 单步解答
function single_step_solve() {
    if (map_data['operations'] == null) {
        return;
    }
    if (solve_index >= map_data['operations'].length) {
        return;
    }
    var block_id = map_data['operations'][solve_index];
    var block_object = block_objects[block_id];
    scene.remove(block_object);
    removed_blocks.push(block_object);
    print_block_info(block_object.block_data, true);
    block_object.block_data.take_away();
    solve_index += 1;
    update_highlight_mesh();
    //console.log("counts :", counter);
    //console.log("slots  :", slots);
}

function bindEvent(){
    document.getElementById('undo').onclick = undo;
    document.getElementById('auto_solve').onclick = auto_solve;
    document.getElementById('single_step_solve').onclick = single_step_solve;
}
