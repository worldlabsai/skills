# Example run: a studio as splats

The request was "turn this into a 3D scene I can look around in", from one 16:9 image of a
potter's studio seen from its doorway: a work table with a wheel and unfired bowls in the middle
of the room, shelves of pots along the walls, a kiln in a corner, windows on the left.

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

## The reconstruction

The eight frames were checked as input: the floor, the table from every side, and all four walls
appear in at least one view, the table and wheel agree across views, and every frame is 1280x720
with depth. Eight is the low end for a room; it was enough here because the room is small and the
views surround its one large object.

[`splats-request.json`](../assets/example/splats-request.json) is the request: the posed frame
and the seven views, each with its image, depth and camera. It was submitted once, refined, and
took 18 minutes.

## The result

One SPZ file with 2,000,000 splats, 31 MB, in the same world as the cameras that were sent.
[`splats.jpg`](../assets/example/splats.jpg) shows it rendered from eight positions it was not
given: along a path that enters the room and circles the table.

- From inside the room the scene is sharp and holds together from every side, including the
  walls the model invented.
- From the source camera's own position (the first picture) a blurred surface covers the lower
  part of the view. The door threshold and frame were close to the lens and only the source
  image saw them, so they reconstructed poorly. Surfaces that one view sees at close range are
  the weak spot to tell the person about, or to cover with another view.
