# Example run: an orbit around a work table

The request was "a video that goes into this studio and circles the work table", from one 16:9
image of a potter's studio seen from its doorway: a work table with a wheel and unfired bowls in
the middle of the room, shelves of pots along the walls, a kiln in a corner, windows on the left.

These are the choices made for this scene. Another scene, or another reading of the request,
calls for different ones.

## What posing returned

[`pose-request.json`](../assets/example/pose-request.json) is the request and
[`pose-result.json`](../assets/example/pose-result.json) the part of the saved result that
matters. The camera is 0.97 above the floor and tilted about 7 degrees down. `fx` is 762 on a
1280-wide grid, an 80 degree horizontal field of view.

Reading the depth file gave a typical (median) depth of 2.5, with the nearest surface 1.3 away
and the far shelves about 5.5 away. The work table is the main part of the scene. Its top, at the
pixel in the middle of the table, is 1.9 from the camera and 0.64 above the floor. There is open
floor all round the table, between it and the shelves.

## The sparse views

Seven cameras on a circle around the table, each aimed at the table top:

- The circle's radius is 1.2, about two thirds of the source camera's distance to the table. That
  keeps every position over open floor, which was checked against the depth.
- The cameras sit every 45 degrees from 45 to 315, counted from the source camera's side. The
  source image covers the remaining direction.
- They are at the source camera's height, 0.97.

[`views-request.json`](../assets/example/views-request.json) is the whole request: the posed
frame as context, the seven cameras, and `"returnDepth": true`. It took 23 seconds and cost 110
credits.

[`views.jpg`](../assets/example/views.jpg) shows the source image and the seven views. The table,
wheel and bowls keep their shape and place all the way round. The model invented everything the
photo could not see: the far side of the wheel, shelving on the wall behind the source camera, and
doorways on two sides of the room.

## What the person saw

The contact sheet, with a note that the back wall and the doorways are invented, and the cost and
time of the next step. They agreed to continue.

## The path

- 8 seconds at 24 frames a second: 192 cameras.
- The first camera is the posed source camera, so the video opens on the photo.
- Over the first 30 frames the camera moves 0.65 straight ahead, through the doorway, to the
  circle the views stood on, and turns to aim at the table top.
- It then goes once around the table on that circle and ends where it joined it, easing in and
  out. The largest step between frames is 0.05 and 2.5 degrees of the circle.

A first attempt went from the source camera directly toward the nearest view's position and
closed in on the circle as it went. Both ends of that stretch were in open space, but the line
between them was not: the frames in the middle looked into the door frame. Moving straight in
first fixed it.

[`path-request.json`](../assets/example/path-request.json) is the request with 9 of the 192
target cameras kept (every 24th and the last) so the file stays small. Its context is the posed
frame and all seven views, each with its depth.

## The result

One request, 109 seconds, 192 JPEG frames at 1280x720, 1,568 credits.
[`frames.jpg`](../assets/example/frames.jpg) shows twelve of them in order.

- The first frame matches the photo.
- The table, wheel and bowls hold their shape through the whole circle, and the shelving behind
  the source camera matches what the sparse views showed.
- The door frame crosses the edge of the picture as the camera passes the doorway on the way
  round, as it should.
