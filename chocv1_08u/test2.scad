// https://qiita.com/zk_phi/items/ab99315ebaef66e84aa0
// https://bebebe.hatenablog.jp/entry/2019/06/04/232501
// https://qiita.com/zk_phi/items/ab99315ebaef66e84aa0

$fs = 0.1;
$fa = 0.25;

module rounded_plate(x, y, r) {
  thickness = 0.0001;
  minkowski () {
    cube([x-r*2, y-r*2, thickness], center = true);
    cylinder(r = r, h = thickness);
  }
}


module keycap1_outer_shape(bottom_size, middle_size, top_size, top_height, skert_height) {
  hull () {
    translate([0, 0, top_height])
    rounded_plate(top_size, top_size, 1);
    
    translate([0, 0, 0])
    rounded_plate(middle_size, middle_size, 1);
    
    translate([0, 0, -skert_height])
    rounded_plate(bottom_size, bottom_size, 1);
  }
}

module head_depress(top_size, top_height, depth) {
  // https://qiita.com/zk_phi/items/ab99315ebaef66e84aa0
  function dish_r(w, d) = (w * w + 4 * d * d) / (8 * d);
  
  hull() {
    angle = 0;
    translate([0, 0, top_height]);
    rotate([- angle, 0, 0])
    translate([0, 0, dish_r(top_size, depth) - depth+top_height])
    rotate([90, 0, 0])
    cylinder(r = dish_r(top_size, depth), h = 60, /* 適当に十分な長さ */ center = true);
  }
}

module keycap_shape () {
  thickness = 1.0;
  
  bottom_size = 15;
  middle_size = 14;
  top_height = 1.5;
  top_size = 12;
  top_depth = 1.0;
  skert_height = 5.0; 

  
  difference () {
    // 外形
    keycap1_outer_shape(bottom_size, middle_size, top_size, top_height, skert_height);
    
    // 上部の凹み
    head_depress(top_size, 1.5, 1);

    // くり抜くための外形
    keycap1_outer_shape(bottom_size - thickness * 2, middle_size - thickness * 2, top_size - thickness * 2, 0, skert_height);
  }
}

difference() {

keycap_shape();

}

module kailh_choc_v1_stem() {
    translate([-2.85, 0, -3/2])
    cube([1, 2, 3], center=true);
    translate([2.85, 0, -3/2])
    cube([1, 2, 3], center=true);
}

kailh_choc_v1_stem();
