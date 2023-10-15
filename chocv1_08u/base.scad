$fs = 0.1;

// 角丸のプレート
module rounded_plate(x, y, r) {
  thickness = 0.0001;
  minkowski () {
    cube([x-r*2, y-r*2, thickness], center = true);
    cylinder(r = r, h = thickness);
  }
}

// キーキャップの外観を定義
module keycap1_outer_shape(bottom_size, middle_size, top_size, head_height, skert_height) {
  hull () {
    translate([0, 0, head_height])
    rounded_plate(top_size, top_size, 1);
    
    translate([0, 0, 0])
    rounded_plate(middle_size, middle_size, 1);
    
    translate([0, 0, -skert_height])
    rounded_plate(bottom_size, bottom_size, 1);
  }
}

module keycap_shape() {
  thickness = 1.0;
  
  head_height = 1.5;
  bottom_size = 15;
  middle_size = 14;
  top_size = 12.5;
  skert_height = 5.0; 
  
  difference () {
    // 外形
    keycap1_outer_shape(bottom_size, middle_size, top_size, head_height, skert_height);
    // くり抜くための外形
    keycap1_outer_shape(bottom_size - thickness * 2, middle_size - thickness * 2, top_size - thickness * 2, 0, skert_height);
  }
}

module kailh_choc_v1_stem() {
  translate([-2.85, 0, -3/2])
  cube([1, 2, 3], center=true);
  translate([2.85, 0, -3/2])
  cube([1, 2, 3], center=true);
}

union() {
  keycap_shape();
  kailh_choc_v1_stem();
}
