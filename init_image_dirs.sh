#!/bin/bash

# Base legends directory
mkdir -p images/leg

# Hydrometeor vertical cross sections
for i in {0..5}
do
  mkdir -p images/lat/${i}
  mkdir -p images/lon/${i}
done

# Hydrometeor planar cross sections
for i in {0..10}
do
  mkdir -p images/vert/${i}
done

# Hydrometeor legends
mkdir -p images/leg

# Create empty figure when reflectivity is not loaded
#convert -size 400x200 xc:transparent images/transparent.png

# Reflectivity vertical cross sections
for i in {0..5}
do
  mkdir -p images/h/lat/${i}
  mkdir -p images/h/lon/${i}
  mkdir -p images/l/lat/${i}
  mkdir -p images/l/lon/${i}

  cp images/transparent.png images/h/lat/${i}/0.png
  cp images/transparent.png images/h/lon/${i}/0.png
  cp images/transparent.png images/l/lat/${i}/0.png
  cp images/transparent.png images/l/lon/${i}/0.png
done

# Reflectivity planar cross sections
for i in {0..10}
do
  mkdir -p images/h/vert/${i}
  mkdir -p images/l/vert/${i}

  cp images/transparent.png images/h/vert/${i}/0.png
  cp images/transparent.png images/l/vert/${i}/0.png
done

# Reflectivity legends
mkdir -p images/h/leg
mkdir -p images/l/leg

cp images/transparent.png images/h/leg/0.png
cp images/transparent.png images/l/leg/0.png
