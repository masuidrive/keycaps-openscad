

// 角丸のプレート
module rounded_plate(x, y, r) {
  thickness = 0.0001;
  minkowski () {
    cube([x-r*2, y-r*2, thickness], center = true);
    cylinder(r = r, h = thickness);
  }
}

// ベーシックなキーキャップの外観を定義
module keycap_basic_outer_shape(bottom_size, middle_size, top_size, top_height, skert_height) {
  hull () {
    translate([0, 0, top_height])
    rounded_plate(top_size, top_size, 1);
    
    if(middle_size > 0) {
      translate([0, 0, 0])
      rounded_plate(middle_size, middle_size, 1);
    }
    
    translate([0, 0, -skert_height])
    rounded_plate(bottom_size, bottom_size, 1);
  }
}

// chocで使われる一般的なキーキャップの形状を定義
module keycap_basic_shape(
  top_size,
  head_height,
  middle_size,
  skert_height,
  bottom_size,
  thickness = 1.0,
  side_r = 1.0) {
  difference () {
    // 外形
    keycap_basic_outer_shape(bottom_size, middle_size, top_size, head_height, skert_height, side_r);
    // くり抜くための外形
    keycap_basic_outer_shape(bottom_size - thickness * 2, middle_size - thickness * 2, top_size - thickness * 2, 0, skert_height, side_r);
  }
}


// cylindricalな凹みを作る
module head_cylindrical_depress(top_size, top_height, depth) {
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

// https://qiita.com/zk_phi/items/ab99315ebaef66e84aa0
// https://bebebe.hatenablog.jp/entry/2019/06/04/232501
// https://qiita.com/zk_phi/items/ab99315ebaef66e84aa0
