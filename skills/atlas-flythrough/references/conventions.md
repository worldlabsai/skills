# Camera and depth conventions

These are properties of the API's results, stated so you do not have to work them out. This file
is identical in `atlas-flythrough` and `atlas-splats`.

## Cameras

A camera is
`{"extrinsics": {"position", "quaternion", "coordinateSystem": "rub"}, "intrinsics": {"width", "height", "fx", "fy", "cx", "cy"}}`.

- The pose is camera-to-world: `position` is where the camera is and `quaternion` is its
  orientation.
- Camera axes are +X right, +Y up, +Z back, so the camera looks along its own -Z.
- Quaternions are `[x, y, z, w]`.
- After `images2PosedRGBD` the world is Y-up and level with gravity, so the floor is horizontal.
- Turning right (clockwise seen from above) is a negative rotation about world +Y. A camera with
  no rotation that turns 30 degrees right has quaternion `[0, -0.2588, 0, 0.9659]`.
- Intrinsics are in pixels with the origin at the top-left. They describe the depth grid, which is
  the size you asked for in `targetResolution`.
- Horizontal field of view is `2 * atan(width / (2 * fx))`.
- A target camera has the same shape as a posed one. Keep the posed camera's intrinsics unless you
  change the output size. All target cameras in one request share one size: 1280x720, 960x720,
  528x704 or 720x1280.

## Depth

- A depth file is an EXR with one channel. Rows run top to bottom, like the image.
- Each value is the distance along the camera's view axis (not along the ray through that pixel),
  in the same units as camera positions.
- `NaN`, `0`, negative and infinite values mean no surface there, such as sky.
- The scale is estimated from the image. Treat distances as consistent within the scene, not as
  measured metres.
- A point seen at pixel `(u, v)` with depth `z` is at
  `((u - cx) / fx * z, -(v - cy) / fy * z, -z)` in the camera's axes.
- The confidence file is an image on the same grid. Low values mark depth to trust less.

## Frames

A posed or generated frame is an image, its camera and its depth. Keep the three together: a
frame used as context for `atlasGenerate`, or as input to `posedImages2Splats`, names all three.

A posed frame also has `centroidWorld`: the mean visible point, projected onto the floor
(`y = 0`). It is a rough centre of what the image sees, which is not always the subject.

More: https://docs.atlas.worldlabs.ai/cameras-and-posed-images.md
