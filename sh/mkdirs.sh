#/usr/bin/env bash
cat sku.txt | while IFS=$'\t' read -r brand sku _; do
  echo $brand $sku
  mkdir -p ./images/products/$brand/$sku
  cp ./old_images/$sku.jpg ./images/products/$brand/$sku/
  cp ./old_images/${sku}m.jpg ./images/products/$brand/$sku/
  cp ./old_images/${sku}fb.jpg ./images/products/$brand/$sku/
  cp ./old_images/${sku}big.jpg ./images/products/$brand/$sku/

  for i in {1..9}
  do
    cp ./old_images/${sku}fb-${i}.jpg ./images/products/$brand/$sku/
  done

  for i in {1..9}
  do
    cp ./old_images/${sku}big-${i}.jpg ./images/products/$brand/$sku/
  done

done