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
module keycap1_outer_shape(bottom_size, middle_size, top_size, head_height, skert_height, r=1) {
  hull () {
    translate([0, 0, head_height])
    rounded_plate(top_size, top_size, r);
    
    if(middle_size > 0) {
      translate([0, 0, 0])
      rounded_plate(middle_size, middle_size, r);
    }
    
    translate([0, 0, -skert_height])
    rounded_plate(bottom_size, bottom_size, r);
  }
}

module keycap1_shape(
  top_size,
  head_height,
  middle_size,
  skert_height,
  bottom_size,
  thickness = 1.0,
  r = 1.0) {
  difference () {
    // 外形
    keycap1_outer_shape(bottom_size, middle_size, top_size, head_height, skert_height, r);
    // くり抜くための外形
    keycap1_outer_shape(bottom_size - thickness * 2, middle_size - thickness * 2, top_size - thickness * 2, 0, skert_height, r);
  }
}

// ChocV1の足を作る
module kailh_choc_v1_stem() {
  leg_length = 3.6;
  thin_length = 0.6;

  for (z = [-2.85, 2.85]) {
    translate([z, 0, -leg_length/2])
      hull() {
        cube([1, 2, leg_length], center=true);
        translate([0, 0, -(leg_length/2)-thin_length])
          cube([0.5, 1, 0.001], center=true);
      }
  }
}

// キーキャップ生成
module generate(
  top_size,
  head_height,
  middle_size,
  skert_height,
  bottom_size,
  thickness = 1.0,
  r = 1.0
) {
  union() {
    keycap1_shape(top_size, head_height, middle_size, skert_height, bottom_size, thickness, r);
    kailh_choc_v1_stem();
  }
}

translate([-10, 0, 0])
generate(
  12.5, // top_size
  1.5, // head_height
  14, // middle_size
  1.0, // skert_height
  15, // bottom_size
  1.0, //thickness
  1.0 // r
);

translate([10, 0, 0])
generate(
  15.6, // top_size
  1.5, // head_height
  0, // middle_size
  1.0, // skert_height
  15.6, // bottom_size
  1.0, // thickness
  2.0 // r
);
